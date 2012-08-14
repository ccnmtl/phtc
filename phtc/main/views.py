from annoying.decorators import render_to
from django.http import HttpResponseRedirect, HttpResponse
from pagetree.helpers import get_section_from_path, get_hierarchy
from pagetree.helpers import get_module, needs_submit, submitted
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.simplejson import dumps
from phtc.main.models import UserProfile
from phtc.main.forms import UserRegistrationForm
from phtc.main.models import DashboardInfo
from pagetree.models import UserPageVisit
from django.core.mail import EmailMessage
import os.path
import pdb

def redirect_to_first_section_if_root(section, root):
    if section.id == root.id:
        # trying to visit the root page
        if section.get_next():
            # just send them to the first child
            # users will redirect to their dashboard
            # - if not logged in will goto login page
            return HttpResponseRedirect(reverse("dashboard"))


def update_status(section, user, module, request):
    if user.is_anonymous():
        return
    prev_status = False
    prev_section = section.get_previous()
    if prev_section:
        try:
            prev_status = UserPageVisit.objects.get(
                section=prev_section,
                user=user).status
        except UserPageVisit.DoesNotExist:
            pass
    uv = section.get_uservisit(user)
    if not uv and not prev_status:
        return
    if not is_module(module, user, request, section):
        status = calculate_status(prev_status, uv)
        section.user_pagevisit(user, status=status)


def calculate_status(prev_status, uv):
    if uv:
        if prev_status:
            if prev_status == "complete" or prev_status == "in_progress":
                return "in_progress"
        if uv.status == "allowed" or uv.status == "in_progress":
            return "in_progress"
        elif uv.status == "complete":
            return "complete"
        else:
            return "incomplete"
    else:
        if prev_status == "in_progress":
            return "in_progress"
        else:
            return "incomplete"


def user_visits(request):
    return UserPageVisit.objects.filter(user=request.user)


def send_post_test_email(user, section, module):
    directory = os.path.dirname(__file__)
    email = EmailMessage()
    email.subject = "Public Health Training Diploma"
    if is_module_one(module, section, user):
        section_msg = module.label + ' ' + section.label +'<a href="http://kang.ccnmtl.columbia.edu:13095/certificate' + module.get_absolute_url() + ' ">Click Here to print certificate</a>  '
    else:
        section_msg = module.label
    email.body = ('Congratulations on completing ' + section_msg +
                  '. Please find the attached certificate of completion.')
    email.from_email = "lowernysphtc.org <no-reply@lowernysphtc.org>"
    email.to = [user.email, ]

    #attach the file
    file = open(directory + '/../../media/img/diploma.jpg', 'rb')
    email.attach(filename="diploma.jpg",
                 mimetype="image/jpeg",
                 content=file.read())
    file.close()

    email.send(fail_silently=False)


def page_post(request, section, module):
    if request.POST.get('post_test') == "true":
        # not sute sure yet if module 1 needs to be handled spererately
        if is_module_one(module, section, request.user):
            send_post_test_email(request.user, section, module)
            module.user_pagevisit(request.user, status="complete")
            section.user_pagevisit(request.user, status="complete")
        else:
            send_post_test_email(request.user, section, module)
            module.user_pagevisit(request.user, status="complete")
            section.user_pagevisit(request.user, status="complete")

    if request.user.is_anonymous():
        return HttpResponse("you must login first")
    # user has submitted a form. deal with it
    if request.POST.get('action', '') == 'reset':
        section.reset(request.user)
        section.user_pagevisit(request.user, status="incomplete")
        return HttpResponseRedirect(section.get_absolute_url())
    proceed = section.submit(request.POST, request.user)
    if proceed:
        section.user_pagevisit(request.user, status="complete")
        return HttpResponseRedirect(section.get_next().get_absolute_url())
    elif request.POST.get('post_test') == "true":
        #forward over to dashboard
        return HttpResponseRedirect(reverse('dashboard'))
    elif request.POST.get('pre_test') == "true":
        #return HttpResponse(request.POST)
        return HttpResponseRedirect(section.get_absolute_url())
    else:
        # giving them feedback before they proceed
        return HttpResponseRedirect(section.get_absolute_url())


def make_sure_module1_parts_are_allowed(module, user):
    parts = module.get_children()
    for part in parts:
        try:
            part_status = UserPageVisit.objects.get(section_id=part.id,
                                                    user_id=user.id)
            if part_status == "in_progress":
                try:
                    visit = UserPageVisit.objects.get(
                    section_id=part.get_previous().id,
                    user_id=user_id)
                    visit.status = "complete"
                    visit.save()
                except:
                    pass
        except:
            part_status = UserPageVisit.objects.get_or_create(
                section_id=part.id,
                user_id=user.id,
                status="allowed")

def make_sure_parts_are_allowed(module, user, request, section, is_module):
    #handle Module one seperately
    if is_module_one(module, section, user):
        make_sure_module1_parts_are_allowed(module, user)
    else:
        if is_module == True:
            if UserPageVisit.objects.get(
                section=module,
                user=user).status == "complete":
                module.user_pagevisit(request.user, status="complete")
                return
            try:
                status = "exists"
                UserPageVisit.objects.get(
                    section=section.get_next(), user=user)
            except UserPageVisit.DoesNotExist:
                status = "created"

            if status == "exists":
                if UserPageVisit.objects.get(
                    section=section.get_next(),
                    user=user).status == "in_progress":
                    section.get_next().user_pagevisit(request.user,
                                                      status="complete")
                elif UserPageVisit.objects.get(
                    section=section.get_next(),
                    user=user).status == "allowed":
                    section.get_next().user_pagevisit(request.user,
                                                      status="in_progress")
            if status == "created":
                section.get_next().user_pagevisit(
                    request.user, status="allowed")


def part_flagged_as_allowed(upv):
    return upv.status == "allowed" or upv.status == "in_progress"

def is_module_one(module, section, user):
    modArr = section.hierarchy.get_root().get_children()
    if module.label == modArr[0].label:
        return True
    else:
        return False

def is_module(module, user, request, section):
    try:
        mod_obj = UserPageVisit.objects.get(
            section=module,
            user=user)
        sec_obj = UserPageVisit.objects.get(
            section=section,
            user=user)
        if mod_obj.id == sec_obj.id:
            return True
    except UserPageVisit.DoesNotExist:
        return False


def process_dashboard_ajax(request, user, section, module):
    try:
        mod_status = UserPageVisit.objects.get(
            section=module,
            user=user).status
    except UserPageVisit.DoesNotExist:
        mod_status = False
    if mod_status == "complete":
        if not is_module_one(module, section, user):
            for sec in module.get_children():
                sec.user_pagevisit(request.user, status="complete")
            return reverse("dashboard")
    else:
        module.user_pagevisit(request.user, status="in_progress")
        make_sure_parts_are_allowed(module, user, request, section,
            is_module(module, user, request, section))
        return reverse("dashboard")


@login_required
@render_to('main/page.html')
def page(request, path):
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    module = get_module(section)
    is_visited = user_visits(request)

    # dashboard ajax
    if request.POST.get('module'):
        return HttpResponse(
            process_dashboard_ajax(request, request.user, section, module))

    #is the user allowed?
    if not request.user.is_anonymous():
        section.user_visit(request.user)

    rv = redirect_to_first_section_if_root(section, root)
    if rv:
        return rv
    update_status(section, request.user, module, request)

    if request.method == "POST":
        return page_post(request, section, module)

    # test if there is a previous section - if so then
    # decide whether to change status
    if section.get_previous():
        prev_section = section.get_previous()
        try:
            prev_section_visit = UserPageVisit.objects.get(
                section=prev_section,
                user=request.user)
            if (prev_section_visit.status == "in_progress"
                and not is_module(module, request.user, request,
                                  prev_section)):
                section.get_previous().user_pagevisit(
                    request.user, status="complete")
        except UserPageVisit.DoesNotExist:
            # Need to catch whether a part has been flagged as "allowed"
            try:
                upv = UserPageVisit.objects.get(
                    section=section,
                    user=request.user)
                prev_section_visit = part_flagged_as_allowed(upv)
            except UserPageVisit.DoesNotExist:
                prev_section_visit = False
                pass
        # make sure user cannot type in url by hand to skip around
        if not hand_type_secure(prev_section_visit, request, section):
            section.user_pagevisit(request.user, status="incomplete")
            return HttpResponseRedirect("/dashboard/?incomplete=true")

    return dict(section=section,
                module=module,
                is_visited=is_visited,
                needs_submit=needs_submit(section),
                is_submitted=submitted(section, request.user),
                modules=root.get_children(),
                root=section.hierarchy.get_root(),
                )


def hand_type_secure(prev_section_visit, request, section):
    if prev_section_visit == False:
        if request.user.is_staff:
            section.user_pagevisit(request.user, status="in_progress")
            return True
        return False
    else:
        return True


@login_required
@render_to('main/edit_page.html')
def edit_page(request, path):
    if request.user.is_staff:
        section = get_section_from_path(path)
        root = section.hierarchy.get_root()
        edit_page = True
        try:
            DashboardInfo.objects.get(dashboard=section)
        except DashboardInfo.DoesNotExist:
            DashboardInfo.objects.create(dashboard=section)

        dashboard = DashboardInfo.objects.get(dashboard=section)
        if request.method == "POST":
            dashboard_info = request.POST['dashboard_info']
            dashboard.info = dashboard_info

        dashboard.save()

        return dict(section=section,
                    dashboard=dashboard,
                    module=get_module(section),
                    modules=root.get_children(),
                    root=section.hierarchy.get_root(),
                    edit_page=edit_page)
    else:
        return HttpResponseRedirect(reverse("dashboard"))


@render_to('main/instructor_page.html')
def instructor_page(request, path):
    return dict()


def exporter(request):
    h = get_section_from_path('/').hierarchy
    data = h.as_dict()
    resp = HttpResponse(dumps(data))
    resp['Content-Type'] = 'application/json'
    return resp


@login_required
@render_to('main/profile.html')
def get_user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        form = UserRegistrationForm(initial={
                'username': request.user.username,
                'email': request.user.email,
                'sex': profile.sex,
                'age': profile.age,
                'origin': profile.origin,
                'ethnicity': profile.ethnicity,
                'disadvantaged': profile.disadvantaged,
                'employment_location': profile.employment_location,
                'position': profile.position,
                })
        return dict(profile=profile, form=form)
    except UserProfile.DoesNotExist:
        form = UserRegistrationForm(initial={
                'username': request.user.username,
                'email': request.user.email,
                })
    return dict(form=form, user=request.user)


@login_required
def update_user_profile(request):
    form = UserRegistrationForm(request.POST)
    request.user.username = form.data["username"]
    if form.data["password1"] != "":
        request.user.set_password(form.data["password1"])
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        userprofile = UserProfile.objects.create(user=request.user)
    userprofile.sex = form.data["sex"]
    userprofile.age = form.data["age"]
    userprofile.origin = form.data["origin"]
    userprofile.ethnicity = form.data["ethnicity"]
    userprofile.disadvantaged = form.data["disadvantaged"]
    userprofile.employment_location = form.data["employment_location"]
    userprofile.position = form.data["position"]
    userprofile.save()
    request.user.save()
    return HttpResponseRedirect('/profile/?saved=true/')


@login_required
@render_to('main/dashboard.html')
def dashboard(request):
    return render_dashboard(request)


@login_required
@render_to('main/dashboard_panel.html')
def dashboard_panel(request):
    return render_dashboard(request)

@login_required
@render_to('main/certificate.html')
def certificate(request, path):
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    module = get_module(section)
    is_visited = user_visits(request)
    return dict(section=section,
            module=module,
            is_visited=is_visited,
            needs_submit=needs_submit(section),
            is_submitted=submitted(section, request.user),
            modules=root.get_children(),
            root=section.hierarchy.get_root(),
            user = request.user,
            )

def render_dashboard(request):
    h = get_hierarchy("main")
    root = h.get_root()
    last_session = h.get_user_section(request.user)
    dashboard_info = DashboardInfo.objects.all()

    is_visited = user_visits(request)
    empty = ""
    return dict(root=root, last_session=last_session,
                dashboard_info=dashboard_info,
                empty=empty, is_visited=is_visited)

from annoying.decorators import render_to
from django.http import HttpResponseRedirect, HttpResponse
from pagetree.helpers import get_section_from_path, get_hierarchy
from pagetree.helpers import get_module, needs_submit, submitted
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.simplejson import dumps
from phtc.main.models import UserProfile
from phtc.main.forms import UserRegistrationForm
from phtc.main.models import DashboardInfo
from pagetree.models import UserPageVisit
from pagetree.models import Section
from django.core.mail import send_mail

def redirect_to_first_section_if_root(section, root):
    if section.id == root.id:
        # trying to visit the root page
        if section.get_next():
            # just send them to the first child
            # users will redirect to their dashboard
            # - if not logged in will goto login page
            return HttpResponseRedirect("/dashboard/")


def update_status(section, user):
    prev_status = False
    try:
        prev_status = UserPageVisit.objects.get(section_id = section.get_previous().id, user_id =user.id).status
    except:
        pass
    uv = None
    if not user.is_anonymous():
        uv = section.get_uservisit(user)
        if not uv:
            if prev_status != False:
                if prev_status == "in_progress":
                    section.user_pagevisit(user, status ="in_progress")
            else:
                section.user_pagevisit(user, status="incomplete")
        else:

            if prev_status != False:
                if prev_status == "complete":
                    section.user_pagevisit(user, status="in_progress")
                    return
                if prev_status == "in_progress":
                    section.user_pagevisit(user, status="in_progress")
                    return

            if uv.status == "allowed":
                section.user_pagevisit(user, status="in_progress")
            elif uv.status == "in_progress":
                section.user_pagevisit(user, status="in_progress")
            elif uv.status == "complete":
                section.user_pagevisit(user, status="complete")
            else:
                # we still want the last_visit time to update
                section.user_pagevisit(user, status="incomplete")

def user_visits(request):
    visits = UserPageVisit.objects.filter(user_id = request.user)
    return visits

def send_post_test_email():
    send_mail('PHTC Training', 'Here is your digital diploma!', 'admin@lowernysphtc.org',
    ['djredhand@gmail.com'], fail_silently=False)

@login_required
@render_to('main/page.html')
def page(request, path):
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    module = get_module(section)
    is_visited = user_visits(request)
    user_id = request.user.id
        

    if not request.user.is_anonymous():
        section.user_visit(request.user)

    rv = redirect_to_first_section_if_root(section, root)
    if rv:
        return rv
    update_status(section, request.user)
    #return HttpResponse( update_status(section, request.user) )

    if request.method == "POST":
        #if request.POST.get('pre_test') == "true":
            #return HttpResponse('YES this is a PRE_test submit')
        if request.POST.get('post_test') == "true":
            send_post_test_email()
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
        else:
            # giving them feedback before they proceed
            return HttpResponseRedirect(section.get_absolute_url())
    else:
        #make sure modules are allowed
        rootMods = root.get_children()
        for mod in rootMods:
            mod.user_pagevisit(request.user, status="allowed")
            try:
                mod_next_visit = UserPageVisit.objects.get(section_id = mod.get_next().id, user_id = user_id)
                if mod_next_visit.status == "in_progress":
                    mod.user_pagevisit(request.user, status="in_progress")
            except:
                pass

        # make sure that "Parts" are allowed
        parts = module.get_children()
        for part in parts:
            try:
                part_status = UserPageVisit.objects.get(section_id = part.id, user_id = user_id)
                if part_status == "in_progress":
                    visit = UserPageVisit.objects.get(section_id = prev_section.id, user_id = user_id)
                    visit.status = "complete"
                    visit.save()
            except:
                part_status = UserPageVisit.objects.get_or_create(section_id = part.id, user_id = user_id, status ="allowed")


        if section.get_previous():
            prev_section = section.get_previous()
            try:
                prev_section_visit = UserPageVisit.objects.get(section_id = prev_section.id, user_id = user_id)
                if prev_section_visit.status == "in_progress":
                    visit = UserPageVisit.objects.get(section_id = prev_section.id, user_id = user_id)
                    visit.status = "complete"
                    visit.save()
            except:
                #return HttpResponse(UserPageVisit.objects.get(section_id = section.id, user_id = user_id).status)
                # Need to catch whether a part has been flagged as "allowed"
                if UserPageVisit.objects.get(section_id = section.id, user_id = user_id).status == "allowed":
                    prev_section_visit = True
                elif UserPageVisit.objects.get(section_id = section.id, user_id = user_id).status == "in_progress":
                    prev_section_visit = True
                else:
                    prev_section_visit = False
                #return HttpResponse (UserPageVisit.objects.get(section_id = section.id, user_id = user_id).status)
            # make sure user cannot type in url by hand to skip around
            if prev_section_visit == False:
                if request.user.is_staff:
                    section.user_pagevisit(request.user, status="in_progress")
                    
                else:
                    section.user_pagevisit(request.user, status="incomplete")
                    go_back_message = "/dashboard/?incomplete=true"
                    return HttpResponseRedirect(go_back_message )

            
    return dict(section=section,
                module=module,
                is_visited = is_visited,
                needs_submit=needs_submit(section),
                is_submitted=submitted(section, request.user),
                modules=root.get_children(),
                root=section.hierarchy.get_root(),
                )


@login_required
@render_to('main/edit_page.html')
def edit_page(request, path):
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    edit_page = True
    try:

        DashboardInfo.objects.get(dashboard_id = section.id)
    except: 
        DashboardInfo.objects.create(dashboard_id = section.id)

    dashboard = DashboardInfo.objects.get(dashboard_id = section.id)
    if request.method == "POST":
        dashboard_info = request.POST['dashboard_info']
        dashboard.info = dashboard_info
    
    dashboard.save()  

    return dict(section=section,
                dashboard=dashboard,
                module=get_module(section),
                modules=root.get_children(),
                root=section.hierarchy.get_root(),
                edit_page = edit_page)


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
        profile = UserProfile.objects.get(user=request.user.id)
        user = User.objects.get(pk=request.user.id)
        form = UserRegistrationForm(initial={
                'username': user.username,
                'email': user.email,
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
        user = User.objects.get(pk=request.user.id)
        form = UserRegistrationForm(initial={
                'username': user.username,
                'email': user.email,
                })
    return dict(form=form, user=user)


@login_required
def update_user_profile(request):
    form = UserRegistrationForm(request.POST)
    user = User.objects.get(pk=request.user.id)
    user.username = form.data["username"]
    if form.data["password1"] != "":
        user.set_password(form.data["password1"])
    try:
        userprofile = UserProfile.objects.get(user=user)
    except:
        userprofile = UserProfile.objects.create(user=user)
    userprofile.sex = form.data["sex"]
    userprofile.age = form.data["age"]
    userprofile.origin = form.data["origin"]
    userprofile.ethnicity = form.data["ethnicity"]
    userprofile.disadvantaged = form.data["disadvantaged"]
    userprofile.employment_location = form.data["employment_location"]
    userprofile.position = form.data["position"]
    userprofile.save()
    user.save()
    return HttpResponseRedirect('/profile/?saved=true/')


@login_required
@render_to('main/dashboard.html')
def dashboard(request):
    h = get_hierarchy("main")
    root = h.get_root()
    last_session = h.get_user_section(request.user)
    dashboard_info = DashboardInfo.objects.all()

    is_visited = user_visits(request)
    empty = ""
    return dict(root=root, last_session=last_session,dashboard_info = dashboard_info,
                empty=empty, is_visited = is_visited)


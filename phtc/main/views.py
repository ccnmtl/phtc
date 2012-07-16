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


def redirect_to_first_section_if_root(section, root):
    if section.id == root.id:
        # trying to visit the root page
        if section.get_next():
            # just send them to the first child
            # users will redirect to their dashboard
            # - if not logged in will goto login page
            return HttpResponseRedirect("/dashboard/")


def update_status(section, user):
    uv = None
    if not user.is_anonymous():
        uv = section.get_uservisit(user)
        if not uv:
            section.user_pagevisit(user, status="incomplete")
        else:
            if uv.status != "complete":
                section.user_pagevisit(user, status="incomplete")
            else:
                # we still want the last_visit time to update
                section.user_pagevisit(user, status="complete")

def user_visits(request):
    visits = UserPageVisit.objects.filter(user_id = request.user)
    return visits

@login_required
@render_to('main/page.html')
def page(request, path):
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    module = get_module(section)
    is_visited = user_visits(request)
    incomplete = "incomplete"
    completed = "completed"
    user_id = request.user.id
    if section.get_previous():
        prev_section_id = Section.objects.get(id = section.get_previous().id )
    
    if not request.user.is_anonymous():
        section.user_visit(request.user)

    rv = redirect_to_first_section_if_root(section, root)
    if rv:
        return rv

    # this needs to test whether it is a feedback or matching section

    if not request.method == "POST":
        for s in module.get_children():
            s.user_pagevisit(request.user, status="complete")
        if module == section:
            section.user_pagevisit(request.user, status="complete")
        else:
            try:
                prev_section_status = UserPageVisit.objects.get(section_id = prev_section_id, user_id = user_id).status
            except:
                prev_section_status = "incomplete"
            
            try:
                sec_status = UserPageVisit.objects.get(section_id = section.id, user_id = user_id).status
            except:
                sec_status = "incomplete"

            if sec_status == "complete":
                sec_status = "complete"
            elif prev_section_status == "incomplete":
                go_back_message = "/dashboard/?incomplete=true"
                return HttpResponseRedirect(go_back_message )
            else:
                section.user_pagevisit(request.user, status="complete")
            #is_allowed = Section.objects.get(id = prev_section.id)

    update_status(section, request.user)

    if request.method == "POST":
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
        return dict(section=section,
                    module=module,
                    is_visited = is_visited,
                    incomplete = incomplete,
                    completed = completed,
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
                root=section.hierarchy.get_root())


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


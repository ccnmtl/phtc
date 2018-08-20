from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from pagetree.helpers import get_section_from_path, get_hierarchy
from pagetree.models import UserPageVisit

from phtc.main.models import DashboardInfo, UserProfile, ModuleType
from phtc.main.models import SectionCss
from django.utils.datastructures import MultiValueDictKeyError


def context_processor(request):
    ctx = {}
    ctx['MEDIA_URL'] = settings.MEDIA_URL
    return ctx


def region2phtc(request):
    # training.lowernysphtc.org site root permanently redirects to region2phtc
    # training.lowernysphtc.org/<modules>/ were given to external train site
    return HttpResponseRedirect('http://region2phtc.org/')


@login_required
@render_to('main/dashboard.html')
def dashboard(request):
    # full module listing available for logged in users
    return dict(
        root=get_hierarchy("main").get_root(),
        dashboard_info=DashboardInfo.objects.all(),
        module_type=ModuleType.objects.all(),
        section_css=SectionCss.objects.all())


def redirect_to_first_section_if_root(section, root):
    if section.id == root.id:
        # trying to visit the root page
        if section.get_next():
            # just send them to the first child
            # users will redirect to their dashboard
            # - if not logged in will goto login page
            return HttpResponseRedirect(reverse("dashboard"))


def make_sure_module1_parts_are_allowed(module, user):

    parts = module.get_children()
    for part in parts:
        v = part.get_uservisit(user)
        if v:
            if (v.status == "in_progress" and
                    part.get_previous().get_uservisit(user)):
                part.get_previous().user_pagevisit(user, status="complete")
            else:
                part.user_pagevisit(user, status="allowed")


def get_userpagevisit_status(section, user):
    try:
        UserPageVisit.objects.get(
            section=section.get_next(), user=user)
        return "exists"
    except UserPageVisit.DoesNotExist:
        return "created"


def make_sure_parts_are_allowed(module, user, section, is_module):
    # handle Module one seperately
    if is_module_one(module):
        make_sure_module1_parts_are_allowed(module, user)

    if not is_module:
        return

    if UserPageVisit.objects.get(
            section=module, user=user).status == "complete":
        module.user_pagevisit(user, status="complete")
        return
    status = get_userpagevisit_status(section, user)
    if status == "exists":
        ns = section.get_next()
        update_next_status(ns, user, "in_progress", "complete")
        update_next_status(ns, user, "allowed", "in_progress")
    if status == "created":
        section.get_next().user_pagevisit(user, status="allowed")


def update_next_status(section, user, current_status, next_status):
    if get_upv_status(section, user) == current_status:
        section.user_pagevisit(user, status=next_status)


def get_upv_status(section, user):
    return UserPageVisit.objects.get(section=section, user=user).status


def part_flagged_as_allowed(upv):
    return upv.status == "allowed" or upv.status == "in_progress"


def is_module_one(module):
    module_one = module.hierarchy.get_root().get_children()[0]
    return module.id == module_one.id


def is_module(module, section):
    return module.id == section.id


def has_user_prof(request):
    try:
        request.user.userprofile
        return True
    except UserProfile.DoesNotExist:
        return False


def is_mod_one(module):
    return (module is not None and
            module == module.hierarchy.get_root().get_children()[0])


@render_to('main/page.html')
def page(request, path):
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    module = section.get_module()
    page_dict = dict(
        section=section,
        module=module,
        modules=root.get_children(),
        root=section.hierarchy.get_root(),
        is_mod_one=is_mod_one(module),
    )

    rv = redirect_to_first_section_if_root(section, root)
    if rv:
        return rv

    if request.method == "POST":
        # giving them feedback before they proceed
        return HttpResponseRedirect(section.get_absolute_url())

    return page_dict


@login_required
@render_to('main/edit_page.html')
def edit_page(request, path):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("dashboard"))
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    edit_page = True
    dashboard, created = DashboardInfo.objects.get_or_create(
        dashboard=section)
    module_type, created = ModuleType.objects.get_or_create(
        module_type=section)

    update_module_type_info(module_type, request)
    section_css, created = SectionCss.objects.get_or_create(
        section_css=section)

    if request.method == "POST":
        try:
            dashboard.info = request.POST['dashboard_info']
        except MultiValueDictKeyError:
            pass
        try:
            section_css.css_field = request.POST['section_css_field']
        except MultiValueDictKeyError:
            pass

    dashboard.save()
    section_css.save()
    module_type.save()

    return dict(section=section,
                section_css=section_css,
                dashboard=dashboard,
                module_type=module_type,
                module=section.get_module(),
                modules=root.get_children(),
                root=section.hierarchy.get_root(),
                edit_page=edit_page)


def update_module_type_info(module_type, request):
    if (request.POST.get('module_type_form') or
            request.POST.get('module_type_form') == ''):
        module_type.info = request.POST.get('module_type_form', '')

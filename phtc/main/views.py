from json import dumps

from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.flatpages.models import FlatPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from pagetree.helpers import get_section_from_path, get_hierarchy

from phtc.main.models import DashboardInfo, UserProfile, ModuleType
from phtc.main.models import SectionCss


def context_processor(request):
    ctx = {}
    ctx['MEDIA_URL'] = settings.MEDIA_URL
    return ctx


def redirect_to_first_section_if_root(section, root):
    if section.id == root.id:
        # trying to visit the root page
        if section.get_next():
            # just send them to the first child
            # users will redirect to their dashboard
            # - if not logged in will goto login page
            return HttpResponseRedirect(reverse("dashboard"))


def page_post(request, section, module):
    '''I guess this will most likely need to be removed'''
    # giving them feedback before they proceed
    return HttpResponseRedirect(section.get_absolute_url())


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
        return page_post(request, section, module)

    # return page
    return page_dict


@login_required
@render_to('main/edit_page.html')
def edit_page(request, path):
    if request.user.is_staff:
        section = get_section_from_path(path)
        root = section.hierarchy.get_root()
        edit_page = True
        dashboard, created = DashboardInfo.objects.get_or_create(
            dashboard=section)

        module_type, created = ModuleType.objects.get_or_create(
            module_type=section)

        if (request.POST.get('module_type_form') or
                request.POST.get('module_type_form') == ''):
            module_type.info = request.POST.get('module_type_form', '')

        section_css, created = SectionCss.objects.get_or_create(
            section_css=section)

        if request.method == "POST":
            try:
                dashboard.info = request.POST['dashboard_info']
            except:
                pass
            try:
                section_css.css_field = request.POST['section_css_field']
            except:
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
    else:
        return HttpResponseRedirect(reverse("dashboard"))


def exporter(request):
    h = get_section_from_path('/').hierarchy
    data = h.as_dict()
    resp = HttpResponse(dumps(data))
    resp['Content-Type'] = 'application/json'
    return resp


@render_to('main/dashboard.html')
def dashboard(request):
    '''I assume if we are getting rid of state, then the only
    users that should be logging in are admins and there should
    not be courses'''
    if request.user.is_anonymous():
        return render_dashboard(request)
    try:
        UserProfile.objects.get(user=request.user).fname
        return render_dashboard(request)
    except UserProfile.DoesNotExist:
        return render_dashboard(request)


@render_to('main/dashboard_panel.html')
def dashboard_panel(request):
    return render_dashboard(request)


def render_dashboard(request):
    try:
        next_path = request.META['HTTP_REFERER']
        if (len(next_path.split('/nylearns/?')[1].split('&')) > 1):
            params = next_path.split('/nylearns/?')[1].split('&')
            if (params[0].split('=')[0] == "course" or
                    params[1].split('=')[0] == "course"):
                url = '/nylearns/?' + params[0] + '&' + params[1]
                return HttpResponseRedirect(url)
    except:
        pass

    h = get_hierarchy("main")
    root = h.get_root()
    dashboard_info = DashboardInfo.objects.all()
    module_type = ModuleType.objects.all()
    section_css = SectionCss.objects.all()
    empty = ""
    return dict(root=root,
                dashboard_info=dashboard_info, empty=empty,
                section_css=section_css,
                module_type=module_type)


@render_to('flatpages/about.html')
def about_page(request):
    page = FlatPage.objects.get(title="About")
    return dict(flatpage=page)


@render_to('flatpages/help.html')
def help_page(request):
    page = FlatPage.objects.get(title="Help")
    return dict(flatpage=page)


@render_to('flatpages/contact.html')
def contact_page(request):
    page = FlatPage.objects.get(title="Contact")
    return dict(flatpage=page)

from json import dumps
from annoying.decorators import render_to
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from pagetree.helpers import get_section_from_path, get_hierarchy
from pagetree.models import Section, UserPageVisit
from phtc.main.forms import UserRegistrationForm
from phtc.main.models import DashboardInfo, UserProfile, ModuleType
from phtc.main.models import SectionCss, NYLEARNS_Course_Map


@render_to('registration/nylearns_registration_form.html')
def nylearns(request):
    form = UserRegistrationForm(initial={
        'is_nylearns': 'True',
        'nylearns_user_id': user_id,
        'nylearns_course_init': course
    })

    if not request.user.is_anonymous():
        course = request.GET.get('course')
        try:
            course_map = NYLEARNS_Course_Map.objects.get(courseID=course)
            url = course_map.phtc_url.split('/')
            # courses must be mapped to first page in module
            course_url = url[1] + '/' + url[2]
            section = get_section_from_path(course_url)
            module = section.get_module()
            process_dashboard_ajax(request.user, section, module)
            return HttpResponseRedirect(course_map.phtc_url)
        except NYLEARNS_Course_Map.DoesNotExist:
            return HttpResponseRedirect(
                '/dashboard/?course_not_available=true')
    else:
        return dict(form=form, args=args)


def redirect_to_first_section_if_root(section, root):
    if section.id == root.id:
        # trying to visit the root page
        if section.get_next():
            # just send them to the first child
            # users will redirect to their dashboard
            # - if not logged in will goto login page
            return HttpResponseRedirect(reverse("dashboard"))


def send_nylearns_email(request, user, profile, module):
    send_to_email = 'edlearn@health.state.ny.us'
    (subject, from_email, to) = (
        'PHTC - NYLearns Notification',
        'NYC-LI-LTC Public Health Training Center <no-reply@lowernysphtc.org>',
        send_to_email)
    text_content = ''
    username = profile.lname + ', ' + profile.fname
    nylearns_userid = profile.nylearns_user_id
    user_email = user.email
    html = get_template('main/nylearns_email.html')
    html_context = Context(
        {
            'username': username,
            'module': module,
            'nylearns_userid': nylearns_userid,
            'user_email': user_email
        })
    html_content = html.render(html_context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_post_test_email(user, section, module, request):
    profile = UserProfile.objects.get(user_id=user.id)
    if profile.is_nylearns:
        send_nylearns_email(request, user, profile, module)

    (subject, from_email, to) = (
        'Public Health Training Certificate',
        'NYC-LI-LTC Public Health Training Center <no-reply@lowernysphtc.org>',
        user.email)
    text_content = ''
    label = module.label
    host = request.get_host()
    abs_url = module.get_absolute_url()
    html = get_template('main/completer_email.html')
    html_context = Context(
        {
            'label': label,
            'host': host,
            'abs_url': abs_url
        })
    html_content = html.render(html_context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def page_post(request, section, module):
    if request.POST.get('post_test') == "true":
        send_post_test_email(request.user, section, module, request)
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
        # forward over to dashboard
        return HttpResponseRedirect(reverse('dashboard'))
    elif request.POST.get('pre_test') == "true":
        # return HttpResponse(request.POST)
        return HttpResponseRedirect(section.get_absolute_url())
    else:
        # giving them feedback before they proceed
        return HttpResponseRedirect(section.get_absolute_url())


def make_sure_module1_parts_are_allowed(module, user):

    parts = module.get_children()
    for part in parts:
        v = part.get_uservisit(user)
        if v:
            if (v.status == "in_progress"
                    and part.get_previous().get_uservisit(user)):
                part.get_previous().user_pagevisit(user, status="complete")
            else:
                part.user_pagevisit(user, status="allowed")


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


@login_required
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


def previous_section_handle_status(section, request, module):
    if section.get_previous():
        prev_section = section.get_previous()
        prev_section_visit = prev_section.get_uservisit(request.user)
        if (prev_section_visit
                and prev_section_visit.status == "in_progress"
                and not is_module(module, prev_section)):
            prev_section.user_pagevisit(request.user, status="complete")
        else:
            # Need to catch whether a part has been flagged as "allowed"
            upv = section.get_uservisit(request.user)
            if upv:
                prev_section_visit = part_flagged_as_allowed(upv)
        # make sure user cannot type in url by hand to skip around
        if not hand_type_secure(prev_section_visit, request, section):
            section.user_pagevisit(request.user, status="incomplete")
            return HttpResponseRedirect("/dashboard/?incomplete=true")


def hand_type_secure(prev_section_visit, request, section):
    if prev_section_visit:
        return True
    if request.user.is_staff:
        section.user_pagevisit(request.user, status="in_progress")
        return True
    return False


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
    # test if the user profile has been completed
    if request.GET and request.GET.get('course_not_available'):
        # return HttpResponseRedirect('/profile/')
        request.META['HTTP_REFERER'] = ''
        '''This tells you the course doesn't exist and you need to select a different one'''
        HttpResponseRedirect('/dashboard/?course_not_available=true')
    try:
        UserProfile.objects.get(user=request.user).fname
        return render_dashboard(request)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/profile/?needs_edit=true/')


@login_required
@render_to('main/dashboard_panel.html')
def dashboard_panel(request):
    return render_dashboard(request)


def render_dashboard(request):
    try:
        next_path = request.META['HTTP_REFERER']
        if (len(next_path.split('/nylearns/?')[1].split('&')) > 1):
            params = next_path.split('/nylearns/?')[1].split('&')
            if (params[0].split('=')[0] == "course"
                    or params[1].split('=')[0] == "course"):
                url = '/nylearns/?' + params[0] + '&' + params[1]
                return HttpResponseRedirect(url)
    except:
        pass

    h = get_hierarchy("main")
    root = h.get_root()
    last_session = h.get_user_section(request.user)
    dashboard_info = DashboardInfo.objects.all()
    module_type = ModuleType.objects.all()
    section_css = SectionCss.objects.all()
    # is_visited = user_visits(request)
    empty = ""
    return dict(root=root, last_session=last_session,
                dashboard_info=dashboard_info, empty=empty,
                section_css=section_css,
                module_type=module_type)


def question_other(question, ev, response_list_count, qr):
    counter = []
    for val in response_list_count:
        for res in ev['responses']:
            response = res.value.strip(
                ' \t\n\r').replace(" ", "_").lower()
            if response == val[0]:
                val = (val[0], val[1] + 1)
        counter.append((question, val[0]))
        counter.append(('# of Responses', val[1]))
    qr.append(counter)
    return qr


def question_please_add(question, ev, qr):
    comments = []
    for i in range(len(ev['responses'])):
        if not ev['responses'][i].value == '':
            comments.append(
                (question, ev['responses'][i].value))
            # keep report uniform
            comments.append(('', ''))
    qr.append(comments)
    return qr


def is_question_of_interest(question, qoi):
    for q in qoi:
        if question.text.strip(' \t\n\r') == q:
            return True


@render_to('flatpages/about.html')
def about_page(request):
    page = FlatPage.objects.get(title="About")
    return dict(flatpage=page)


@render_to('flatpages/help.html')
def help_page(request):
    page = FlatPage.objects.get(title="Help")
    return dict(flatpage=page)


@render_to('flatpages/about.html')
def contact_page(request):
    page = FlatPage.objects.get(title="Contact")
    return dict(flatpage=page)
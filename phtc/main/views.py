from annoying.decorators import render_to
from django.http import HttpResponseRedirect, HttpResponse
from pagetree.helpers import get_section_from_path, get_hierarchy
from pagetree.helpers import get_module, needs_submit, submitted
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.simplejson import dumps
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from phtc.main.models import UserProfile
from phtc.main.forms import UserRegistrationForm
from phtc.main.models import DashboardInfo
from phtc.main.models import ModuleType
from phtc.main.models import SectionCss
from pagetree.models import UserPageVisit
from phtc.main.models import NYLEARNS_Course_Map
from django.core.mail import EmailMultiAlternatives
from django.contrib.flatpages.models import FlatPage
from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import get_template
from django.template import Context
from pagetree.models import Section
from quizblock.models import Quiz
from quizblock.models import Question
from quizblock.models import Response
from quizblock.models import Submission
import csv


@render_to('registration/registration_form.html')
def test_nylearns_username(request):
    if request.POST:
        username = request.POST.get('username')
        try:
            User.objects.get(username=username)
            return HttpResponse(True)
        except User.DoesNotExist:
            return HttpResponse(False)
    else:
        return HttpResponse("POST only")


@render_to('registration/nylearns_registration_form.html')
def nylearns(request):
    user_id = request.GET.get('user_id')
    course = request.GET.get('course')
    args = dict(user_id=user_id, course=course)
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
            #courses must be mapped to first page in module
            course_url = url[1] + '/' + url[2]
            section = get_section_from_path(course_url)
            module = get_module(section)
            process_dashboard_ajax(request.user, section, module)
            return HttpResponseRedirect(course_map.phtc_url)
        except NYLEARNS_Course_Map.DoesNotExist:
            return HttpResponseRedirect(
                '/dashboard/?course_not_available=true')

    if request.method == "POST":
        form = UserRegistrationForm()
        return render_to_response('registration/registration_form.html', form)

    if not request.GET.get('has_account'):
        form = AuthenticationForm()
        return render_to_response(
            'registration/nylearns_login.html',
            {'form': form, 'args': args, 'request': request})
    else:
        return dict(form=form, args=args)


@render_to('registration/nylearns_registration_form.html')
def create_nylearns_user(request):
    if request.POST and request.POST.get('nylearns_course_init'):
        course = request.POST.get('nylearns_course_init')
    else:
        course = 'none'
    if request.POST and request.POST.get('nylearns_user_id'):
        user_id = request.POST.get('nylearns_user_id')
    else:
        user_id = 'none'
    form = UserRegistrationForm(request.POST)
    email = form.data["email"]
    username = form.data["username"]
    password = form.data["password1"]
    args = dict(user_id=user_id, course=course)
    # check if user or email exist and make sure pass is not blank
    if (User.objects.filter(email=email).exists() or
            User.objects.filter(username=username).exists() or
            password == ""):
        return dict(form=form, args=args)

    else:
        user = User.objects.create_user(username, email, password)
        user.save()
        userprofile = UserProfile.objects.create(user=user)

    try:
        userprofile.other_employment_location = form.data[
            "other_employment_location"]
    except:
        pass

    try:
        userprofile.other_position_category = form.data[
            "other_position_category"]
    except:
        pass

    request.user.email = form.data["email"]
    userprofile.is_nylearns = form.data["is_nylearns"]
    userprofile.nylearns_user_id = form.data["nylearns_user_id"]
    userprofile.nylearns_course_init = form.data["nylearns_course_init"]
    userprofile.fname = form.data["fname"]
    userprofile.lname = form.data["lname"]
    userprofile.degree = form.data["degree"]
    userprofile.sex = form.data["sex"]
    userprofile.age = form.data["age"]
    userprofile.origin = form.data["origin"]
    userprofile.ethnicity = form.data["ethnicity"]
    userprofile.degree = form.data["degree"]
    userprofile.work_city = form.data["work_city"]
    userprofile.work_state = form.data["work_state"]
    userprofile.work_zip = form.data["work_zip"]
    userprofile.employment_location = form.data["employment_location"]
    userprofile.umc = form.data["umc"]
    userprofile.position = form.data["position"]
    userprofile.dept_health = form.data["dept_health"]
    userprofile.geo_dept_health = form.data["geo_dept_health"]
    userprofile.experience = form.data["experience"]
    userprofile.rural = form.data["rural"]
    userprofile.save()
    user.is_active = True
    user.save()
    authenticated_user = authenticate(username=username, password=password)
    login(request, authenticated_user)
    return HttpResponseRedirect(
        '/nylearns/?profile_created=true&course=' + course)


@render_to('registration/nylearns_login.html')
def nylearns_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    course = request.GET.get('course')
    user_id = request.GET.get('user_id')
    form = AuthenticationForm(initial={'username': username})
    if request.POST.get('args'):
        args = request.POST.get('args')
    else:
        args = {'course': course, 'user_id': user_id}
    if not request.GET.get('course') == '':
        course = request.GET.get('course')
    else:
        course = 'none'
    if request.method == "POST":
        req = request.POST
        if not req.get('username') == '' and not req.get('password') == '':
            authenticated_user = authenticate(username=username,
                                              password=password)
            try:
                login(request, authenticated_user)
                return HttpResponseRedirect('/nylearns/?course=' + course)
            except:
                pass
    return dict(form=form, errors=True, args=args)


def redirect_to_first_section_if_root(section, root):
    if section.id == root.id:
        # trying to visit the root page
        if section.get_next():
            # just send them to the first child
            # users will redirect to their dashboard
            # - if not logged in will goto login page
            return HttpResponseRedirect(reverse("dashboard"))


def update_status(section, user, module):
    if user.is_anonymous():
        return
    prev_status = False
    prev_section = section.get_previous()
    if prev_section:
        upv = prev_section.get_uservisit(user)
        if upv:
            prev_status = upv.status
    uv = section.get_uservisit(user)
    if not uv and not prev_status:
        return
    if not is_module(module, section):
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
        v = part.get_uservisit(user)
        if v:
            if (v.status == "in_progress"
                    and part.get_previous().get_uservisit(user)):
                part.get_previous().user_pagevisit(user, status="complete")
        else:
            part.user_pagevisit(user, status="allowed")


def make_sure_parts_are_allowed(module, user, section, is_module):
    #handle Module one seperately
    if is_module_one(module):
        make_sure_module1_parts_are_allowed(module, user)
    elif is_module:
        if UserPageVisit.objects.get(
            section=module,
                user=user).status == "complete":
            module.user_pagevisit(user, status="complete")
            return
        try:
            status = "exists"
            UserPageVisit.objects.get(
                section=section.get_next(), user=user)
        except UserPageVisit.DoesNotExist:
            status = "created"

        if status == "exists":
            ns = section.get_next()
            if UserPageVisit.objects.get(
                    section=ns, user=user).status == "in_progress":
                section.get_next().user_pagevisit(user,
                                                  status="complete")
            elif UserPageVisit.objects.get(
                    section=ns,
                    user=user).status == "allowed":
                section.get_next().user_pagevisit(user,
                                                  status="in_progress")
        if status == "created":
            section.get_next().user_pagevisit(
                user, status="allowed")


def part_flagged_as_allowed(upv):
    return upv.status == "allowed" or upv.status == "in_progress"


def is_module_one(module):
    module_one = module.hierarchy.get_root().get_children()[0]
    return module.id == module_one.id


def is_module(module, section):
    return module.id == section.id


def process_dashboard_ajax(user, section, module):
    upv = module.get_uservisit(user)
    if upv and upv.status == "complete":
        if not is_module_one(module):
            for sec in module.get_children():
                sec.user_pagevisit(user, status="complete")
            return reverse("dashboard")
    else:
        module.user_pagevisit(user, status="in_progress")
        make_sure_parts_are_allowed(module, user, section,
                                    is_module(module, section))
        return reverse("dashboard")


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
    if not has_user_prof(request):
        return HttpResponseRedirect("/dashboard/")

    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    module = get_module(section)
    is_visited = user_visits(request)
    page_dict = dict(
        section=section,
        module=module,
        is_visited=is_visited,
        needs_submit=needs_submit(section),
        is_submitted=submitted(section, request.user),
        modules=root.get_children(),
        root=section.hierarchy.get_root(),
        is_mod_one=is_mod_one(module),
    )

    # dashboard ajax
    if request.POST.get('module'):
        return HttpResponse(
            process_dashboard_ajax(request.user, section, module))

    #is the user allowed?
    if request.user.is_anonymous():
        section.user_pagevisit(request.user)

    rv = redirect_to_first_section_if_root(section, root)
    if rv:
        return rv

    # if this is a deep link to the module make sure ro go to dashboard
    # as to not break the locking
    if (request.GET.get('deep_link') and request.GET.get('deep_link') == "true"
            and not(is_module(module, section))):
        return HttpResponseRedirect('/dashboard/')

    # is the page already completed? If so, do not update status
    if(section.get_uservisit(request.user) and
       section.get_uservisit(request.user).status == "complete"):
        return page_dict
    else:
        update_status(section, request.user, module)

    if request.method == "POST":
        return page_post(request, section, module)

    # test if there is a previous section - if so then
    # decide whether to change status
    previous_section_handle_status(section, request, module)

    #return page
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
        form = UserRegistrationForm(
            initial={
                'fname': profile.fname,
                'lname': profile.lname,
                'username': request.user.username,
                'email': request.user.email,
                'sex': profile.sex,
                'age': profile.age,
                'origin': profile.origin,
                'ethnicity': profile.ethnicity,
                'degree': profile.degree,
                'work_city': profile.work_city,
                'work_state': profile.work_state,
                'work_zip': profile.work_zip,
                'umc': profile.umc,
                'employment_location': profile.employment_location,
                'other_employment_location': profile.other_employment_location,
                'position': profile.position,
                'other_position_category': profile.other_position_category,
                'dept_health': profile.dept_health,
                'geo_dept_health': profile.geo_dept_health,
                'experience': profile.experience,
                'rural': profile.rural
            })
        return dict(profile=profile, form=form)
    except UserProfile.DoesNotExist:
        form = UserRegistrationForm(
            initial={
                'username': request.user.username,
                'email': request.user.email,
            })
    return dict(form=form, user=request.user)


@login_required
def update_user_profile(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        request.user.username = form.data["username"]
        if form.data["password1"] != "":
            request.user.set_password(form.data["password1"])
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            userprofile = UserProfile.objects.create(user=request.user)

        try:
            userprofile.other_employment_location = form.data[
                "other_employment_location"]
        except:
            pass

        try:
            userprofile.other_position_category = form.data[
                "other_position_category"]
        except:
            pass
        request.user.email = form.data["email"]
        userprofile.fname = form.data["fname"]
        userprofile.lname = form.data["lname"]
        userprofile.degree = form.data["degree"]
        userprofile.sex = form.data["sex"]
        userprofile.age = form.data["age"]
        userprofile.origin = form.data["origin"]
        userprofile.ethnicity = form.data["ethnicity"]
        userprofile.degree = form.data["degree"]
        userprofile.work_city = form.data["work_city"]
        userprofile.work_state = form.data["work_state"]
        userprofile.work_zip = form.data["work_zip"]
        userprofile.employment_location = form.data["employment_location"]
        userprofile.umc = form.data["umc"]
        userprofile.position = form.data["position"]
        userprofile.dept_health = form.data["dept_health"]
        userprofile.geo_dept_health = form.data["geo_dept_health"]
        userprofile.experience = form.data["experience"]
        userprofile.rural = form.data["rural"]
        userprofile.save()
        request.user.save()
        return HttpResponseRedirect('/profile/?saved=true/')
    else:
        return HttpResponseRedirect('/profile/')


@login_required
@render_to('main/dashboard.html')
def dashboard(request):
    # test if the user profile has been completed
    if request.GET and request.GET.get('course_not_available'):
        #return HttpResponseRedirect('/profile/')
        request.META['HTTP_REFERER'] = ''
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


@login_required
@render_to('main/certificate.html')
def certificate(request, path):
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    module = get_module(section)
    is_visited = user_visits(request)
    # make sure this page is only viewable if the module is completed.
    if (module.get_uservisit(request.user)
            and module.get_uservisit(request.user).status == "complete"):
        return dict(
            section=section,
            module=module,
            is_visited=is_visited,
            needs_submit=needs_submit(section),
            is_submitted=submitted(section, request.user),
            modules=root.get_children(),
            root=section.hierarchy.get_root(),
            user=request.user,
            profile=UserProfile.objects.get(user=request.user),
            date=UserPageVisit.objects.get(user=request.user,
                                           section=module).last_visit
        )
    else:
        return HttpResponseRedirect('/dashboard/')


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
    is_visited = user_visits(request)
    empty = ""
    return dict(root=root, last_session=last_session,
                dashboard_info=dashboard_info, empty=empty,
                is_visited=is_visited, section_css=section_css,
                module_type=module_type)


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


def create_csv_report(request, report, report_name):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        'attachment; filename="' + report_name + '.csv"')
    writer = csv.writer(response)
    header = []
    header_row = report[0]
    for k, v in header_row.iteritems():
        header.append(k)
    writer.writerow(header)

    for row in report:
        data = []
        for k, v in row.iteritems():
            data.append(v)
        writer.writerow(data)
    return response


def create_csv_report2(request, report, report_name):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        'attachment; filename="' + report_name + '.csv"')
    writer = csv.writer(response)

    #write a header row
    header_fields = []
    for row in report[0]:
        header_fields.append(row[0])
    writer.writerow(header_fields)

    for row in report:
        fields = []
        for field in row:
            field_string = field[1]
            if type(field_string) == int:
                field_string = str(field_string)
            try:
                field_string = field_string.encode('utf-8')
            except:
                pass
            field_string = field_string[:10000000]
            fields.append(field_string)

        writer.writerow(fields)
    return response

QOI = [
    'What is your overall assessment of this training?',
    ('I would recommend this course to others.'),
    ('To what extent do you agree or disagree with the '
     'following statement: I can apply the information '
     'I learned in the training in my practice setting.'),
    ('This online training was an effective method for '
     'me to learn this material.'),
    'Approximately how long did it take you to complete the course?',
    ('Please add any additional comments, including '
     'suggestions for improving the course and requests '
     'for future web-based training modules.')
]


@login_required
@render_to('main/reports.html')
def reports(request):
    welcome_msg = "PHTC Reports"
    h = get_hierarchy("main")
    root = h.get_root()
    modules = root.get_children()
    pagevisits = UserPageVisit.objects.all()
    users = UserProfile.objects.all()
    total_number_of_users = len(users)
    attempted_modules = get_all_attempted_modules(root, modules, pagevisits)
    completed_modules = get_all_completed_modules(root, modules, pagevisits)
    if request.method == "POST":

        report = request.POST.get('report')
        ev_report = request.POST.get('eval_report')
        # vars used to create reports
        completed_modules_counted = count_modules_completed(completed_modules)
        completers = create_completers_list(completed_modules)
        if report == "training_env":
            training_env_report = create_training_env_report(
                completers,
                total_number_of_users, completed_modules_counted)
            return create_csv_report2(request, training_env_report, report)

        if report == "user_report_completed":
            user_report_table = create_user_report_table(
                completed_modules, users)
            return create_csv_report2(request, user_report_table, report)

        if report == "user_report_attempted":
            user_report_table = create_user_report_table(
                attempted_modules, users)
            return create_csv_report2(request, user_report_table, report)

        if report == "age_gender_report":
            age_gender = create_age_gender_dict(completers)
            return create_csv_report(request, age_gender, report)

        if report == "course_report":
            pre_test_data = get_pre_test_data(completed_modules, modules)
            post_test_data = get_post_test_data(completed_modules, modules)
            course_report_table = create_course_report_table(completed_modules,
                                                             pre_test_data,
                                                             post_test_data)
            return create_csv_report2(request, course_report_table, report)

        if ev_report:
            return create_ev_report(request, ev_report, completed_modules,
                                    modules)
    return dict(welcome_msg=welcome_msg, modules=modules)


def create_ev_report(request, ev_report, completed_modules, modules):
    mod = Section.objects.get(label=ev_report)
    evaluation_reports = create_eval_report(
        completed_modules, modules, QOI)

    for ev in evaluation_reports:
        if ev['module'] == mod:
            evaluation_report = ev

    try:
        qr = aggregate_responses(evaluation_report)
        flat_report = flatten_response_tables(qr)
        return create_csv_report2(
            request, flat_report, 'evaluation_report')
    except UnboundLocalError:
        return dict(welcome_msg='Report could not be found.',
                    modules=modules)


def flatten_response_tables(qr):
    #set the number of rows in the report
    qr_rows = 0
    for qr_table in qr:
        if qr_rows < len(qr_table):
            qr_rows = len(qr_table)

    flat_report = []
    for row in range(qr_rows):
        report_row = []
        if row % 2 == 0:
            for report in qr:
                try:
                    report_row.append(report[row])
                    report_row.append(report[row+1])
                except:
                    report_row.append(('', ''))
                    report_row.append(('', ''))
            flat_report.append(report_row)
    return flat_report


def aggregate_responses(evaluation_report):
    # create single report
    qr = []

    response_list_count = [
        ('strongly_disagree', 0),
        ('neither_agree_nor_disagree', 0),
        ('disagree', 0),
        ('agree', 0),
        ('strongly_agree', 0)
    ]
    response_time_list_count = [
        ('30_minutes_or_less', 0),
        ('1_hour', 0),
        ('1.5_hours', 0),
        ('2_hours', 0),
        ('2.5_hours', 0),
        ('3_hours', 0),
        ('3.5_hours', 0),
        ('4_hours', 0)
    ]

    for ev in evaluation_report['question_response']:
        question = ev['question'].text.strip(
            ' \t\n\r').replace(" ", "_").lower()

        if question.startswith('approximately_how_long_did'):
            qr = question_approximately_how_long(
                question, response_time_list_count, qr, ev)
        elif question.startswith('please_add'):
            qr = question_please_add(question, ev, qr)
        else:
            qr = question_other(question, ev, response_list_count, qr)
    return qr


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


def question_approximately_how_long(question, response_time_list_count,
                                    qr, ev):
    counter = []
    for val in response_time_list_count:
        for res in ev['responses']:
            response = res.value.strip(
                ' \t\n\r').replace(" ", "_").lower()
            if response == val[0]:
                val = (val[0], val[1] + 1)
        counter.append((question, val[0]))
        counter.append(('# of Responses', val[1]))
    qr.append(counter)
    return qr


def get_pre_test_data(completed_modules, modules):
    module_pre_test_map = []
    quizes = [x for x in Quiz.objects.filter(pre_test="TRUE")]
    pre_tests = [q for q in quizes if q.pageblocks.all().count() > 0]

    for test in pre_tests:
        obj = {}
        get_module(test.pageblock().section)
        obj['quiz_label'] = get_module(test.pageblock().section).label
        obj['submission_set'] = test.submission_set
        module_pre_test_map.append(obj)
    return module_pre_test_map


def get_post_test_data(completed_modules, modules):
    module_post_test_map = []
    quizes = [x for x in Quiz.objects.filter(post_test="TRUE")]
    post_tests = [q for q in quizes if q.pageblocks.all().count() > 0]

    for test in post_tests:
        obj = {}
        get_module(test.pageblock().section)
        obj['quiz_label'] = get_module(test.pageblock().section).label
        obj['submission_set'] = test.submission_set
        module_post_test_map.append(obj)
    return module_post_test_map


def create_eval_report(completed_modules, modules, qoi):
    module_post_test_map = []
    quizes = [x for x in Quiz.objects.filter(post_test="TRUE")]
    post_tests = [q for q in quizes if q.pageblocks.all().count() > 0]

    for t in post_tests:
        # get questions
        questions = Question.objects.filter(quiz_id=t.id)
        obj = {
            'module': t.pageblock().section.get_module(),
            'quiz': t
        }

        qr = []
        for q in questions:
            if is_question_of_interest(q, qoi):
                question_answer = {
                    'question': q,
                    'responses': Response.objects.filter(question_id=q.id)
                }
                qr.append(question_answer)
        obj['question_response'] = qr

        module_post_test_map.append(obj)
    return module_post_test_map


def is_question_of_interest(question, qoi):
    for q in qoi:
        if question.text.strip(' \t\n\r') == q:
            return True


def sort_test_data(test_data, mod):

    qreps = []
    for data in test_data:
        if data['quiz_label'] == mod.section.label:

            for val in data['submission_set'].values():
                if mod.user_id == val['user_id']:
                    uid = str(val['user_id'])
                    qid = str(val['quiz_id'])
                    sub = Submission.objects.extra(
                        where=["user_id=" + uid, "quiz_id=" + qid])
                    subid = str(sub.values()[0]['id'])
                    questions = Question.objects.extra(
                        where=["quiz_id="+qid])

                    for ques in questions:
                        query = Response.objects.extra(
                            where=["question_id=" + str(ques.id),
                                   "submission_id=" + subid])

                        if len(query) > 0:
                            cln_qry_vals = query.values()[0]['value']
                            cln_qry_vals = cln_qry_vals.encode('utf-8',
                                                               'ignore')
                            qreps.append(cln_qry_vals)
                        else:
                            qreps.append('none')
    return qreps


def create_course_report_table(completed_modules, pre_test_data,
                               post_test_data):
    course_table = []
    preq_length = []
    postq_length = []
    for mod in completed_modules:
        course = []
        pre_qreps = sort_test_data(pre_test_data, mod)
        post_qreps = sort_test_data(post_test_data, mod)
        date = UserPageVisit.objects.filter(
            user=mod.user, section=mod.section)
        date = date[len(date)-1].last_visit
        user = UserProfile.objects.get(user_id=mod.user_id)
        preq_length.append(
            dict({'length': len(pre_qreps), 'section': mod.section.label}))
        postq_length.append(
            dict({'length': len(post_qreps), 'section': mod.section.label}))

        course.append(('course_name', mod.section.label))
        course.append(('date_completed', date.strftime("%D")))
        course.append(('username', user.user.username))
        course.append(('email', user.user.email))
        course.append(('first_name', user.fname))
        course.append(('last_name', user.lname))
        course.append(('age', user.age))
        course.append(('gender', user.sex))
        course.append(('hispanic_origin', user.origin))
        course.append(('race', user.ethnicity))
        course.append(('heighest_degree_earned', user.degree))
        course.append(('work_city', user.work_city))
        course.append(('work_state', user.work_state))
        course.append(('work_zip_code', user.work_zip))
        course.append((
            'primary_discipline_specialty', user.position))
        course.append((
            'employment_location', user.employment_location))
        course.append(('work_in_doh', user.dept_health))
        course.append(('target_doh', user.geo_dept_health))
        course.append(('experience_in_pulic_health', user.experience))
        course.append(('muc', user.umc))
        course.append(('rural', user.rural))
        if len(pre_qreps) == 8:
            course.append(('PreQ1', pre_qreps[0]))
            course.append(('PreQ2', pre_qreps[1]))
            course.append(('PreQ3', pre_qreps[2]))
            course.append(('PreQ4', pre_qreps[3]))
            course.append(('PreQ5', pre_qreps[4]))
            course.append(('PreQ6', pre_qreps[5]))
            course.append(('PreQ7', pre_qreps[6]))
            course.append(('PreQ8', pre_qreps[7]))
        else:
            course.append(('PreQ1', 'n/a'))
            course.append(('PreQ2', 'n/a'))
            course.append(('PreQ3', 'n/a'))
            course.append(('PreQ4', 'n/a'))
            course.append(('PreQ5', 'n/a'))
            course.append(('PreQ6', 'n/a'))
            course.append(('PreQ7', 'n/a'))
            course.append(('PreQ8', 'n/a'))
        if len(post_qreps) == 6:
            course.append(('PostQ1', post_qreps[0]))
            course.append(('PostQ2', post_qreps[1]))
            course.append(('PostQ3', post_qreps[2]))
            course.append(('PostQ4', post_qreps[3]))
            course.append(('PostQ5', post_qreps[4]))
            course.append(('PostQ6', post_qreps[5]))
            course.append(('PostQ7', 'n/a'))
            course.append(('PostQ8', 'n/a'))
            course.append(('PostQ9', 'n/a'))
            course.append(('PostQ10', 'n/a'))
            course.append(('PostQ11', 'n/a'))
            course.append(('PostQ12', 'n/a'))
            course.append(('PostQ13', 'n/a'))
            course.append(('PostQ14', 'n/a'))
        elif len(post_qreps) == 14:
            course.append(('PostQ1', post_qreps[0]))
            course.append(('PostQ2', post_qreps[1]))
            course.append(('PostQ3', post_qreps[2]))
            course.append(('PostQ4', post_qreps[3]))
            course.append(('PostQ5', post_qreps[4]))
            course.append(('PostQ6', post_qreps[5]))
            course.append(('PostQ7', post_qreps[6]))
            course.append(('PostQ8', post_qreps[7]))
            course.append(('PostQ9', post_qreps[8]))
            course.append(('PostQ10', post_qreps[9]))
            course.append(('PostQ11', post_qreps[10]))
            course.append(('PostQ12', post_qreps[11]))
            course.append(('PostQ13', post_qreps[12]))
            course.append(('PostQ14', post_qreps[13]))
        else:
            course.append(('PostQ1', 'n/a'))
            course.append(('PostQ2', 'n/a'))
            course.append(('PostQ3', 'n/a'))
            course.append(('PostQ4', 'n/a'))
            course.append(('PostQ5', 'n/a'))
            course.append(('PostQ6', 'n/a'))
            course.append(('PostQ7', 'n/a'))
            course.append(('PostQ8', 'n/a'))
            course.append(('PostQ9', 'n/a'))
            course.append(('PostQ10', 'n/a'))
            course.append(('PostQ11', 'n/a'))
            course.append(('PostQ12', 'n/a'))
            course.append(('PostQ13', 'n/a'))
            course.append(('PostQ14', 'n/a'))

        course_table.append(course)
    return course_table


def create_training_env_report(completers,
                               total_number_of_users,
                               completed_modules_counted):
        table = []
        report = []
        num_of_completers_duplicated = 0
        for mod in completed_modules_counted:
            num_of_completers_duplicated = len(completed_modules_counted)
        report.append(('Total Unique Registered Users', total_number_of_users))
        report.append(
            ('Total Number Completers Unduplicated', len(completers)))
        report.append(
            ('Total Number Completers_duplicated',
                num_of_completers_duplicated))
        table.append(report)
        return table


def get_all_attempted_modules(root, modules, pagevisits):
    attempted_modules = []
    for module in modules:
        for pv in pagevisits:
            if module.id == pv.section_id:
                attempted_modules.append(pv)
    return attempted_modules


def get_all_completed_modules(root, modules, pagevisits):
    completed_modules = []
    for module in modules:
        for pv in pagevisits:
            if module.id == pv.section_id and pv.status == "complete":
                completed_modules.append(pv)
    return completed_modules


def count_modules_completed(completed_modules):
    mod_list = []
    for v in completed_modules:
        mod_list.append(v.section.label.encode("ascii"))
    return mod_list


def create_completers_list(completed_modules):
    completers_list = []
    #create a list map so we only add unduplicated completers
    completer_set = []
    for v in completed_modules:
        completer_set.append(v.user_id)
    completer_set = list(set(completer_set))
    for v in completer_set:
        user = UserProfile.objects.get(user_id=v)
        completers_list.append(user)
    return completers_list


def create_user_report_table(completed_modules, completers):
    completer_objects = []
    for v in completers:
        obj = []
        num_of_courses_completed = 0
        this_user = User.objects.get(id=v.user_id)
        obj.append(('Username', this_user.username))
        obj.append(('Email Address', this_user.email))
        obj.append(('First Name', v.fname))
        obj.append(('Last Name', v.lname))
        obj.append(('Age', v.age))
        obj.append(('Gender', v.sex))
        obj.append(('Hispanic Origin', v.origin))
        obj.append(('Race', v.ethnicity))
        obj.append(('Highest Degree Earned', v.degree))
        obj.append(('Work City', v.work_city))
        obj.append(('Work State', v.work_state))
        obj.append(('Work Zip Code', v.work_zip))
        obj.append(('Work in DOH', v.dept_health))
        obj.append(('Experience in Public Health', v.experience))
        obj.append(('MUC', v.umc))
        obj.append(('Rural', v.rural))

        if v.other_employment_location == '':
            obj.append(('Employment Location', v.employment_location))
        else:
            obj.append(('Employment Location', v.other_employment_location))
        if v.other_position_category == '':
            obj.append(('Primary Discipline/Seciality', v.position))
        else:
            obj.append(('Primary Discipline/Seciality',
                        v.other_position_category))

        #Gather those that have completed more than one module
        for mod in completed_modules:
            try:
                if v.user_id == mod.user_id:
                    num_of_courses_completed += 1
            except AttributeError:
                num_of_courses_completed += 0

        obj.append(('# of courses completed/attempted',
                    num_of_courses_completed))
        completer_objects.append(obj)

    return completer_objects


def create_age_gender_dict(completers):
    items = [
        {
            'Age': 'Under 20',
            'Male': 0,
            'Female': 0,
            'Total': 0
        },
        {
            'Age': '20-29',
            'Male': 0,
            'Female': 0,
            'Total': 0
        },
        {
            'Age': '30-39',
            'Male': 0,
            'Female': 0,
            'Total': 0
        },
        {
            'Age': '40-49',
            'Male': 0,
            'Female': 0,
            'Total': 0
        },
        {
            'Age': '50-59',
            'Male': 0,
            'Female': 0,
            'Total': 0
        },
        {
            'Age': '60 or Older',
            'Male': 0,
            'Female': 0,
            'Total': 0
        },
        {
            'Age': 'Total',
            'Male': 0,
            'Female': 0,
            'Total': 0
        }]
    calculate_age_gender(completers, items)
    return items


def calculate_age_gender(completers, items):
    for completer in completers:
        if completer.age == "Under 20":
            row = 0
            set_row_total(completer, items, row)
            items[row]['Total'] += 1

        if completer.age == "20-29":
            row = 1
            set_row_total(completer, items, row)
            items[row]['Total'] += 1

        if completer.age == "30-39":
            row = 2
            set_row_total(completer, items, row)
            items[row]['Total'] += 1

        if completer.age == "40-49":
            row = 3
            set_row_total(completer, items, row)
            items[row]['Total'] += 1

        if completer.age == "50-59":
            row = 4
            set_row_total(completer, items, row)
            items[row]['Total'] += 1

        if completer.age == "60-69":
            row = 5
            set_row_total(completer, items, row)
            items[row]['Total'] += 1
        # set Totals of male and Female
        items[6]['Total'] += 1
    return items


def set_row_total(completer, items, row):
    if completer.sex == "male":
        items[row]['Male'] += 1
        items[6]['Male'] += 1  # this is the Total row

    if completer.sex == "female":
        items[row]['Female'] += 1
        items[6]['Female'] += 1  # this is the Total row
    return items

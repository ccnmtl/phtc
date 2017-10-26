import csv
from json import dumps

from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import HttpResponseForbidden
from pagetree.helpers import get_section_from_path, get_hierarchy
from pagetree.models import Section
from pagetree.models import UserPageVisit

from phtc.main.models import DashboardInfo, UserProfile, ModuleType
from phtc.main.models import SectionCss
from quizblock.models import Quiz, Question, Response, Submission
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


def exporter(request):
    h = get_section_from_path('/').hierarchy
    data = h.as_dict()
    resp = HttpResponse(dumps(data))
    resp['Content-Type'] = 'application/json'
    return resp


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
    if not request.user.is_staff:
        return HttpResponseForbidden(
                "You must be a staff member to view reports.")

    welcome_msg = "PHTC Reports"
    h = get_hierarchy("main")
    root = h.get_root()
    modules = root.get_children()
    pagevisits = UserPageVisit.objects.all()
    users = UserProfile.objects.all()
    attempted_modules = get_all_attempted_modules(root, modules, pagevisits)
    completed_modules = get_all_completed_modules(root, modules, pagevisits)

    if request.method != "POST":
        return dict(welcome_msg=welcome_msg, modules=modules)

    report = request.POST.get('report')
    ev_report = request.POST.get('eval_report')

    reporters = {
        "training_env": TrainingEnvReporter,
        "user_report_completed": UserReportCompletedReporter,
        "user_report_attempted": UserReportAttemptedReporter,
        "age_gender_report": AgeGenderReporter,
        "course_report": CourseReporter,
    }
    if report in reporters:
        reporter = reporters[report](
            request, completed_modules, attempted_modules,
            users.count(), users, modules)
        return reporter.create_report()

    if ev_report:
        return create_ev_report(request, ev_report, completed_modules,
                                modules)


class BaseReporter(object):
    def __init__(self, request, completed_modules, attempted_modules,
                 total_number_of_users, users, modules):
        self.request = request
        self.total_number_of_users = total_number_of_users
        self.users = users
        self.completed_modules = completed_modules
        self.attempted_modules = attempted_modules
        # vars used to create reports
        self.completed_modules_counted = count_modules_completed(
            completed_modules)
        self.completers = create_completers_list(completed_modules)
        self.modules = modules

    def create_report(self):
        table = self.generate_table()
        f = self.report_function
        return f(self.request, table, self.report)

    @classmethod
    def create_csv_report(cls, request, report, report_name):
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

    @classmethod
    def create_csv_report2(cls, request, report, report_name):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename="' + report_name + '.csv"')
        writer = csv.writer(response)

        # write a header row
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
                except UnicodeEncodeError:
                    pass
                field_string = field_string[:10000000]
                fields.append(field_string)

            writer.writerow(fields)
        return response


class TrainingEnvReporter(BaseReporter):
    report = "training_env"
    report_function = BaseReporter.create_csv_report2

    def generate_table(self):
        return create_training_env_report(
            self.completers,
            self.total_number_of_users,
            self.completed_modules_counted)


class UserReportCompletedReporter(BaseReporter):
    report = "user_report_completed"
    report_function = BaseReporter.create_csv_report2

    def generate_table(self):
        return create_user_report_table(self.completed_modules, self.users)


class UserReportAttemptedReporter(BaseReporter):
    report = "user_report_attempted"
    report_function = BaseReporter.create_csv_report2

    def generate_table(self):
        return create_user_report_table(self.attempted_modules, self.users)


class AgeGenderReporter(BaseReporter):
    report = "age_gender_report"
    report_function = BaseReporter.create_csv_report

    def generate_table(self):
        return create_age_gender_dict(self.completers)


class CourseReporter(BaseReporter):
    report = "course_report"
    report_function = BaseReporter.create_csv_report2

    def generate_table(self):
        pre_test_data = get_pre_test_data(self.completed_modules, self.modules)
        post_test_data = get_post_test_data(self.completed_modules,
                                            self.modules)
        return create_course_report_table(self.completed_modules,
                                          pre_test_data, post_test_data)


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
        return BaseReporter.create_csv_report2(
            request, flat_report, 'evaluation_report')
    except UnboundLocalError:
        return dict(welcome_msg='Report could not be found.',
                    modules=modules)


def flatten_response_tables(qr):
    # set the number of rows in the report
    qr_rows = get_qr_rows(qr)

    flat_report = []
    for row in range(qr_rows):
        report_row = []
        if row % 2 == 0:
            for report in qr:
                try:
                    report_row.append(report[row])
                    report_row.append(report[row+1])
                except (IndexError, KeyError):
                    report_row.append(('', ''))
                    report_row.append(('', ''))
            flat_report.append(report_row)
    return flat_report


def get_qr_rows(qr):
    qr_rows = 0
    for qr_table in qr:
        if qr_rows < len(qr_table):
            qr_rows = len(qr_table)
    return qr_rows


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
    quizes = [x for x in Quiz.objects.filter(pre_test=True)]
    pre_tests = [q for q in quizes if q.pageblocks.all().count() > 0]

    for test in pre_tests:
        obj = {}
        test.pageblock().section.get_module()
        obj['quiz_label'] = test.pageblock().section.get_module().label
        obj['submission_set'] = test.submission_set
        module_pre_test_map.append(obj)
    return module_pre_test_map


def get_post_test_data(completed_modules, modules):
    module_post_test_map = []
    quizes = [x for x in Quiz.objects.filter(post_test=True)]
    post_tests = [q for q in quizes if q.pageblocks.all().count() > 0]

    for test in post_tests:
        obj = {}
        test.pageblock().section.get_module()
        obj['quiz_label'] = test.pageblock().section.get_module().label
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
    # create a list map so we only add unduplicated completers
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
        obj.append(('Employment Location', get_employment_location(v)))
        obj.append(('Primary Discipline/Seciality', get_position(v)))

        # Gather those that have completed more than one module
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


def get_employment_location(v):
    if v.other_employment_location == '':
        return v.employment_location
    else:
        return v.other_employment_location


def get_position(v):
    if v.other_position_category == '':
        return v.position
    else:
        return v.other_position_category


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
    ranges_to_row = [
        ("Under 20", 0),
        ("20-29", 1),
        ("30-39", 2),
        ("40-49", 3),
        ("50-59", 4),
        ("60-69", 5),
    ]
    for completer in completers:
        for age_range, row in ranges_to_row:
            if completer.age == age_range:
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

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from phtc.main.models import UserProfile
from pagetree.models import Hierarchy
from phtc.main.views import set_row_total
from phtc.main.views import calculate_age_gender
from phtc.main.views import create_age_gender_dict
from phtc.main.views import calculate_status
from phtc.main.views import get_pre_test_data
from phtc.main.views import get_post_test_data
from phtc.main.views import create_eval_report
from phtc.main.views import create_training_env_report
from phtc.main.views import create_user_report_table
from .test_models import FakeRequest
from phtc.main.models import user_created


class SimpleViewTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_index(self):
        result = self.c.get("/")
        self.assertEqual(result.status_code, 302)

    def test_testnylearns_username(self):
        result = self.c.post("/test_nylearns_username/", dict(username="foo"))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, "False")

        result = self.c.get("/test_nylearns_username/?username=foo")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, "POST only")

    def test_nylearns(self):
        result = self.c.get("/nylearns/")
        self.assertEqual(result.status_code, 200)

    def test_nylearns_post(self):
        result = self.c.post("/nylearns/")
        self.assertEqual(result.status_code, 200)

    def test_create_nylearns_user(self):
        result = self.c.post(
            "/create_nylearns_user/",
            dict(
                username="test",
                password1="test",
                email="test@example.com",
                is_nylearns="is_nylearns",
                nylearns_user_id="nylearns_user_id",
                nylearns_course_init="nylearns_course_init",
                fname="fname",
                lname="lname",
                degree="degree",
                sex="sex",
                age="age",
                origin="origin",
                ethnicity="ethnicity",
                work_city="work_city",
                work_state="work_state",
                work_zip="work_zip",
                employment_location="employment_location",
                umc="umc",
                position="position",
                dept_health="dept_health",
                geo_dept_health="geo_dept_health",
                experience="experience",
                rural="rural",
            )
        )
        self.assertEqual(result.status_code, 302)

    def test_nylearns_login(self):
        result = self.c.post(
            "/nylearns_login/?course=none&user_id=foo",
            dict(username="test", password="test"))
        self.assertEqual(result.status_code, 200)


class LoggedInTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create(username="test")
        self.user.set_password("test")
        self.user.save()
        self.c.login(username="test", password="test")

    def test_testnylearns_username(self):
        result = self.c.post("/test_nylearns_username/", dict(username="test"))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, "True")

    def test_nylearns(self):
        result = self.c.get("/nylearns/")
        # logged in, we get redirected to course map or dashboard
        self.assertEqual(result.status_code, 302)

    def test_get_profile(self):
        result = self.c.get("/profile/")
        self.assertEqual(result.status_code, 200)

    def test_reports(self):
        result = self.c.get("/reports/")
        self.assertEqual(result.status_code, 200)

    def test_reports_training_env(self):
        result = self.c.post(
            "/reports/",
            dict(report="training_env")
        )
        self.assertEqual(result.status_code, 200)

    def test_reports_age_gender_report(self):
        result = self.c.post(
            "/reports/",
            dict(report="age_gender_report")
        )
        self.assertEqual(result.status_code, 200)

    def test_dashboard(self):
        result = self.c.get("/dashboard/")
        self.assertEqual(result.status_code, 302)

    def test_dashboard_panel(self):
        result = self.c.get("/dashboard_panel/")
        self.assertEqual(result.status_code, 200)

    def test_page(self):
        UserProfile.objects.create(user=self.user)
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.c.get("/socialwork/introduction/")
        self.assertEqual(r.status_code, 200)

    def test_page_with_prev(self):
        UserProfile.objects.create(user=self.user)
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"},
                          {'label': "Four", 'slug': "second"},
                          ]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.c.get("/socialwork/second/")
        self.assertEqual(r.status_code, 200)

    def test_page_root(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.c.get("/")
        self.assertEqual(r.status_code, 302)

    def test_page_post(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.c.post("/socialwork/introduction/")
        self.assertEqual(r.status_code, 302)

    def test_page_post_then_visit(self):
        UserProfile.objects.create(user=self.user)
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.c.post("/socialwork/introduction/")
        self.assertEqual(r.status_code, 302)
        r = self.c.post("/socialwork/introduction/")
        self.assertEqual(r.status_code, 200)

    def test_page_post_reset(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.c.post("/socialwork/introduction/", dict(action='reset'))
        self.assertEqual(r.status_code, 302)

    def test_page_post_post_test(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        req = FakeRequest()
        user_created(None, self.user, req)
        r = self.c.post("/socialwork/introduction/", dict(post_test='true'))
        self.assertEqual(r.status_code, 302)

    def test_page_post_pre_test(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})

        r = self.c.post("/socialwork/introduction/", dict(pre_test='true'))
        self.assertEqual(r.status_code, 302)

    def test_edit_page(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.c.get("/edit/socialwork/introduction/")
        self.assertEqual(r.status_code, 302)
        self.user.is_staff = True
        self.user.save()
        r = self.c.get("/edit/socialwork/introduction/")
        self.assertEqual(r.status_code, 200)

        r = self.c.post(
            "/edit/socialwork/introduction/",
            dict(module_type_form='')
        )
        self.assertEqual(r.status_code, 200)
        r = self.c.post(
            "/edit/socialwork/introduction/",
            dict(dashboard_info="foo",
                 section_css_field="bar")
        )
        self.assertEqual(r.status_code, 200)

    def test_update_profile(self):
        d = dict(
            username="testuser",
            password1="",
            other_employment_location="foo",
            email="foo@example.com",
            fname="fname",
            lname="lname",
            degree="none",
            sex="F",
            age="old",
            origin="void",
            ethnicity="void",
            work_city="NYC",
            work_state="NY",
            work_zip="10025",
            employment_location="NYC",
            umc="",
            position="",
            dept_health="",
            geo_dept_health="",
            experience="",
            rural="",
        )
        r = self.c.post("/update_profile/", d)
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/profile/")
        self.assertEqual(r.status_code, 200)
        # submit again to catch the "profile already exists" case
        r = self.c.post("/update_profile/", d)
        self.assertEqual(r.status_code, 302)

    def test_certificate_incomplete(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.c.get("/certificate/socialwork/introduction/")
        self.assertEqual(r.status_code, 302)


class FakeCompleter(object):
    def __init__(self, sex="male", age="Under 20"):
        self.sex = sex
        self.age = age


class TestUtilFunctions(TestCase):
    def test_set_row_total(self):
        completer = FakeCompleter()
        items = {
            0: dict(Male=0, Female=0),
            6: dict(Male=0, Female=0)
        }
        r = set_row_total(completer, items, 0)
        self.assertEqual(r[0]['Male'], 1)
        self.assertEqual(r[6]['Male'], 1)
        self.assertEqual(r[0]['Female'], 0)
        self.assertEqual(r[6]['Female'], 0)
        completer.sex = "female"
        items = {
            0: dict(Male=0, Female=0),
            6: dict(Male=0, Female=0)
        }
        r = set_row_total(completer, items, 0)
        self.assertEqual(r[0]['Male'], 0)
        self.assertEqual(r[6]['Male'], 0)
        self.assertEqual(r[0]['Female'], 1)
        self.assertEqual(r[6]['Female'], 1)

    def test_calculate_age_gender(self):
        completers = [
            FakeCompleter(),
            FakeCompleter(sex="female"),
            FakeCompleter(age="20-29"),
            FakeCompleter(age="30-39"),
            FakeCompleter(age="40-49"),
            FakeCompleter(age="50-59"),
            FakeCompleter(age="60-69"),
        ]
        items = [
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
        ]
        r = calculate_age_gender(completers, items)
        self.assertEqual(r[0]['Male'], 1)
        self.assertEqual(r[0]['Female'], 1)
        self.assertEqual(r[0]['Total'], 2)

        self.assertEqual(r[1]['Male'], 1)
        self.assertEqual(r[1]['Female'], 0)
        self.assertEqual(r[1]['Total'], 1)

        self.assertEqual(r[2]['Male'], 1)
        self.assertEqual(r[2]['Female'], 0)
        self.assertEqual(r[2]['Total'], 1)

        self.assertEqual(r[3]['Male'], 1)
        self.assertEqual(r[3]['Female'], 0)
        self.assertEqual(r[3]['Total'], 1)

        self.assertEqual(r[4]['Male'], 1)
        self.assertEqual(r[4]['Female'], 0)
        self.assertEqual(r[4]['Total'], 1)

        self.assertEqual(r[5]['Male'], 1)
        self.assertEqual(r[5]['Female'], 0)
        self.assertEqual(r[5]['Total'], 1)

        self.assertEqual(r[6]['Male'], 6)
        self.assertEqual(r[6]['Female'], 1)
        self.assertEqual(r[6]['Total'], 7)

    def test_create_age_gender_dict(self):
        completers = [
            FakeCompleter(),
            FakeCompleter(sex="female"),
            FakeCompleter(age="20-29"),
            FakeCompleter(age="30-39"),
            FakeCompleter(age="40-49"),
            FakeCompleter(age="50-59"),
            FakeCompleter(age="60-69"),
        ]
        r = create_age_gender_dict(completers)
        self.assertEqual(r[0]['Male'], 1)
        self.assertEqual(r[0]['Female'], 1)
        self.assertEqual(r[0]['Total'], 2)

        self.assertEqual(r[1]['Male'], 1)
        self.assertEqual(r[1]['Female'], 0)
        self.assertEqual(r[1]['Total'], 1)

        self.assertEqual(r[2]['Male'], 1)
        self.assertEqual(r[2]['Female'], 0)
        self.assertEqual(r[2]['Total'], 1)

        self.assertEqual(r[3]['Male'], 1)
        self.assertEqual(r[3]['Female'], 0)
        self.assertEqual(r[3]['Total'], 1)

        self.assertEqual(r[4]['Male'], 1)
        self.assertEqual(r[4]['Female'], 0)
        self.assertEqual(r[4]['Total'], 1)

        self.assertEqual(r[5]['Male'], 1)
        self.assertEqual(r[5]['Female'], 0)
        self.assertEqual(r[5]['Total'], 1)

        self.assertEqual(r[6]['Male'], 6)
        self.assertEqual(r[6]['Female'], 1)
        self.assertEqual(r[6]['Total'], 7)


class CalculateStatusTest(TestCase):
    def test_uv_case(self):

        class UV(object):
            def __init__(self, s="complete"):
                self.status = s

        self.assertEqual(calculate_status("complete", UV()), "in_progress")
        self.assertEqual(calculate_status("in_progress", UV()), "in_progress")
        self.assertEqual(calculate_status("foo", UV("allowed")), "in_progress")
        self.assertEqual(calculate_status("foo", UV("in_progress")),
                         "in_progress")
        self.assertEqual(calculate_status("foo", UV()), "complete")
        self.assertEqual(calculate_status("foo", UV("foo")), "incomplete")

    def test_uv_else(self):
        self.assertEqual(calculate_status("in_progress", None), "in_progress")
        self.assertEqual(calculate_status("foo", None), "incomplete")


class PreTestDataTest(TestCase):
    def test_empty(self):
        result = get_pre_test_data([], [])
        self.assertEqual(result, [])


class PostTestDataTest(TestCase):
    def test_empty(self):
        result = get_post_test_data([], [])
        self.assertEqual(result, [])


class CreateEvalReportTest(TestCase):
    def test_create_eval_report_empty(self):
        result = create_eval_report([], [], [])
        self.assertEqual(result, [])


class CreateTrainingEnvReportTest(TestCase):
    def test_create_training_env_report_empty(self):
        result = create_training_env_report([], 0, [])
        self.assertEqual(result[0][0],
                         ('Total Unique Registered Users', 0))
        self.assertEqual(result[0][1],
                         ('Total Number Completers Unduplicated', 0))
        self.assertEqual(result[0][2],
                         ('Total Number Completers_duplicated', 0))


class CreateUserReportTableTest(TestCase):
    def test_create_user_report_table_empty(self):
        result = create_user_report_table([], [])
        self.assertEqual(result, [])

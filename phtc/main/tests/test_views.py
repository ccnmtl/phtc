from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client, RequestFactory
from pagetree.models import Hierarchy, UserPageVisit

from phtc.main.models import UserProfile
from phtc.main.views import TrainingEnvReporter, UserReportCompletedReporter, \
    UserReportAttemptedReporter, AgeGenderReporter, CourseReporter


class SimpleViewTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_index(self):
        result = self.c.get("/")
        self.assertEqual(result.status_code, 302)


class LoggedInTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create(username="test", is_staff=True)
        self.user.set_password("test")
        self.user.save()
        self.c.login(username="test", password="test")

    def test_dashboard(self):
        result = self.c.get("/dashboard/")
        self.assertEqual(result.status_code, 200)

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

    def test_page_root(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.c.get("/")
        self.assertEqual(r.status_code, 200)

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

    def test_edit_page(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.c.get("/edit/socialwork/introduction/")
        self.assertEqual(r.status_code, 200)
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


class ReportTest(TestCase):
    def setUp(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        self.sections = root.get_children()

        user = User.objects.create(username="test")
        self.profile = UserProfile.objects.create(user=user)
        self.completed = []
        for section in self.sections:
            uv = UserPageVisit.objects.create(
                user=user, status='complete', section=section)
            self.completed.append(uv)

    def test_reporters(self):
        reporters = {
            "training_env": TrainingEnvReporter,
            "user_report_completed": UserReportCompletedReporter,
            "user_report_attempted": UserReportAttemptedReporter,
            "age_gender_report": AgeGenderReporter,
            "course_report": CourseReporter,
        }
        request = RequestFactory()
        for reporter in reporters:
            reporter = reporters[reporter](
                request, self.completed, [], 1, [self.profile], self.sections)
            response = reporter.create_report()
            self.assertEquals(response.status_code, 200)

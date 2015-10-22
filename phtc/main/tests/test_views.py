from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from phtc.main.models import UserProfile
from pagetree.models import Hierarchy


class SimpleViewTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_index(self):
        result = self.c.get("/")
        self.assertEqual(result.status_code, 200)


class LoggedInTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create(username="test")
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

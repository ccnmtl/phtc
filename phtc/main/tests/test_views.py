from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from pagetree.models import Hierarchy

from phtc.main.models import UserProfile


class SimpleViewTest(TestCase):
    def test_index(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 302)


class LoggedOutTest(TestCase):
    def test_root(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 302)
        self.assertEquals(r.url, 'http://region2phtc.org/')

    def test_dashboard(self):
        r = self.client.get(reverse('dashboard'))
        self.assertEqual(r.status_code, 302)
        self.assertEquals(r.url,
                          '/accounts/login/?next=/dashboard/')

    def test_page(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.client.get("/socialwork/introduction/")
        self.assertEqual(r.status_code, 200)


class LoggedInTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", is_staff=True)
        self.user.set_password("test")
        self.user.save()
        self.client.login(username="test", password="test")

    def test_root(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 302)
        self.assertEquals(r.url, 'http://region2phtc.org/')

    def test_dashboard(self):
        result = self.client.get(reverse('dashboard'))
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
        r = self.client.get("/socialwork/introduction/")
        self.assertEqual(r.status_code, 200)

    def test_page_post(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.client.post("/socialwork/introduction/")
        self.assertEqual(r.status_code, 302)

    def test_edit_page(self):
        h = Hierarchy.objects.create(name="main", base_url="/")
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        r = self.client.get("/edit/socialwork/introduction/")
        self.assertEqual(r.status_code, 200)
        self.user.is_staff = True
        self.user.save()
        r = self.client.get("/edit/socialwork/introduction/")
        self.assertEqual(r.status_code, 200)

        r = self.client.post(
            "/edit/socialwork/introduction/",
            dict(module_type_form='')
        )
        self.assertEqual(r.status_code, 200)
        r = self.client.post(
            "/edit/socialwork/introduction/",
            dict(dashboard_info="foo",
                 section_css_field="bar")
        )
        self.assertEqual(r.status_code, 200)

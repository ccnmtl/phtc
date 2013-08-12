from django.test import TestCase
from django.contrib.auth.models import User
from phtc.main.models import DashboardInfo, NYLEARNS_Course_Map
from phtc.main.models import ModuleType, SectionCss, user_created
from phtc.main.models import UserProfile
from pagetree.models import Hierarchy


class DashboardInfoTest(TestCase):
    def test_edit_form(self):
        h = Hierarchy.from_dict({'name': 'main', 'base_url': ""})
        root = h.get_root()
        d = DashboardInfo.objects.create(dashboard=root, info="")
        f = d.edit_form()
        self.assertTrue(f is not None)


class NYLEARNS_Course_MapTest(TestCase):
    def test_unicode(self):
        ncm = NYLEARNS_Course_Map.objects.create(
            courseID="foo", phtc_url="bar")
        self.assertEqual(str(ncm), "url path:bar")


class ModuleTypeTest(TestCase):
    def test_edit_form(self):
        h = Hierarchy.from_dict({'name': 'main', 'base_url': ""})
        root = h.get_root()
        m = ModuleType.objects.create(module_type=root, info="")
        self.assertTrue(m.edit_form() is not None)


class SectionCssTest(TestCase):
    def test_edit_form(self):
        h = Hierarchy.from_dict({'name': 'main', 'base_url': ""})
        root = h.get_root()
        sc = SectionCss.objects.create(section_css=root, css_field="")
        self.assertTrue(sc.edit_form() is not None)


class FakeRequest(object):
    POST = dict(
        fname="test",
        lname="user",
        work_city="new york",
        work_state="ny",
        work_zip="10027",
        sex="M",
        age="21",
        origin="space",
        ethnicity="orange",
        umc="umc",
        employment_location="employment_location",
        position="position",
        dept_health="dept_health",
        geo_dept_health="geo_dept_health",
        experience="experience",
        rural="rural",
        degree="degree",
        nylearns_course_init="nylearns_course_init",
        nylearns_user_id="nylearns_user_id",
    )


class UserCreatedTest(TestCase):
    def test_user_created(self):
        sender = None
        user = User.objects.create(username="testuser")
        req = FakeRequest()
        user_created(sender, user, req)
        up = UserProfile.objects.get(user=user)
        self.assertEqual(str(up), "testuser's profile")

    def test_user_created_optional_fields(self):
        sender = None
        user = User.objects.create(username="testuser")
        req = FakeRequest()
        req.POST["other_position_category"] = "other position"
        req.POST["other_location"] = "other location"
        user_created(sender, user, req)
        up = UserProfile.objects.get(user=user)
        self.assertEqual(str(up), "testuser's profile")

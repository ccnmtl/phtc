from django.test import TestCase
from phtc.main.models import DashboardInfo, NYLEARNS_Course_Map
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

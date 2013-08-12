from django.test import TestCase
from phtc.main.models import DashboardInfo
from pagetree.models import Hierarchy


class DashboardInfoTest(TestCase):
    def test_edit_form(self):
        h = Hierarchy.from_dict({'name': 'main', 'base_url': ""})
        root = h.get_root()
        d = DashboardInfo.objects.create(dashboard=root, info="")
        f = d.edit_form()
        self.assertTrue(f is not None)

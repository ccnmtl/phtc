from django.test import TestCase
from phtc.treatment_activity.models import TreatmentNode, TreatmentPath
from phtc.treatment_activity.models import TreatmentActivityBlock


class TreatmentNodeTest(TestCase):
    def test_unicode(self):
        tn = TreatmentNode.add_root(name="foo", type="RT")
        self.assertEqual(str(tn), "  foo")
        tn.duration = 10
        self.assertEqual(str(tn), "  10 weeks: foo")
        tn2 = tn.add_child(name="bar", type="DP")
        self.assertEqual(str(tn2), "  Decision Point: bar")

    def test_to_json(self):
        tn = TreatmentNode.add_root(name="foo", type="RT")
        tn2 = tn.add_child(name="bar", type="DP")
        self.assertEqual(
            tn.to_json(),
            {
                'id': tn.id,
                'name': "foo",
                'type': "RT",
                'text': None,
                'help': None,
                'duration': 0,
                'value': 0,
                'children_list': [{'name': "bar", 'id': tn2.id, 'value': 0}]
            }
        )


class TreatmentPathTest(TestCase):
    def test_unicode(self):
        tn = TreatmentNode.add_root(name="foo", type="RT")
        tp = TreatmentPath.objects.create(
            tree=tn, name="testpath",
            cirrhosis=False, treatment_status=1,
            drug_choice='telaprevir')
        self.assertEqual(str(tp), "testpath")


class TreatmentActivityBlockTest(TestCase):
    def test_needs_submit(self):
        tab = TreatmentActivityBlock.objects.create()
        self.assertFalse(tab.needs_submit())

    def test_add_form(self):
        f = TreatmentActivityBlock.add_form()
        self.assertTrue(hasattr(f, 'fields'))

    def test_edit_form(self):
        tab = TreatmentActivityBlock.objects.create()
        f = tab.edit_form()
        self.assertTrue(hasattr(f, 'fields'))

    def test_unlocked(self):
        tab = TreatmentActivityBlock.objects.create()
        self.assertTrue(tab.unlocked(None))

    def test_edit(self):
        tab = TreatmentActivityBlock.objects.create()
        tab.edit(dict(), None)

    def test_treatment_paths(self):
        tab = TreatmentActivityBlock.objects.create()
        self.assertEqual(list(tab.treatment_paths()), [])

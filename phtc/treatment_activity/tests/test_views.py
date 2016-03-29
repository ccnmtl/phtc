from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from phtc.treatment_activity.models import TreatmentNode, TreatmentPath


class BasicTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def test_get_next_steps_not_ajax(self):
        r = self.c.get("/_rgt/1/2/")
        self.assertEqual(r.status_code, 403)

    def test_get_next_steps(self):
        tn = TreatmentNode.add_root(name="foo", type="RT")
        tn2 = tn.add_child(name="bar", type="ST")
        tn2.add_child(name="bar", type="ST")
        r = self.c.post(
            "/_rgt/1/%d/" % tn2.id,
            dict(steps=[]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)

    def test_get_next_steps_dp(self):
        tn = TreatmentNode.add_root(name="foo", type="RT")
        tn2 = tn.add_child(name="bar", type="DP")
        tn2.add_child(name="bar", type="ST")
        tn2.add_child(name="bar", type="DP")
        r = self.c.post(
            "/_rgt/1/%d/" % tn2.id,
            dict(steps="[{\"decision\":1}]"),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)

    def test_choose_treatment_path(self):
        tn = TreatmentNode.add_root(name="foo", type="RT")
        tn2 = tn.add_child(name="bar", type="ST")
        tn2.add_child(name="bar", type="ST")
        TreatmentPath.objects.create(
            tree=tn, name="testpath",
            cirrhosis=False, treatment_status=1,
            drug_choice='telaprevir')
        r = self.c.post(
            "/_rgt/",
            dict(steps="[{\"decision\":1}]"),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)

    def test_choose_treatment_path_get(self):
        r = self.c.get("/_rgt/")
        self.assertEqual(r.status_code, 403)

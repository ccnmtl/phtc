from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from phtc.logic_model.models import GamePhase, ActivePhase, Column


class BasicTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def test_settings_get(self):
        response = self.c.get("/_logic_model/settings/")
        self.assertEquals(response.status_code, 200)

    def test_settings_post_no_aps(self):
        response = self.c.post(
            "/_logic_model/settings/",
            {},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEquals(response.status_code, 200)

    def test_settings_post_populated(self):
        gp = GamePhase.objects.create()
        c = Column.objects.create()
        gp2 = GamePhase.objects.create()
        ActivePhase.objects.create(game_phase=gp, column=c)
        ActivePhase.objects.create(game_phase=gp2, column=c)
        response = self.c.post(
            "/_logic_model/settings/",
            {},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEquals(response.status_code, 200)

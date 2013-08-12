from django.test import TestCase
from django.test.client import Client
from phtc.main.views import set_row_total


class SimpleViewTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_index(self):
        result = self.c.get("/")
        self.assertEqual(result.status_code, 302)


class FakeCompleter(object):
    sex = "male"


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

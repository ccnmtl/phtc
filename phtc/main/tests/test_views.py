from django.test import TestCase
from django.test.client import Client
from phtc.main.views import set_row_total
from phtc.main.views import calculate_age_gender
from phtc.main.views import create_age_gender_dict


class SimpleViewTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_index(self):
        result = self.c.get("/")
        self.assertEqual(result.status_code, 302)


class FakeCompleter(object):
    def __init__(self, sex="male", age="Under 20"):
        self.sex = sex
        self.age = age


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

    def test_calculate_age_gender(self):
        completers = [
            FakeCompleter(),
            FakeCompleter(sex="female"),
            FakeCompleter(age="20-29"),
            FakeCompleter(age="30-39"),
            FakeCompleter(age="40-49"),
            FakeCompleter(age="50-59"),
            FakeCompleter(age="60-69"),
        ]
        items = [
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
            dict(Male=0, Female=0, Total=0),
        ]
        r = calculate_age_gender(completers, items)
        self.assertEqual(r[0]['Male'], 1)
        self.assertEqual(r[0]['Female'], 1)
        self.assertEqual(r[0]['Total'], 2)

        self.assertEqual(r[1]['Male'], 1)
        self.assertEqual(r[1]['Female'], 0)
        self.assertEqual(r[1]['Total'], 1)

        self.assertEqual(r[2]['Male'], 1)
        self.assertEqual(r[2]['Female'], 0)
        self.assertEqual(r[2]['Total'], 1)

        self.assertEqual(r[3]['Male'], 1)
        self.assertEqual(r[3]['Female'], 0)
        self.assertEqual(r[3]['Total'], 1)

        self.assertEqual(r[4]['Male'], 1)
        self.assertEqual(r[4]['Female'], 0)
        self.assertEqual(r[4]['Total'], 1)

        self.assertEqual(r[5]['Male'], 1)
        self.assertEqual(r[5]['Female'], 0)
        self.assertEqual(r[5]['Total'], 1)

        self.assertEqual(r[6]['Male'], 6)
        self.assertEqual(r[6]['Female'], 1)
        self.assertEqual(r[6]['Total'], 7)

    def test_create_age_gender_dict(self):
        completers = [
            FakeCompleter(),
            FakeCompleter(sex="female"),
            FakeCompleter(age="20-29"),
            FakeCompleter(age="30-39"),
            FakeCompleter(age="40-49"),
            FakeCompleter(age="50-59"),
            FakeCompleter(age="60-69"),
        ]
        r = create_age_gender_dict(completers)
        self.assertEqual(r[0]['Male'], 1)
        self.assertEqual(r[0]['Female'], 1)
        self.assertEqual(r[0]['Total'], 2)

        self.assertEqual(r[1]['Male'], 1)
        self.assertEqual(r[1]['Female'], 0)
        self.assertEqual(r[1]['Total'], 1)

        self.assertEqual(r[2]['Male'], 1)
        self.assertEqual(r[2]['Female'], 0)
        self.assertEqual(r[2]['Total'], 1)

        self.assertEqual(r[3]['Male'], 1)
        self.assertEqual(r[3]['Female'], 0)
        self.assertEqual(r[3]['Total'], 1)

        self.assertEqual(r[4]['Male'], 1)
        self.assertEqual(r[4]['Female'], 0)
        self.assertEqual(r[4]['Total'], 1)

        self.assertEqual(r[5]['Male'], 1)
        self.assertEqual(r[5]['Female'], 0)
        self.assertEqual(r[5]['Total'], 1)

        self.assertEqual(r[6]['Male'], 6)
        self.assertEqual(r[6]['Female'], 1)
        self.assertEqual(r[6]['Total'], 7)

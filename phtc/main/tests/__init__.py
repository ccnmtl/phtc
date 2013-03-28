from django.test import TestCase


class DummyTest(TestCase):
    def test_nothing(self):
        """ jenkins needs to have at least one test """
        assert True

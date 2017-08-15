from django.test import TestCase
from phtc.logic_model.models import BoxColor, GamePhase, ActivePhase, Column
from phtc.logic_model.models import Scenario, LogicModelBlock


class BoxColorTest(TestCase):
    def test_unicode(self):
        bc = BoxColor()
        self.assertEqual(str(bc), '')

    def test_to_json(self):
        bc = BoxColor()
        self.assertEqual(bc.to_json(), {'color': 'FFFFFF'})


class GamePhaseTest(TestCase):
    def test_unicode(self):
        gp = GamePhase()
        self.assertEqual(str(gp), '')

    def test_to_json(self):
        gp = GamePhase.objects.create()
        self.assertEqual(
            gp.to_json(),
            {
                'id': gp.id,
                'name': '',
                'instructions': '',
                'css_classes': '',
            })


class ActivePhaseTest(TestCase):
    def test_unicode(self):
        gp = GamePhase.objects.create()
        c = Column.objects.create()
        ap = ActivePhase.objects.create(game_phase=gp, column=c)
        self.assertEqual(
            str(ap),
            "Column \"%s\" is active during game phase \"%s\"" % (c, gp))

    def test_to_json(self):
        gp = GamePhase.objects.create()
        c = Column.objects.create()
        ap = ActivePhase.objects.create(game_phase=gp, column=c)
        self.assertEqual(
            ap.to_json(),
            {
                'game_phase_id': gp.id,
                'column_id': c.id,
            }
        )


class ScenarioTest(TestCase):
    def test_unicode(self):
        s = Scenario()
        self.assertEqual(str(s), '')

    def test_to_json(self):
        s = Scenario.objects.create()
        self.assertEqual(
            s.to_json(),
            {
                'id': s.id,
                'title': '',
                'instructions': '',
                'difficulty': '',
                'answer_key': None
            }
        )


class ColumnTest(TestCase):
    def test_unicode(self):
        c = Column()
        self.assertEqual(str(c), '')

    def test_to_json(self):
        c = Column.objects.create()
        self.assertEqual(
            c.to_json(),
            {
                'id': c.id,
                'name': '',
                'css_classes': '',
                'help_definition': '',
                'help_examples': '',
                'flavor': ''
            })


class LogicModelBlockTest(TestCase):
    def test_needs_submit(self):
        lmb = LogicModelBlock.objects.create()
        self.assertFalse(lmb.needs_submit())

    def test_add_form(self):
        f = LogicModelBlock.add_form()
        self.assertTrue(hasattr(f, 'fields'))

    def test_edit_form(self):
        lmb = LogicModelBlock.objects.create()
        f = lmb.edit_form()
        self.assertTrue(hasattr(f, 'fields'))

    def test_unlocked(self):
        lmb = LogicModelBlock.objects.create()
        self.assertTrue(lmb.unlocked(None))

    def test_edit(self):
        lmb = LogicModelBlock.objects.create()
        lmb.edit(dict(), None)

from django import forms
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from pagetree.models import PageBlock


class BoxColor (models.Model):
    name = models.CharField(max_length=256, default='')
    color = models.CharField(max_length=6, default='FFFFFF')
    order_rank = models.IntegerField(default=0, null=True, blank=True, )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order_rank']

    def to_json(self):
        return {
            'color': self.color
        }


class GamePhase (models.Model):
    name = models.CharField(max_length=256, default='')
    instructions = models.TextField(null=True, blank=True, default='')
    order_rank = models.IntegerField(default=0, null=True, blank=True, )
    css_classes = models.CharField(max_length=256, null=True, blank=True,
                                   default='')

    class Meta:
        ordering = ['order_rank']

    def __unicode__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'instructions': self.instructions,
            'css_classes': self.css_classes
        }


class ActivePhase (models.Model):
    """ Indicates that a particular column is active (editable)
    during a particular phase"""

    def __unicode__(self):
        return "Column \"%s\" is active during game phase \"%s\"" % (
            self.column, self.game_phase)

    game_phase = models.ForeignKey('GamePhase')
    column = models.ForeignKey('Column')

    class Meta:
        ordering = ['game_phase', 'column']
        unique_together = ("game_phase", "column")

    def to_json(self):
        return {
            'game_phase_id': self.game_phase.id,
            'column_id': self.column.id
        }


class Scenario  (models.Model):
    title = models.CharField(max_length=256, default='')
    difficulty = models.CharField(max_length=256, default='')
    order_rank = models.IntegerField(default=0, null=True, blank=True, )
    instructions = models.TextField(null=True, blank=True, default='')

    class Meta:
        ordering = ['order_rank']

    def __unicode__(self):
        return self.title

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'instructions': self.instructions,
            'difficulty': self.difficulty
        }


class Column (models.Model):
    name = models.CharField(max_length=256, default='')
    order_rank = models.IntegerField(default=0, null=True, blank=True, )
    css_classes = models.CharField(max_length=256, null=True, blank=True,
                                   default='')
    help_definition = models.TextField(null=True, blank=True, default='')
    help_examples = models.TextField(null=True, blank=True, default='')
    flavor = models.CharField(max_length=256, default='')

    class Meta:
        ordering = ['order_rank']

    def __unicode__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'css_classes': self.css_classes,
            'help_definition': self.help_definition,
            'help_examples': self.help_examples,
            'flavor': self.flavor
        }


class LogicModelBlock(models.Model):
    pageblocks = GenericRelation(PageBlock)
    template_file = "logic_model/logic_model.html"
    js_template_file = "logic_model/block_js.html"
    css_template_file = "logic_model/block_css.html"
    display_name = "Logic Model Activity"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(cls):
        return LogicModelBlockForm()

    def edit_form(self):
        return LogicModelBlockForm(instance=self)

    @classmethod
    def create(cls, request):
        form = LogicModelBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = LogicModelBlockForm(
            data=vals,
            files=files,
            instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True


class LogicModelBlockForm(forms.ModelForm):
    class Meta:
        model = LogicModelBlock
        exclude = []

from django.db import models
from django.contrib.contenttypes import generic
from pagetree.models import PageBlock
from django import forms

class Scenario  (models.Model):
    title = models.CharField(max_length=256, default = '')
    difficulty = models.CharField(max_length=256, default = '')
    order_rank = models.IntegerField(default=0, null=True, blank=True, )
    instructions = models.TextField(null=True, blank=True, default = '')

    class Meta:
        ordering = ['order_rank']

    def __unicode__(self):
        return self.title

    def to_json(self):
        return {
            'title': self.title,
            'instructions': self.instructions
        }

class Column (models.Model):
    name = models.CharField(max_length=256, default = '')
    order_rank = models.IntegerField(default=0, null=True, blank=True, )
    css_classes = models.CharField(max_length=256, null=True, blank=True, default = '')
    help_definition  = models.TextField(null=True, blank=True, default = '')
    help_examples  = models.TextField(null=True, blank=True, default = '')
    flavor = models.CharField(max_length=256, default = '')
    class Meta:
        ordering = ['order_rank']


    def __unicode__(self):
        return self.name

    def to_json(self):
        return {
            'css_classes': self.css_classes,
            'help_definition': self.help_definition,
            'help_examples': self.help_examples,
            'flavor': self.flavor
        }

class LogicModelBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
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
    def add_form(self):
        return LogicModelBlockForm()

    def edit_form(self):
        return LogicModelBlockForm(instance=self)

    @classmethod
    def create(self, request):
        form = LogicModelBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = LogicModelBlockForm(data=vals,
                                          files=files,
                                          instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True

    def treatment_paths(self):
        return TreatmentPath.objects.all()


class LogicModelBlockForm(forms.ModelForm):
    class Meta:
        model = LogicModelBlock


if 1 == 0:
    class TreatmentNode(MP_Node):
        name = models.CharField(max_length=256)
        type = models.CharField(max_length=2, choices=NODE_CHOICES)
        text = models.TextField(null=True, blank=True)
        help = models.TextField(null=True, blank=True)
        duration = models.IntegerField(default=0)
        value = models.IntegerField(default=0)

        def __unicode__(self):
            if self.type == 'DP':
                return "  Decision Point: " + self.name
            elif self.duration:
                return "  %s weeks: %s" % (self.duration, self.name)
            else:
                return "  %s" % self.name

        def to_json(self):
            return {
                'id': self.id,
                'name': self.name,
                'type': self.type,
                'text': self.text,
                'help': self.help,
                'duration': self.duration,
                'value': self.value, 
                'children_list': [{'name': c.name, 'id': c.id, 'value': c.value} for c in self.get_children()]
            }


    class TreatmentPath(models.Model):
        name = models.CharField(max_length=512)
        tree = models.ForeignKey(TreatmentNode)
        cirrhosis = models.BooleanField()
        treatment_status = models.IntegerField(choices=STATUS_CHOICES)
        drug_choice = models.CharField(max_length=12, choices=DRUG_CHOICES)

        def __unicode__(self):
            return self.name



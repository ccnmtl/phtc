from django.db import models
from django.contrib.contenttypes import generic
from pagetree.models import PageBlock
from django import forms
from treebeard.mp_tree import MP_Node


NODE_CHOICES = (
    ('RT', 'Root'),
    ('PR', 'Parent'),
    ('IF', 'TreatmentStep'),
    ('DP', 'DecisionPoint'),
    ('ST', 'Stop')
)

STATUS_CHOICES = (
    (0, 'Treatment Naive'),
    (1, 'Prior Null Responder'),
    (2, 'Prior Relapser'),
    (3, 'Prior Partial Responder')
)

DRUG_CHOICES = (
    ('boceprevir', 'Boceprevir'),
    ('telaprevir', 'Telaprevir')
)


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
            'value': self.value
        }


class TreatmentPath(models.Model):
    name = models.CharField(max_length=512)
    tree = models.ForeignKey(TreatmentNode)
    cirrhosis = models.BooleanField()
    treatment_status = models.IntegerField(choices=STATUS_CHOICES)
    drug_choice = models.CharField(max_length=12, choices=DRUG_CHOICES)

    def __unicode__(self):
        return self.name


class TreatmentActivityBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "treatment_activity/treatment_activity.html"
    js_template_file = "treatment_activity/block_js.html"
    css_template_file = "treatment_activity/block_css.html"
    display_name = "Response Guided Treatment Activity"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return TreatmentActivityBlockForm()

    def edit_form(self):
        return TreatmentActivityBlockForm(instance=self)

    @classmethod
    def create(self, request):
        form = TreatmentActivityBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = TreatmentActivityBlockForm(data=vals,
                                          files=files,
                                          instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True

    def treatment_paths(self):
        return TreatmentPath.objects.all()


class TreatmentActivityBlockForm(forms.ModelForm):
    class Meta:
        model = TreatmentActivityBlock

from django.db import models
from django.contrib.contenttypes import generic
from pagetree.models import PageBlock
from django import forms
from treebeard.mp_tree import MP_Node


NODE_CHOICES = (
    ('RT', 'Root'), # trivial -- at the very top.
    ('PR', 'Parent'), #Decision Point Branch -- similar to Decision Point, but different and appears more friendly to non-binary
    ('IF', 'TreatmentStep'), #  Generic Treatment Step  -- trivial -- describes what happens .
    ('DP', 'DecisionPoint'), # shows a yes  or no question, returns 1 or 0.
    ('ST', 'Stop') # trivial -- a leaf node.
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

"""

TODO wireframes

    Are we adding steps before/after step 4 for reflection?

    Are we allowing users to submit more than one logic_model per scenario?
        I assume not, but if so we need wireframes about how to navigate between the different
        responses to the same scenario.

    How does the user get back to the list of logic models once they're done submitting a response?
        Hint -- maybe a conclusion page.

    The wireframes don't show the regular Forest back and next buttons.


        How is a user supposed to leave the activity?

        If the user does leave the activity, are they prompted about unfinished scenarios or logic models?

    Wireframes re: user-created scenario -- how does that work?
    The wireframes don't describe what happens when a user clicks "Your Own Scenario", then Begin.
        How many scenarios are allowed per user per pageblock? (Is there a max of 1?
            Or does a user build up a portfolio of logic models?)


    You can both click and drag boxes. I'm assuming the following common rules:
        When you click a box it becomes editable and a cursor appears.
        When you click *outside* a box you were editing, it loses focus and the new contents are saved.
        When you *drag* a box it starts to move.



Here is the model:
    column
        ""A column in the activity. Everything in this table is shared by all possible scenarios.""
        title            (text)
        ordering         (int)
        css_classes      (text)
        help_definition  (free HTML)
        help_examples    (free HTML)
        flavor           (first / last / middle_step)

    LogicModelBlock
        ""A pageblock that displays a collection of scenarios and links to CRUD them.""
        pageblock              (GenericRelation)
        allow_user_contributed (boolean)

    scenario
        ""A case study describing a problem. The participants are challenged to propose a way to solve it. Their response
        takes the form of a logic_model.""
        LogicModelBlock (FK)
        user            (FK) (in case of user-contributed scenarios.)
        instructions    (text) (this is editable to users in the case of a user_contributed scenario.)
        special_flags   (text) (a way to describe anything funky about this scenario)
        css_classes     (text)
        notes_1         (text)
        notes_2         (text)
        notes_3         (text)
        row_count       (int)
        difficulty      (simple/moderate/complex)

    logic_model
        ""A logic model describes a particular user's response to the case study provided by the scenario.""
        expert          (boolean)
        user            (FK)
        scenario        (FK)
        pre_reflection  (text)
        post_reflection (text)
        other_notes     (text)
        created         (timestamp)
        modified        (timestamp)
        finished        (boolean)
        public          (boolean)

    content_box
        "" What one user typed in one box in response to a particular scenario.""
        logic_model     (FK)
        column          (FK)
        row             (int)
        html            (text)

******
    NOTES:
        We are deliberately not making up our mind about whether a user can submit more than one
        logic_model per scenario. I would assume this would be on a per-application basis.






"""

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



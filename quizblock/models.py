from django.db import models
from pagetree.models import PageBlock
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django import forms
from datetime import datetime
from django.core.urlresolvers import reverse


class Quiz(models.Model):
    pageblocks = GenericRelation(PageBlock)
    description = models.TextField(blank=True)
    rhetorical = models.BooleanField(default=False)
    reading_exercise = models.BooleanField(default=False)
    feedback = models.BooleanField(default=False)
    matching = models.BooleanField(default=False)
    allow_redo = models.BooleanField(default=True)
    pre_test = models.BooleanField(default=False)
    post_test = models.BooleanField(default=False)
    post_test_credit = models.FloatField(default=0.0, null=True)

    template_file = "quizblock/quizblock.html"

    display_name = "Quiz"
    exportable = True
    importable = True

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return not self.rhetorical

    def submit(self, user, data):
        """ a big open question here is whether we should
        be validating submitted answers here, on submission,
        or let them submit whatever garbage they want and only
        worry about it when we show the admins the results """
        s = Submission.objects.create(quiz=self, user=user)
        for k in data.keys():
            if k.startswith('question'):
                qid = int(k[len('question'):])
                question = Question.objects.get(id=qid)
                # it might make more sense to just accept a QueryDict
                # instead of a dict so we can use getlist()
                if isinstance(data[k], list):
                    for v in data[k]:
                        Response.objects.create(
                            submission=s,
                            question=question,
                            value=v)
                else:
                    Response.objects.create(
                        submission=s,
                        question=question,
                        value=data[k])

    def redirect_to_self_on_submit(self):
        return True

    def unlocked(self, user):
        # meaning that the user can proceed *past* this one,
        # not that they can access this one. careful.
        if user.is_anonymous:
            return False

        return Submission.objects.filter(quiz=self, user=user).count() > 0

    def edit_form(self):
        class EditForm(forms.Form):
            description = forms.CharField(widget=forms.widgets.Textarea(),
                                          initial=self.description,
                                          required=False)
            rhetorical = forms.BooleanField(initial=self.rhetorical,
                                            required=False)
            feedback = forms.BooleanField(initial=self.feedback,
                                          required=False)
            allow_redo = forms.BooleanField(initial=self.allow_redo,
                                            required=False)
            reading_exercise = forms.BooleanField(
                initial=self.reading_exercise,
                required=False)
            matching = forms.BooleanField(initial=self.matching,
                                          required=False)
            pre_test = forms.BooleanField(initial=self.pre_test,
                                          required=False)
            post_test = forms.BooleanField(initial=self.post_test,
                                           required=False)
            post_test_credit = forms.FloatField(
                widget=forms.widgets.TextInput(
                    attrs={'class': 'post_test_credit'}),
                initial=self.post_test_credit,
                required=False)
            alt_text = (
                "<a href=\"" + reverse("edit-quiz", args=[self.id]) +
                "\">manage questions/answers</a>")
        return EditForm()

    @classmethod
    def add_form(cls):
        class AddForm(forms.Form):
            description = forms.CharField(required=False,
                                          widget=forms.widgets.Textarea())
            rhetorical = forms.BooleanField(required=False)
            feedback = forms.BooleanField(required=False)
            allow_redo = forms.BooleanField(required=False)
            reading_exercise = forms.BooleanField(required=False)
            matching = forms.BooleanField(required=False)
            pre_test = forms.BooleanField(required=False)
            post_test = forms.BooleanField(required=False)
            post_test_credit = forms.FloatField(initial=0.0, required=False)
        return AddForm()

    @classmethod
    def bool(cls, d, name, default_value):
        value = d.get(name, default_value)
        return value in ('True', True, 'on')

    @classmethod
    def create(cls, request):
        reading_exercise = cls.bool(request.POST, 'reading_exercise', False)
        matching = cls.bool(request.POST, 'matching', False)
        allow_redo = cls.bool(request.POST, 'allow_redo', False)
        pre_test = cls.bool(request.POST, 'pre_test', False)
        post_test = cls.bool(request.POST, 'post_test', False)
        rhetorical = cls.bool(request.POST, 'rhetorical', False)
        feedback = cls.bool(request.POST, 'feedback', False)

        return Quiz.objects.create(
            description=request.POST.get('description', ''),
            rhetorical=rhetorical,
            feedback=feedback,
            reading_exercise=reading_exercise,
            matching=matching,
            allow_redo=allow_redo,
            pre_test=pre_test,
            post_test=post_test,
            post_test_credit=request.POST.get('post_test_credit', 0.0)
        )

    @classmethod
    def create_from_dict(cls, d):
        q = Quiz.objects.create(
            description=d.get('description', ''),
            rhetorical=d.get('rhetorical', False),
            feedback=d.get('feedback', False),
            reading_exercise=d.get('reading_exercise', False),
            matching=d.get('matching', False),
            pre_test=d.get('pre_test', False),
            post_test=d.get('post_test', False),
            post_test_credit=d.get('post_test_credit', 0.0),
            allow_redo=d.get('allow_redo', True),
        )
        q.import_from_dict(d)
        return q

    def edit(self, vals, files):
        self.description = vals.get('description', '')
        self.rhetorical = self.bool(vals, 'rhetorical', False)
        self.feedback = self.bool(vals, 'feedback', False)
        self.reading_exercise = self.bool(vals, 'reading_exercise', False)
        self.matching = self.bool(vals, 'matching', False)
        self.pre_test = self.bool(vals, 'pre_test', False)
        self.post_test = self.bool(vals, 'post_test', False)
        self.post_test_credit = vals.get('post_test_credit', '')
        self.allow_redo = self.bool(vals, 'allow_redo', False)
        self.save()

    def add_question_form(self, request=None):
        return QuestionForm(request)

    def update_questions_order(self, question_ids):
        self.set_question_order(question_ids)

    def clear_user_submissions(self, user):
        Submission.objects.filter(user=user, quiz=self).delete()

    def as_dict(self):
        d = dict(description=self.description,
                 rhetorical=self.rhetorical,
                 feedback=self.feedback,
                 reading_exercise=self.reading_exercise,
                 matching=self.matching,
                 pre_test=self.pre_test,
                 post_test=self.post_test,
                 post_test_credit=self.post_test_credit,
                 allow_redo=self.allow_redo)
        d['questions'] = [q.as_dict() for q in self.question_set.all()]
        return d

    def import_from_dict(self, d):
        self.description = d['description']
        self.rhetorical = d['rhetorical']
        self.feedback = d['feedback']
        self.reading_exercise = d['reading_exercise']
        self.matching = d['matching']
        self.allow_redo = d.get('allow_redo', True)
        self.save()
        self.submission_set.all().delete()
        self.question_set.all().delete()
        for q in d['questions']:
            question = Question.objects.create(
                quiz=self, text=q['text'],
                question_type=q['question_type'],
                explanation=q['explanation'],
                intro_text=q['intro_text'])
            for a in q['answers']:
                Answer.objects.create(question=question,
                                      value=a['value'],
                                      label=a['label'],
                                      feedback=a['feedback'],
                                      correct=a['correct'])


class Question(models.Model):
    quiz = models.ForeignKey(Quiz)
    text = models.TextField()
    question_type = models.CharField(
        max_length=256,
        choices=(
            ("multiple choice", "Multiple Choice: Multiple answers"),
            ("matching", "Matching: Match questions with set of answers"),
            ("single choice", "Multiple Choice: Single answer"),
            ("single choice feedback",
             "Multiple Choice: Single answer with item feedback"),
            ("single choice dropdown",
             "Multiple Choice: Single answer (dropdown)"),
            ("short text", "Short Text"),
            ("long text", "Long Text"),
        ))
    explanation = models.TextField(blank=True)
    intro_text = models.TextField(blank=True)

    class Meta:
        order_with_respect_to = 'quiz'

    def __unicode__(self):
        return self.text

    def display_number(self):
        return self._order + 1

    def edit_form(self, request=None):
        return QuestionForm(request, instance=self)

    def add_answer_form(self, request=None):
        return AnswerForm(request)

    def correct_answer_values(self):
        return [a.value for a in self.answer_set.filter(correct=True)]

    def correct_answer_number(self):
        if self.question_type != "single choice":
            return None
        return self.answer_set.filter(correct=True)[0]._order

    def correct_answer_letter(self):
        if (self.question_type != "single choice" or
                self.answer_set.count() == 0):
            return None
        return chr(ord('A') + self.correct_answer_number())

# FIXME: this redefines an existing function.
# please pick one or the other.
#
#    def correct_answer_number(self):
#        if self.question_type != "single choice feedback":
#            return None
#        return self.answer_set.filter(correct=True)[0]._order

# FIXME: this redefines an existing function.
# please pick one or the other.
#
#    def correct_answer_letter(self):
#        if (self.question_type != "single choice feedback"
#            or self.answer_set.count() == 0):
#            return None
#        return chr(ord('A') + self.correct_answer_number())

    def update_answers_order(self, answer_ids):
        self.set_answer_order(answer_ids)

    def answerable(self):
        """ whether it makes sense to have Answers associated with this """
        return self.question_type in ["multiple choice",
                                      "matching",
                                      "single choice feedback",
                                      "single choice",
                                      "single choice dropdown"]

    def is_short_text(self):
        return self.question_type == "short text"

    def is_long_text(self):
        return self.question_type == "long text"

    def is_single_choice(self):
        return self.question_type == "single choice"

    def is_single_choice_feedback(self):
        return self.question_type == "single choice feedback"

    def is_matching(self):
        return self.question_type == "matching"

    def is_single_choice_dropdown(self):
        return self.question_type == "single choice dropdown"

    def is_multiple_choice(self):
        return self.question_type == "multiple choice"

    def user_responses(self, user):
        submission = Submission.objects.filter(
            user=user,
            quiz=self.quiz).order_by("-submitted")[0]
        return Response.objects.filter(question=self, submission=submission)

    def as_dict(self):
        return dict(
            text=self.text,
            question_type=self.question_type,
            explanation=self.explanation,
            intro_text=self.intro_text,
            answers=[a.as_dict() for a in self.answer_set.all()]
        )


class Answer(models.Model):
    question = models.ForeignKey(Question)
    value = models.CharField(max_length=256)
    label = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    correct = models.BooleanField(default=False)

    class Meta:
        order_with_respect_to = 'question'

    def __unicode__(self):
        return self.label

    def edit_form(self, request=None):
        return AnswerForm(request, instance=self)

    def as_dict(self):
        return dict(value=self.value, label=self.label, feedback=self.feedback,
                    correct=self.correct)


class Submission(models.Model):
    quiz = models.ForeignKey(Quiz)
    user = models.ForeignKey(User)
    submitted = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return "quiz %d submission by %s at %s" % (self.quiz.id,
                                                   unicode(self.user),
                                                   self.submitted)


class Response(models.Model):
    question = models.ForeignKey(Question)
    submission = models.ForeignKey(Submission)
    value = models.TextField(blank=True)

    class Meta:
        ordering = ('question',)

    def __unicode__(self):
        return "response to %s [%s]" % (unicode(self.question),
                                        unicode(self.submission))

    def is_correct(self):
        return self.value in self.question.correct_answer_values()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ("quiz",)
        fields = ('question_type', 'intro_text', 'text', 'explanation')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ("question",)

    def clean(self):
        if 'value' not in self.cleaned_data:
            raise forms.ValidationError(
                'Please enter a meaningful value for this answer.')
        else:
            return self.cleaned_data

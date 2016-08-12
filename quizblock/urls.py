from django.conf.urls import url

from .views import (
    edit_quiz, add_question_to_quiz, edit_question, add_answer_to_question,
    delete_question, reorder_answers, reorder_questions, delete_answer,
    edit_answer,
)

urlpatterns = [
    url(r'^edit_quiz/(?P<id>\d+)/$', edit_quiz, {}, 'edit-quiz'),
    url(r'^edit_quiz/(?P<id>\d+)/add_question/$', add_question_to_quiz, {},
        'add-question-to-quiz'),
    url(r'^edit_question/(?P<id>\d+)/$', edit_question, {}, 'edit-question'),
    url(r'^edit_question/(?P<id>\d+)/add_answer/$', add_answer_to_question, {},
        'add-answer-to-question'),
    url(r'^delete_question/(?P<id>\d+)/$', delete_question, {},
        'delete-question'),
    url(r'^reorder_answers/(?P<id>\d+)/$', reorder_answers, {},
        'reorder-answer'),
    url(r'^reorder_questions/(?P<id>\d+)/$', reorder_questions, {},
        'reorder-questions'),
    url(r'^delete_answer/(?P<id>\d+)/$', delete_answer, {}, 'delete-answer'),
    url(r'^edit_answer/(?P<id>\d+)/$', edit_answer, {}, 'edit-answer'),
]

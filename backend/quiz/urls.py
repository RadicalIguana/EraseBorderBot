from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    
    path('getUserId', views.get_user_id, name='get_user_id'),
    path('createUser', views.create_user, name='create_user'),
    path("getUser", views.get_user, name='get_user'),
    path("getQuestionAnswer", views.get_question_answer, name="get_question_answer"),
    path("getSubTest", views.get_subjects_tests, name="get_subjects_tests"),
    path("createResult", views.create_result, name="create_result"),
    path("getResult", views.get_result, name="get_result"),
    path("checkTest", views.check_test, name="check_test"),
    path("checkResult", views.check_result, name="check_result"),
    path("quizCreate", views.quiz_create, name='quiz_create'),
    path("sendFeedback", views.send_feedback, name="send_feedback"),
]
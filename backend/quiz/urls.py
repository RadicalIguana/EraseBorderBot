from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path('getUserId', views.get_user_id, name='get_user_id'),
    path('createUser', views.create_user, name='create_user'),
    path("getUser", views.get_user, name='get_user'),
    
    path("getSubject", views.get_subject, name="get_subject"),
    path("getAllSubjects", views.get_all_subjects, name="get_all_subjects"),
    path("getTest", views.get_test, name="get_test"),
    path("getQuestion", views.get_question, name="get_question"),
    path("getAnswer", views.get_answer, name="get_answer"),
    path("getQuestionAnswer", views.get_question_answer, name="get_question_answer"),
    
    path("getSubTest", views.get_subjects_tests, name="get_subjects_tests"),
    
    path("createResult", views.create_result, name="create_result"),
    path("updateResult", views.update_result, name="update_result"),
    
    path("checkResult", views.check_result, name="check_result"),
]
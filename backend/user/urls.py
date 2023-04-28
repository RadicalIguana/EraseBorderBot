from django.urls import path, include

from . import views

urlpatterns = [
    path('getUserId', views.get_user_id, name='get_user_id'),
    path('createUser', views.create_user, name='create_user'),
    path('getUser', views.get_user, name='get_user')
]

from django.urls import path
from . import views

urlpatterns = [
    path('function', views.all_user),
    path('class', views.HelloWorldView.as_view()),
]
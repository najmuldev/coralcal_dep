from django.urls import path
from . import views

urlpatterns = [
    path('form', views.form, name='p_form'),
    path('history', views.history, name='p_history'),
]

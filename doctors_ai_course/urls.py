from django.urls import path
from . import views

urlpatterns = [
    path('form', views.dac_form, name='dac_form'),
]

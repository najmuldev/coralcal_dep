from django.urls import path 
from .import views

urlpatterns = [
    path('form', views.dac_form, name='dac2_form'),
    path('edit', views.edit_dac_form, name='dac2_edit'),
]

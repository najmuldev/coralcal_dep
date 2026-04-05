from django.urls import path 
from .import views

urlpatterns = [
    path('form', views.dac_form, name='dac2_form'),
    path('edit/<int:instance_id>', views.edit_dac_form, name='dac2_edit'),
    path('history', views.dac2_history, name='dac2_history'),
    path('delete/<int:instance_id>', views.dac2_delete, name='dac2_delete'),
]

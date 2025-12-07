from django.urls import path
from . import views

urlpatterns = [
    path('form', views.form, name='p_form'),
    path('history', views.history, name='p_history'),
    path('edit/<int:instance_id>', views.edit, name='p_edit'),
]

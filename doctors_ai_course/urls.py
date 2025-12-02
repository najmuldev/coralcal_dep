from django.urls import path
from . import views

urlpatterns = [
    path('form', views.dac_form, name='dac_form'),
    path('edit', views.edit_dac_form, name='edit_dac'),
    path('delete/<str:territory>', views.delete_dac, name='delete_dac'),
]

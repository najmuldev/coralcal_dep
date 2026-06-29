from django.urls import path 
from .views import nfc_form_view, nfc_history_view, nfc_edit_view, nfc_delete_view

urlpatterns = [
    path('nfc_form', nfc_form_view, name='nfc_form'),
    path('nfc_history', nfc_history_view, name='nfc_history'),
    path('nfc_edit/<int:pk>', nfc_edit_view, name= 'nfc_edit'),
    path('nfc_delete/<int:pk>', nfc_delete_view, name= 'nfc_delete'),
]

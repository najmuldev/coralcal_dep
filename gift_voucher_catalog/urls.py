from django.urls import path
from .views import *

urlpatterns = [
    path('form', gift_voucher_catalog_26_form, name='gvc_form'),
    path('admin', gvc_admin_form, name='gvc_admin'),
    path('export', gvc_export, name='gvc_export'),
    path('delete/<int:id>', gvc_delete, name='gvc_delete'),
]
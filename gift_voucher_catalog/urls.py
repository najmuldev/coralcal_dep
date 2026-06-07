from django.urls import path
from .views import *

urlpatterns = [
    path('form', gift_voucher_catalog_26_form, name='gvc_form'),
]
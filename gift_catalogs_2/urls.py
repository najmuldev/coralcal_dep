from django.urls import path 
from .views import *

urlpatterns = [
    path('form', gift_catalogs_2026_form, name='gift_catalogs_2026_form'),
]

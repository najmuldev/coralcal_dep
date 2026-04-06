from django.urls import path 
from .views import *

urlpatterns = [
    path('form', gift_catalogs_2026_form, name='gift_catalogs_2026_form'),
    path('edit/<int:id>/', edit_gift_catalog, name='edit_gift_catalogs_2026'),
    path('delete/<int:id>/', delete_gift_catalog, name='delete_gift_catalogs_2026'),
]

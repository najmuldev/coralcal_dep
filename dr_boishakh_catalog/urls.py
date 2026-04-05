from django.urls import path
from .views import boishakh_choice, view_boishakh_catalogs, delete_boishakh_catalog, edit_boishakh_catalog

urlpatterns = [
    path('choice', boishakh_choice, name='boishakh_choice'),
    path('choiced', view_boishakh_catalogs, name='view_boishakh_catalogs'),
    path('delete_gift/<int:id>/', delete_boishakh_catalog, name='delete_boishakh_catalog'),
    path('edit_gift/<int:id>', edit_boishakh_catalog, name='edit_boishakh_catalog'),
]
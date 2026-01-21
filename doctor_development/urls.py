from django.urls import path
from doctor_development.views import book_choice, admin, export_wishlist, edit_choice

urlpatterns = [
    path('gift', book_choice, name='book_choice'),
    path('admin',admin, name='admin'),
    path('export_wishlist', export_wishlist, name='export_wishlist'),
    path('edit_ks/<int:id>', edit_choice, name='edit_ks')
]
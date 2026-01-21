from django.urls import path
from doctor_development.views import gift_choice, admin, export_wishlist, edit_choice

urlpatterns = [
    path('gift', gift_choice, name='gift_choice'),
    path('admin',admin, name='admin'),
    path('export_wishlist', export_wishlist, name='export_wishlist'),
    path('edit_dd/<int:id>', edit_choice, name='edit_dd')
]
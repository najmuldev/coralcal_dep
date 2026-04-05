from django.urls import path
from doctor_development.views import dd_gift_choice, admin, export_wishlist, edit_choice

urlpatterns = [
    path('gift', dd_gift_choice, name='dd_gift_choice'),
    path('admin',admin, name='admin'),
    path('export_wishlist', export_wishlist, name='export_wishlist'),
    path('edit_dd/<int:id>', edit_choice, name='edit_dd')
]
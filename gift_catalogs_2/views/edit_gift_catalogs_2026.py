from django.shortcuts import render, redirect
from django.contrib import messages
import csv, os, shutil
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from gift_catalogs_2.models import GiftCatalog2
from gift_catalogs_2.constant import IMAGE_TO_GIFT

@login_required
def edit_gift_catalog(request, id):
    try:
        obj = GiftCatalog2.objects.get(id=id)
        count = 1 if obj else 0

        if request.method == 'POST':
            dr_id = request.POST.get('dr_id')
            dr_name = request.POST.get('dr_name')
            selected_image = request.POST.get('selected_image')
            if not (dr_id and dr_name and selected_image):
                messages.error(request, "All fields are required and a gift must be selected.")
                return redirect('gift_catalogs_2026_form')
            gift = IMAGE_TO_GIFT.get(selected_image)
            
            GiftCatalog2.objects.update_or_create(
                id=id,
                defaults={
                    'dr_id': dr_id,
                    'dr_name': dr_name,
                    'gift': gift
                }
            )
            messages.success(request, "Gift catalog entry updated successfully.")
            if request.user.is_superuser:
                return redirect('gift_catalogs_2026')
            return redirect('home')
        
        return render(request, 'edit_gift_choice.html', {
            'obj': obj,
            'count': count
        })

    except GiftCatalog2.DoesNotExist:
        messages.error(request, "Gift catalog entry not found.")
        if request.user.is_superuser:
            return redirect('gift_catalogs')
        return redirect('gift_choice')
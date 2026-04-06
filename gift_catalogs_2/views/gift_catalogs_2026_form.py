from django.shortcuts import render, redirect
from django.contrib import messages
from gift_catalogs_2.models import GiftCatalog2
from gift_catalogs_2.constant import TERRITORY_LIST, REGION_LIST, IMAGE_TO_GIFT
from core.models import Territory

def gift_catalogs_2026_form(request):
    user = request.user.username
    territory = Territory.objects.get(territory=user)
    region = request.user.userprofile.region_name

    if int(user) not in TERRITORY_LIST:
        if region not in REGION_LIST:
            gift_obj = GiftCatalog2.objects.filter(territory__region_name=region)
            obj_count = gift_obj.count() if gift_obj else 0
            if obj_count >= 1 and gift_obj.first().territory != territory:
                messages.error(request, "One of territory already submitted the form for this region.")
                return redirect('home')
        else:
            messages.error(request, "You are not authorized to access this form.")
            return redirect('home')
    
    if request.method == 'POST':
        try:
            dr_id = request.POST.get('dr_id')
            dr_name = request.POST.get('dr_name')
            selected_image = request.POST.get('selected_image')
            if not (dr_id and dr_name and selected_image):
                messages.error(request, "All fields are required and a gift must be selected.")
                return redirect('gift_catalogs_2026_form')
            gift = IMAGE_TO_GIFT.get(selected_image)
            
            GiftCatalog2.objects.update_or_create(
                territory=territory,
                defaults={
                    'dr_id': dr_id,
                    'dr_name': dr_name,
                    'gift': gift
                }
            )
            
            messages.success(request, f"Successfully submitted gift choice for {dr_name}.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('gift_choice')
    elif request.method == 'GET':
        try:
            obj = GiftCatalog2.objects.filter(territory=territory)
            count = obj.count() if obj else 0
            if count:
                obj = obj.first()
            return render(request, 'gift_catalogs_2_form.html', {
                'obj': obj,
                'count': count
            })
        except Exception as e:
            messages.error(request, "An error occurred while loading the form.")
            return redirect('home')
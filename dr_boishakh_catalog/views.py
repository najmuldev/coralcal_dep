from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PohelaBoishakhCatalog, Territory
import  os, shutil
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static

# map gift names
IMAGE_TO_GIFT = {
    'image1': '1',
    'image2': '2',
    'image3': '3',
    'image4': '4',
    'image5': '5',
    'image6': '6',
    'image7': '7',
}
# Create your views here.
@login_required
def boishakh_choice(request):
    """
    Render the gift catalogs page.
    """
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        selected_image = request.POST.get('selected_image')

        if not (dr_id and dr_name and selected_image):
            messages.error(request, "All fields are required and a gift must be selected.")
            return redirect('gift_choice')
        gift = IMAGE_TO_GIFT.get(selected_image)
        conference_image = request.FILES.get('conference_image')

        try:
            territory = Territory.objects.get(territory=request.user.username)
            if not territory:
                messages.error(request, "No territory found.")
                return redirect('gift_choice')
            # Save data
            PohelaBoishakhCatalog.objects.create(
                territory=territory,
                dr_id=dr_id,
                dr_name=dr_name,
                gift=gift,
                conference_image=conference_image
            )   
            messages.success(request, f"Successfully submitted gift choice for {dr_name}.")
            return redirect('gift_choice')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('gift_choice')
    elif request.method == 'GET':
        territory_id = request.user.username
        try:
            obj = PohelaBoishakhCatalog.objects.filter(territory__territory=territory_id)
        except PohelaBoishakhCatalog.DoesNotExist:
            obj = None
        count = obj.count() if obj else 0
        if count >=2 :
            return redirect('gift_choiced')
        return render(request, 'gift_choice.html', {
            'obj': obj,
            'count': count
        })
        
@login_required 
def view_boishakh_catalogs(request):
    territory_id = request.user.username
    try:
        obj = PohelaBoishakhCatalog.objects.filter(territory__territory=territory_id)
    except PohelaBoishakhCatalog.DoesNotExist:
        obj = None
        return redirect('gift_choice')   
    for item in obj:
        gift = item.gift
        if gift == 'Pureit Classic 23 L':
            item.img = static('images/pureit.webp')
        elif gift == 'Philips Blender 450W Daily Collection (HR2058/91)':
            item.img = static('images/blender.webp')
        elif gift == 'Smart Watch Fastrack Reflex Rave FX':
            item.img = static('images/watch.webp') 
        elif gift == 'Kiam Marble Coated 7 pc Set':
            item.img = static('images/cookware.jpg') 
        elif gift == 'International Scientific Conference Registration':
            item.img = static('images/conference.png')
        else:
            print('No item found')
            
    return render(request, 'view_choice.html', {'data':obj})


@login_required
def delete_boishakh_catalog(request, id):
    """
    Delete a gift catalog entry and its associated conference image folder if applicable.
    """
    try:
        obj = PohelaBoishakhCatalog.objects.get(id=id)

        obj.delete()
        messages.success(request, "Gift catalog entry deleted successfully.")

    except PohelaBoishakhCatalog.DoesNotExist:
        messages.error(request, "Gift catalog entry not found.")
    except Exception as e:
        messages.error(request, f"Error while deleting: {str(e)}")
    if request.user.is_superuser:
        return redirect('boishakh_catalogs')
    return redirect('boishakh_choice')

@login_required
def edit_boishakh_catalog(request, id):
    try:
        obj = PohelaBoishakhCatalog.objects.get(id=id)

        if request.method == 'POST':
            dr_id = request.POST.get('dr_id')
            dr_name = request.POST.get('dr_name')
            selected_image = request.POST.get('gifts')
            size = request.POST.get('size')

            if not (dr_id and dr_name and selected_image):
                messages.error(request, "All fields are required and a gift must be selected.")
                return redirect('edit_boishakh_catalog', id=id)

            
            print(selected_image)

            # # Update fields
            obj.dr_id = dr_id
            obj.dr_name = dr_name
            obj.gifts = selected_image
            obj.size=size

            obj.save()
            messages.success(request, "Gift catalog entry updated successfully.")
            if request.user.is_superuser:
                return redirect('boishakh_catalogs')
            return redirect('boishakh_choice')
        
        return render(request, 'edit_boishakh_choice.html', {
            'obj': obj
        })

    except PohelaBoishakhCatalog.DoesNotExist:
        messages.error(request, "Gift catalog entry not found.")
        if request.user.is_superuser:
            return redirect('boishakh_catalogs')
        return redirect('boishakh_choice')
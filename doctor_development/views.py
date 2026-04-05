from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DoctorDevelopment, Territory 
import csv
from django.http import HttpResponse
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required

# map gift names
IMAGE_TO_GIFT = {
    'image1': 'Araong gift card',
    'image2': 'Mega Mall gift card',
    'image3': 'Watch',
    'image4': 'Kiam 7pcs Set',
}

def dd_gift_choice(request):
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        selected_image = request.POST.get('selected_image')

        # Map image ID to actual gift title
        gift_title = IMAGE_TO_GIFT.get(selected_image)

        if not (dr_id and dr_name and gift_title):
            messages.error(request, "All fields are required and a gift must be selected.")
            return redirect('dd_gift_choice')

        try:
            territory_id = request.user.username
            # Fetch the territory based on the username
            territory = Territory.objects.get(territory=territory_id)
            print(territory)
            if not territory:
                messages.error(request, "No territory found.")
                return redirect('dd_gift_choice')

            # Save data
            DoctorDevelopment.objects.create(
                territory=territory,
                dr_id=dr_id,
                dr_name=dr_name,
                gift=gift_title
            )
            messages.success(request, f"Successfully submitted gift wish for {dr_name}.")
            return redirect('dd_gift_choice')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('dd_gift_choice')
    if request.method=='GET':
        territory_id = request.user.username
        try:
            obj = DoctorDevelopment.objects.get(territory__territory=territory_id)
        except DoctorDevelopment.DoesNotExist:
            obj = None
        if obj:
            gift_title = obj.gift
            if gift_title == 'Araong gift card':
                img = static('images/image001.png')
            elif gift_title == 'Mega Mall gift card':
                img = static('images/image002.png')
            elif gift_title == 'Watch':
                img = static('images/image003.png')
            elif gift_title == 'Kiam 7pcs Set':
                img = static('images/image004.jpeg')
            else:
                print("No image found for the gift title:", gift_title)
            return render(request, 'dd_choice.html', {'obj': obj, 'img':img})
        return render(request, 'dd_gift_choice.html')
    
@login_required
def edit_choice(request, id):
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        selected_image = request.POST.get('selected_image')
        gift_title = IMAGE_TO_GIFT.get(selected_image)

        if not (dr_id and dr_name and gift_title):
            messages.error(request, "All fields are required and a gift must be selected.")
            return redirect('edit_dd_choice', id=id)

        try:
            obj = DoctorDevelopment.objects.get(id=id)
            obj.dr_id = dr_id
            obj.dr_name = dr_name
            obj.gift = gift_title
            obj.save()
            messages.success(request, f"Successfully updated gift wish for {dr_name}.")
            if request.user.is_superuser:
                return redirect('doctor_development')
            return redirect('dd_gift_choice')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('edit_dd_choice', id=id)

    elif request.method == 'GET':
        try:
            obj = DoctorDevelopment.objects.get(id=id)
            gift_title = obj.gift
            if gift_title == 'Araong gift card':
                img = static('images/image001.png')
            elif gift_title == 'Mega Mall gift card':
                img = static('images/image002.png')
            elif gift_title == 'Watch':
                img = static('images/image003.png')
            elif gift_title == 'Kiam 7pcs Set':
                img = static('images/image004.jpeg')
            else:
                img = ''
            return render(request, 'edit_dd_choice.html', {'obj': obj, 'img': img})
        except DoctorDevelopment.DoesNotExist:
            messages.error(request, "Wish not found.")
            if request.user.is_superuser:
                return redirect('doctor_development')
            return redirect('dd_gift_choice')


def export_wishlist(request):
    """
    Export the gift wishes to a CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="gift_wishes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Territory', 'Territory Name', 'Region Name', 'Zone Name', 'Doctor ID', 'Doctor Name', 'Gift'])

    wishes = DoctorDevelopment.objects.all()
    for wish in wishes:
        writer.writerow([wish.territory.territory, wish.territory.territory_name, wish.territory.region_name,wish.territory.zone_name, wish.dr_id, wish.dr_name, wish.gift])

    return response

def admin(request):
    """
    Render the admin page with gift wishes.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('login')

    wishes = DoctorDevelopment.objects.all()
    return render(request, 'admin.html', {'wishes': wishes})
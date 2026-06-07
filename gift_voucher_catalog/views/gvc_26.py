from django.contrib import messages
from django.shortcuts import render, redirect
from core.models import Territory
from gift_voucher_catalog.models import GiftVoucherCatalog

def gift_voucher_catalog_26_form(request):
    # Safely get current territory
    user = request.user.username
    try:
        territory = Territory.objects.get(territory=user)
    except Territory.DoesNotExist:
        messages.error(request, "Territory not found for this user.")
        return redirect('home')

    if request.method == 'POST':
        try:
            dr_id = request.POST.get('dr_id')
            dr_name = request.POST.get('dr_name')
            # FIX: Match the 'name' attribute of the hidden input in HTML
            gift_choice = request.POST.get('selected_image') 

            if not (dr_id and dr_name and gift_choice):
                messages.error(request, "All fields are required.")
                return redirect('gvc_form')

            # Save data to database
            GiftVoucherCatalog.objects.update_or_create(
                territory=territory,
                defaults={
                    'dr_id': dr_id,
                    'dr_name': dr_name,
                    'gift': gift_choice # Saved as 'Apex', 'Bata', etc.
                }
            )
            
            messages.success(request, f"Successfully submitted gift choice for {dr_name}.")
            return redirect('gvc_form')
            
        except Exception as e:
            messages.error(request, f"Internal Server Error.")
            print(f"Error: {str(e)}")
            return redirect('gvc_form')

    if request.method == 'GET':
        try:
            # FIX: Filter cleanly and count records
            queryset = GiftVoucherCatalog.objects.filter(territory=territory)
            count = queryset.count()
            obj = queryset.first() if count > 0 else None
            
            return render(request, 'gvc_form.html', {'obj': obj, 'count': count})
        except Exception as e:
            messages.error(request, "An error occurred while loading the form.")
            return redirect('home')

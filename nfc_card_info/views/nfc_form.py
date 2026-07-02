from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from nfc_card_info.models import NfcCardInfo
from core.models import Territory

# Create your views here.
@login_required
def nfc_form_view(request):
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        degree = request.POST.get('degree')
        specialty = request.POST.get('specialty')
        designation = request.POST.get('designation')
        institute = request.POST.get('institute')
        
        # Validation
        if not dr_id or not dr_name or not degree or not designation or not specialty or not institute:
            error_message = "Please fill in all the fields."
            messages.error(request, error_message)
            return redirect('nfc_form')
        
        try:
            territory = Territory.objects.get(territory=request.user.username)
            NfcCardInfo.objects.create(
                territory = territory,
                dr_rpl_id = dr_id, 
                dr_name = dr_name,
                degree = degree, 
                specialty = specialty,
                designation = designation,
                institute = institute
            )
            messages.success(request, "Doctor's NFC Card info saved successfully.")
            return redirect('nfc_form')
        except Exception as e:
            print(e)
            error_message = f"An error occurred: {str(e)}"
            messages.error(request, error_message)
            return redirect('nfc_form')
        
    try:
        territory = Territory.objects.get(territory=request.user.username)
        objects = NfcCardInfo.objects.filter(territory = territory)
        obj_count = objects.count()
    except Territory.DoesNotExist():
        messages.error(request, 'Terriotry not found!')
    
    if obj_count >= 1:
        messages.success(request, 'You have already added five(5) doctor info.')
        return redirect('nfc_history')
    return render(request, 'nfc_form.html')


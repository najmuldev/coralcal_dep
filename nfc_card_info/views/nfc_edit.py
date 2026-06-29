from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from nfc_card_info.models import NfcCardInfo
from core.models import Territory, UserProfile
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
@login_required
def nfc_edit_view(request, pk):
    obj = get_object_or_404(NfcCardInfo, pk=pk)

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
            return redirect('nfc_edit', pk=pk)

        # Update DoctorOpinion fields
        obj.dr_rpl_id = dr_id
        obj.dr_name = dr_name
        obj.degree = degree
        obj.specialty = specialty
        obj.designation = designation
        obj.institute = institute
        obj.save()

        messages.success(request, "Doctor's NFC Card Info updated successfully.")
        if not request.user.is_superuser:
            try:
                profile = request.user.userprofile
                if profile.user_type == 'zone' or profile.user_type == 'region':
                    return redirect('nfc_admin')
                else:
                    return redirect('nfc_history')
            except UserProfile.DoesNotExist:
                return redirect('nfc_history')
        return redirect('nfc_admin')

    # For GET method: pre-fill data
    # existing_indications = list(obj.indications.values_list('indication_text', flat=True))
    specialties = [
        "Medicine", "GP", "Gynaecology", "Orthopedic", "Neurology", "Dentist",
        "Diabetologist", "ENT", "Surgery", "Nephro-Urology", "Cardiology",
        "Oncology", "Skin-VD", "Pediatric", "Rheumatology", "Eye", "Endocrinology", "Psychology"
    ]
    context = {
        'obj': obj,
        'specialties': specialties
    }
    return render(request, 'nfc_edit.html', context)

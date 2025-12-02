from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DoctorAiCourse
from core.models import Territory
from django.db.models import Q
import openpyxl
from django.http import HttpResponse

# Create your views here.
def dac_form(request):
    try:
        territory = Territory.objects.get(territory=request.user.username)
    except Exception as e:
        messages.error(request, f"Error getting territory: {str(e)}")
        return redirect('home')
    
    try:
        doctor = DoctorAiCourse.objects.get(territory = territory)
    except Exception as e:
        doctor = None
        
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        dr_specialty = request.POST.get('dr_speciality')
        dr_designation = request.POST.get('dr_designation')

        # Basic validation
        if not all([dr_id, dr_name, dr_specialty, dr_designation]):
            messages.error(request, "Please fill out all required doctor fields.")
            return render(request, 'dac_form.html', {'doctor': doctor})
        try:
            with transaction.atomic():
                obj, created = DoctorAiCourse.objects.update_or_create(
                    territory=territory,
                    defaults={
                        'rpl_id': dr_id,
                        'name': dr_name,
                        'specialty': dr_specialty,
                        'designation': dr_designation,
                    }
                )
            if created:
                messages.success(request, "Doctor created successfully!")
            else:
                messages.success(request, "Doctor updated successfully!")
            return render(request, 'dac_form.html', {'doctor': obj})
        except Exception as e:
            messages.error(request, f"Error saving doctor: {str(e)}")
            return render(request, 'dac_form.html', {'doctor': doctor})
    return render(request, 'dac_form.html', {'doctor': doctor})


@login_required
def edit_dac_form(request):
    if not request.user.is_superuser:
        return redirect('home')
    territory = request.GET.get('territory')
    
    try:
        territory = Territory.objects.get(territory=territory)
    except Exception as e:
        messages.error(request, f"Error getting territory: {str(e)}")
        return redirect('doctors_ai_course')

    try:
        doctor = DoctorAiCourse.objects.get(territory = territory)
    except Exception as e:
        messages.error(request, f"Error getting doctor: {str(e)}")
        return redirect('doctors_ai_course')
        
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        dr_specialty = request.POST.get('dr_speciality')
        dr_designation = request.POST.get('dr_designation')

        # Basic validation
        if not all([dr_id, dr_name, dr_specialty, dr_designation]):
            messages.error(request, "Please fill out all required doctor fields.")
            return render(request, 'dac_form.html', {'doctor': doctor})
        try:
            with transaction.atomic():
                obj, created = DoctorAiCourse.objects.update_or_create(
                    territory=territory,
                    defaults={
                        'rpl_id': dr_id,
                        'name': dr_name,
                        'specialty': dr_specialty,
                        'designation': dr_designation,
                    }
                )
            if created:
                messages.success(request, "Doctor created successfully!")
            else:
                messages.success(request, "Doctor updated successfully!")
            return render(request, 'dac_form.html', {'doctor': obj})
        except Exception as e:
            messages.error(request, f"Error saving doctor: {str(e)}")
            return render(request, 'dac_form.html', {'doctor': doctor})
    return render(request, 'dac_form.html', {'doctor': doctor})

@login_required
def delete_dac(request,territory):
    try:
        territory = Territory.objects.get(territory=territory)
    except Exception as e:
        messages.error(request, f"Error getting territory: {str(e)}")
        return redirect('doctors_ai_course')
    try:
        doctor = DoctorAiCourse.objects.get(territory = territory)
    except Exception as e:
        messages.error(request, f"Error getting doctor: {str(e)}")
        return redirect('doctors_ai_course')
    try:
        doctor.delete()
        messages.success(request, "Doctor deleted successfully!")
        return redirect('doctors_ai_course')
    except Exception as e:
        messages.error(request, f"Error deleting doctor: {str(e)}")
        return redirect('doctors_ai_course')
    
@login_required
def export_dac(request):
    wb = openpyxl.Workbook()

    # --- Sheet 1: Doctors ---
    ws_doctors = wb.active
    ws_doctors.title = "Doctors"
    ws_doctors.append(['RPL ID', 'Name', 'Speciality', 'Designation'])
    search_query = request.GET.get('search_query', '')

    data = DoctorAiCourse.objects.all()
    if search_query:
            data = data.filter(
                Q(rpl_id__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(specialty__icontains=search_query) |
                Q(designation__icontains=search_query)
            )
    for doc in data:
        ws_doctors.append([doc.rpl_id, doc.name, doc.specialty, doc.designation])

   

    # Set response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=ai_for_doctors.xlsx'
    wb.save(response)
    return response


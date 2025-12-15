from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DoctorAiCourseUp
from core.models import Territory, UserProfile
from django.db.models import Q
import openpyxl
from django.http import HttpResponse
from dep_admin import utils
from io import BytesIO
from core.utils import redirect_url

# Create your views here.
def dac_form(request):
    try:
        territory = Territory.objects.get(territory=request.user.username)
    except Exception as e:
        messages.error(request, f"Error getting territory: {str(e)}")
        return redirect('home')
    
    try:
        doctor = DoctorAiCourseUp.objects.filter(territory = territory)
    except Exception as e:
        doctor = None
    
    if doctor.count() >=2:
        return redirect('dac2_history')
        
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        dr_specialty = request.POST.get('dr_specialty')
        dr_designation = request.POST.get('dr_designation')

        # Basic validation
        if not all([dr_id, dr_name, dr_specialty, dr_designation]):
            messages.error(request, "Please fill out all required doctor fields.")
            return render(request, 'dac2_form.html')
        try:
            DoctorAiCourseUp.objects.create(
                territory = territory,
                name = dr_name,
                rpl_id = dr_id,
                specialty = dr_specialty,
                designation = dr_designation
            )
            messages.success(request, "Doctor saved successfully!")
            return redirect('dac2_form')
        except Exception as e:
            d = {
                'dr_id': dr_id,
                'dr_name': dr_name,
                'dr_specialty': dr_specialty,
                'dr_designation': dr_designation
            }
            messages.error(request, f"Error saving doctor: {str(e)}")
            return render(request, 'dac2_form.html', {'doctor': d})
    return render(request, 'dac2_form.html')


@login_required
def edit_dac_form(request, instance_id):
    try:
        obj = DoctorAiCourseUp.objects.get(id=instance_id)
        if request.method == 'POST':
            dr_id = request.POST.get('dr_id')
            dr_name = request.POST.get('dr_name')
            dr_specialty = request.POST.get('dr_specialty')
            dr_designation = request.POST.get('dr_designation')
            if not all([dr_id, dr_name, dr_specialty, dr_designation]):
                messages.error(request, "Please fill out all required doctor fields.")
                return render(request, 'dac2_form.html', {'doctor': obj})
            try:
                obj.rpl_id = dr_id
                obj.name = dr_name
                obj.specialty = dr_specialty
                obj.designation = dr_designation
                obj.save()
                messages.success(request, "Doctor updated successfully!")
                return redirect(redirect_url(request, 'doctors_ai_course2', 'doctors_ai_course2', 'dac2_history'))
            except Exception as e:
                d = {
                    'dr_id': dr_id,
                    'dr_name': dr_name,
                    'dr_specialty': dr_specialty,
                    'dr_designation': dr_designation
                }
                messages.error(request, f"Error updating doctor: {str(e)}")
                return render(request, 'dac2_form.html', {'doctor': d})
        return render(request, 'dac2_form.html', {'doctor': obj})
    except Exception as e:
        messages.error(request, f"Error getting doctor: {str(e)}")
        return redirect(redirect_url(request, 'doctors_ai_course2', 'doctors_ai_course2', 'dac2_history'))
    
    
@login_required
def dac2_history(request):
    try:
        territory = Territory.objects.get(territory=request.user.username)
    except Exception as e:
        messages.error(request, f"Error getting territory: {str(e)}")
        return redirect('home')
    obj = DoctorAiCourseUp.objects.filter(territory = territory)
    return render(request, 'dac2_history.html', {'obj': obj})

@login_required
def dac2_delete(request, instance_id):
    try:
        obj = DoctorAiCourseUp.objects.get(id=instance_id)
        obj.delete()
        messages.success(request, "Doctor deleted successfully!")
        return redirect(redirect_url(request, 'doctors_ai_course2', 'doctors_ai_course2', 'dac2_history'))
    except Exception as e:
        messages.error(request, f"Error deleting doctor: {str(e)}")
        return redirect(redirect_url(request, 'doctors_ai_course2', 'doctors_ai_course2', 'dac2_history'))
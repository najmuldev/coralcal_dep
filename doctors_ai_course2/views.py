from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DoctorAiCourseUp
from core.models import Territory
from django.db.models import Q
import openpyxl
from django.http import HttpResponse
from dep_admin import utils
from io import BytesIO

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
        return redirect('doctors_ai_course')
        
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        dr_specialty = request.POST.get('dr_specialty')
        dr_designation = request.POST.get('dr_designation')

        # Basic validation
        if not all([dr_id, dr_name, dr_specialty, dr_designation]):
            messages.error(request, "Please fill out all required doctor fields.")
            return render(request, 'dac_form.html', {'doctor': doctor})
        try:
            DoctorAiCourseUp.objects.create(
                territory = territory,
                name = dr_name,
                rpl_id = dr_id,
                specialty = dr_specialty,
                designation = dr_designation
            )
            messages.success(request, "Doctor saved successfully!")
            return redirect('doctors_ai_course')
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
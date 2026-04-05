from django.shortcuts import render,redirect
from .models import Doctor, Chamber
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from core.models import UserProfile
from core.utils import redirect_url
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.
def dd_form(request):
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        dr_speciality = request.POST.get('dr_speciality')
        dr_designation = request.POST.get('dr_designation')
        
        address = request.POST.getlist('chamber_address[]')
        phone = request.POST.getlist('chamber_phone[]')
        district = request.POST.getlist('district[]')
        upazila = request.POST.getlist('upazila[]')
        thana = request.POST.getlist('thana[]')
        visiting_days = request.POST.getlist('visiting_days[]')
        finalVisitingData = request.POST.get('final_visiting_data')
        finalVisitingDataList = finalVisitingData.split(' || ') if finalVisitingData else []

        # Basic validation
        if not all([dr_id, dr_name, dr_speciality, dr_designation]):
            messages.error(request, "Please fill out all required doctor fields.")
            return render(request, 'doctor_data.html')

        chamber_data = []
        for i in range(len(address)):
            if not (address[i] and phone[i] and district[i] and upazila[i] and thana[i]):
                messages.error(request, f"Please fill out all chamber fields for chamber #{i+1}.")
                return render(request, 'doctor_data.html')

            if not phone[i].startswith('01') or len(phone[i]) != 11:
                print(phone[i])
                messages.error(request, f"Invalid phone number for chamber #{i+1}. Must be 11 digits and start with '01'.")
                return render(request, 'doctor_data.html')
            

            chamber_data.append({
                'address': address[i],
                'phone': phone[i],
                'district': district[i],
                'upazila': upazila[i],
                'thana': thana[i],
                'visiting_days': finalVisitingDataList[i] if i < len(finalVisitingDataList) else ''
            })

        doctor = Doctor.objects.create(
            id = dr_id,
            name = dr_name,
            speciality = dr_speciality,
            designation = dr_designation
        )
        
        for c in chamber_data:
            Chamber.objects.create(doctor=doctor, **c)

        messages.success(request, "Doctor and chambers saved successfully!")
        return redirect('dd_form')
    return render(request, 'doctor_data.html')

@login_required
def delete_doctors_data(request, doctor_id):
    obj = get_object_or_404(Doctor, id=doctor_id)
    obj.delete()
    messages.success(request, "Doctor and associated chambers deleted successfully!")
    redirection_url = redirect_url(request, 'doctors_data', 'doctors_data', 'dd_form')
    return redirect(redirection_url)

@login_required
def edit_doctors_data(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    chambers = Chamber.objects.filter(doctor=doctor)

    days_list = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

    # Prefill visiting data
    for chamber in chambers:
        visiting_map = {}

        if chamber.visiting_days:
            parts = chamber.visiting_days.split(';')
            for p in parts:
                if ':' in p:
                    day, time = p.split(':', 1)
                    visiting_map[day.strip()] = time.strip()

        chamber.visiting_map = visiting_map

    if request.method == 'POST':
        dr_name = request.POST.get('dr_name')
        dr_speciality = request.POST.get('dr_speciality')
        dr_designation = request.POST.get('dr_designation')

        address = request.POST.getlist('chamber_address[]')
        phone = request.POST.getlist('chamber_phone[]')
        district = request.POST.getlist('district[]')
        upazila = request.POST.getlist('upazila[]')
        thana = request.POST.getlist('thana[]')

        final_visiting_data = request.POST.get('final_visiting_data', '')
        visiting_list = final_visiting_data.split('||') if final_visiting_data else []

        if not all([dr_name, dr_speciality, dr_designation]):
            messages.error(request, "Fill doctor info.")
            return render(request, 'edit_doctor_data.html', locals())

        chamber_data = []

        for i in range(len(address)):
            if not (address[i] and phone[i] and district[i] and upazila[i] and thana[i]):
                messages.error(request, f"Fill chamber {i+1}")
                return render(request, 'edit_doctor_data.html', locals())

            visiting = visiting_list[i].strip() if i < len(visiting_list) else ''

            chamber_data.append({
                'address': address[i],
                'phone': phone[i],
                'district': district[i],
                'upazila': upazila[i],
                'thana': thana[i],
                'visiting_days': visiting
            })

        doctor.name = dr_name
        doctor.speciality = dr_speciality
        doctor.designation = dr_designation
        doctor.save()

        chambers.delete()

        for c in chamber_data:
            Chamber.objects.create(doctor=doctor, **c)

        messages.success(request, "Updated successfully")
        return redirect('doctors_data')

    district_list = [
        "Dhaka","Gazipur","Narayanganj","Cumilla","Chattogram","Rajshahi",
        "Khulna","Sylhet","Barisal","Rangpur"
    ]

    return render(request, 'edit_doctor_data.html', locals())
        

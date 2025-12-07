from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import PlantModule
from core.models import Territory
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def form(request):
    if request.method == 'POST':
        territory_id = request.user
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        specialty = request.POST.get('dr_specialty')
        designation = request.POST.get('dr_designation')
        location = request.POST.get('location')
        first_flower_plant = request.POST.get('first_flower_plant')
        second_flower_plant = request.POST.get('second_flower_plant')
        third_flower_plant = request.POST.get('third_flower_plant')
        first_medicinal_plant = request.POST.get('first_medicinal_plant')
        second_medicinal_plant = request.POST.get('second_medicinal_plant')
        
        fields = (
            dr_id, dr_name, specialty, designation, location, 
            first_flower_plant, second_flower_plant, third_flower_plant, 
            first_medicinal_plant, second_medicinal_plant
        )
        
        if not all (fields):
            messages.error(request, "Please fill in all the fields.")
            return redirect('p_form')
        
        plants = f'{first_flower_plant}, {second_flower_plant}, {third_flower_plant}, {first_medicinal_plant}, {second_medicinal_plant}'
        
        try:
            territory= Territory.objects.get(territory=territory_id)
            PlantModule.objects.create(
                territory=territory,
                dr_id=dr_id,
                dr_name=dr_name,
                specialty=specialty,
                designation=designation,
                location=location,
                plants=plants
            )
            messages.success(request, "Plant data added successfully.")
            return redirect('p_form')
        except Exception as e:
            messages.error(request, "Error adding Plant data: " + str(e))
            print("Error adding Plant data: " + str(e))
            return redirect('p_form')
    
    if request.method == 'GET':
        territory_id = request.user
        try:
            territory= Territory.objects.get(territory=territory_id)
        except Exception as e:
            messages.error(request, f"Error getting territory: {str(e)}")
            return redirect('home')
        
        try:
            obj = PlantModule.objects.filter(territory=territory)
            obj_count = obj.count()
            if obj_count >= 2:
                messages.error(request, "You have exceeded the limit of 2 entries.")
                return redirect('p_history')
        except PlantModule.DoesNotExist:
            obj = None
    return render(request, 'p_form.html', {'obj': obj})

@login_required
def history(request):
    territory_id = request.user
    try:
        territory = Territory.objects.get(territory=territory_id)
        obj = PlantModule.objects.filter(territory=territory)
    except Territory.DoesNotExist:
        messages.error(request, "Territory not found.")
        return redirect('p_form')
    except PlantModule.DoesNotExist:
        obj = None
    except Exception as e:
        messages.error(request, f"Error getting PlantModule: {str(e)}")
        return redirect ('home')
    return render(request, 'p_hist.html', {'obj': obj})

@login_required
def edit(request, instance_id):
    if request.method == 'GET':
        try:
            obj = PlantModule.objects.get(id=instance_id)
            data = {}
            data['first_flower_plant'] = obj.plants.split(',')[0]
            data['second_flower_plant'] = obj.plants.split(',')[1].strip()
            data['third_flower_plant'] = obj.plants.split(',')[2].strip()
            data['first_medicinal_plant'] = obj.plants.split(',')[3].strip()
            data['second_medicinal_plant'] = obj.plants.split(',')[4].strip()
            data['dr_id'] = obj.dr_id
            data['dr_name'] = obj.dr_name
            data['specialty'] = obj.specialty
            data['designation'] = obj.designation
            data['location'] = obj.location
            return render(request, 'p_edit.html', {'obj': data})
        except PlantModule.DoesNotExist:
            messages.error(request, "Plant Module data not found.")
            return redirect('p_history')
        except Exception as e:
            messages.error(request, 'Error getting Plant Module data: ' + str(e))
            return redirect('p_history')
        
    if request.method == 'POST':
        try:
            obj = PlantModule.objects.get(id=instance_id)
            obj.dr_id = request.POST.get('dr_id')
            obj.dr_name = request.POST.get('dr_name')
            obj.specialty = request.POST.get('dr_specialty')
            obj.designation = request.POST.get('dr_designation')
            obj.location = request.POST.get('location')
            first_flower_plant = request.POST.get('first_flower_plant')
            second_flower_plant = request.POST.get('second_flower_plant')
            third_flower_plant = request.POST.get('third_flower_plant')
            first_medicinal_plant = request.POST.get('first_medicinal_plant')
            second_medicinal_plant = request.POST.get('second_medicinal_plant')
            plants = f'{first_flower_plant}, {second_flower_plant}, {third_flower_plant}, {first_medicinal_plant}, {second_medicinal_plant}'
            obj.plants = plants
            obj.save()
            messages.success(request, "Plant Module data updated successfully.")
            return redirect('p_history')
        except PlantModule.DoesNotExist:
            messages.error(request, "Plant Module data not found.")
            return redirect('p_history')
        except Exception as e:
            messages.error(request, 'Error updating Plant Module data: ' + str(e))
            return redirect('p_history')
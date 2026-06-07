import os, openpyxl
from io import BytesIO

from django.db.models import Q 
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from gift_voucher_catalog.models import GiftVoucherCatalog 
from core.models import User, UserProfile

@login_required
def gvc_admin_form(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        page_number = int(request.GET.get('page') or 1)
        per_page = int(request.GET.get("per_page") or 10)
        sort = request.GET.get("sort", "territory")
        direction = request.GET.get("direction", "asc")
        # Get data using the utils function
        data = filter_gift_catalogs_data(request)
        paginator = Paginator(data, per_page)
        page_obj = paginator.get_page(page_number)    
    return render(request, 'gvc_admin.html',{'data':page_obj, 'search_query':search_query, 'per_page':per_page, 'sort':sort, 'direction':direction}) 

@login_required
def gvc_delete(request, id):
    try:
        obj = GiftVoucherCatalog.objects.get(id=id)
        obj.delete()
        messages.success(request, "Gift catalog entry deleted successfully.")
    except GiftVoucherCatalog.DoesNotExist:
        messages.error(request, "Gift catalog entry not found.")
    except Exception as e:
        messages.error(request, f"Error while deleting: {str(e)}")
    if request.user.is_superuser:
        return redirect('gvc_admin')
    return redirect('home')
    

@login_required 
def gvc_export(request):
    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Gift Voucher Catalogue"
    
    # Define the header row
    headers = ['Dr. RPL ID', 'Dr. Name', 'Territory ID', 'Territory Name', 'Region', 'Zone', 'Gift Choice']
    worksheet.append(headers)
    data = filter_gift_catalogs_data(request)
    # Populate the worksheet with data
    for obj in data:
        row = [
            obj.dr_id,
            obj.dr_name,
            obj.territory.territory,
            obj.territory.territory_name,
            obj.territory.region_name,
            obj.territory.zone_name,
            obj.gift
        ]
        worksheet.append(row)
    
    # Save the workbook to a BytesIO object
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    
    # Create a response with the Excel file
    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="gift_voucher_catalogue.xlsx"'
    
    return response


def filter_gift_catalogs_data(request, model=None):
    if model:
        data = model.objects.select_related('territory').all()
    else:
        data = GiftVoucherCatalog.objects.select_related('territory').all()
    # Filter based on the User's profile.
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone':
            data = data.filter(territory__zone_name = profile.zone_name)
        elif profile.user_type == 'region':
            data = data.filter(territory__region_name = profile.region_name)
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            data = GiftVoucherCatalog.objects.none()
    
    # Filter Based on search query
    search_query = request.GET.get('search', '')
    if search_query:
        data = data.filter(
            Q(dr_id__icontains=search_query) |
            Q(dr_name__icontains=search_query) |
            Q(territory__territory__icontains=search_query) |
            Q(territory__territory_name__icontains=search_query) |
            Q(territory__region_name__icontains=search_query) |
            Q(territory__zone_name__icontains=search_query) | 
            Q(gift__icontains=search_query)
        )
    
    # Soring
    sort = request.GET.get("sort", "territory")
    direction = request.GET.get("direction", "asc")
    sort_by = sort
    if sort_by == "territory":
        sort_by = "territory__territory"
    elif sort_by == "territory_name":
        sort_by = "territory__territory_name"
    elif sort_by == "region":
        sort_by = "territory__region_name"
    elif sort_by == "zone":
        sort_by = "territory__zone_name"
    elif sort_by == "dr_id":
        sort_by = "dr_id"
    elif sort_by == "dr_name":
        sort_by = "dr_name"
    if direction == "desc":
        sort_by = f"-{sort_by}"
    data = data.order_by(sort_by)
    
    return data
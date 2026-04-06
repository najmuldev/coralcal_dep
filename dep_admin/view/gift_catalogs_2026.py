from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import openpyxl , os, zipfile, shutil, json
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from dep_admin.models import AccessControl
from openpyxl.styles import Alignment
from doctors_data.models import Doctor, Chamber
from dep_admin import utils
import tempfile
import os
from django.core.management import call_command
from gift_catalogs_2.models import GiftCatalog2

@login_required
def gift_catalogs(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        page_number = int(request.GET.get('page') or 1)
        per_page = int(request.GET.get("per_page") or 10)
        sort = request.GET.get("sort", "territory")
        direction = request.GET.get("direction", "asc")
        # Get data using the utils function
        data = utils.filter_gift_catalogs_data(request, model=GiftCatalog2)
        paginator = Paginator(data, per_page)
        page_obj = paginator.get_page(page_number)    
    return render(request, 'gift_catalogs_2026.html',{'data':page_obj, 'search_query':search_query, 'per_page':per_page, 'sort':sort, 'direction':direction}) 

@login_required 
def export_gift_catalogs(request):
    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Gift Catalogs 2026 Data"
    
    # Define the header row
    headers = ['Dr. RPL ID', 'Dr. Name', 'Territory ID', 'Territory Name', 'Region', 'Zone', 'Gift Choice']
    worksheet.append(headers)
    data = utils.filter_gift_catalogs_data(request, data=GiftCatalog2)
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
    response['Content-Disposition'] = 'attachment; filename="gift_catalogs_2026_data.xlsx"'
    
    return response
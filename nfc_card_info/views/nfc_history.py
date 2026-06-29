from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from nfc_card_info.models import NfcCardInfo
from core.models import Territory, UserProfile
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
@login_required
def nfc_history_view(request):
    search_query = request.GET.get("search", "")
    sort = request.GET.get("sort", "created_at")
    direction = request.GET.get("direction", "desc")
    per_page = int(request.GET.get("per_page", 10))
    page = request.GET.get("page", 1)
    
    # sorting logic
    if direction == "desc":
        sort = f"-{sort}"
    
    nfc_card_info = NfcCardInfo.objects.filter(territory=Territory.objects.get(territory=request.user.username))
    
    #search filter
    if search_query:
        nfc_card_info = nfc_card_info.filter(
            Q(dr_rpl_id__icontains=search_query) |
            Q(dr_name__icontains=search_query) |
            Q(degree__icontains= search_query) |
            Q(specialty__icontains=search_query) | 
            Q(institute__icontains=search_query)
        )
    # sorting
    nfc_card_info = nfc_card_info.order_by(sort)
    
    # pagination
    paginator = Paginator(nfc_card_info, per_page)
    page_obj = paginator.get_page(page)
    
    context = {
        'data': page_obj,
        'search_query': search_query,
        'sort': sort,
        'direction': direction,
        'per_page': per_page,
        'page': page,
    }
    
    return render(request, 'nfc_history.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from nfc_card_info.models import NfcCardInfo
from core.models import Territory, UserProfile
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
@login_required
def nfc_delete_view(request, pk):
    try:
        obj = get_object_or_404(NfcCardInfo, pk=pk)
        obj.delete()
        messages.success(request, "Doctor's NFC Card Info deleted successfully.")
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
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
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

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gift_catalogs_2.models import GiftCatalog2

@login_required
def delete_gift_catalog(request, id):
    """
    Delete a gift catalog entry and its associated conference image folder if applicable.
    """
    try:
        obj = GiftCatalog2.objects.get(id=id)
        obj.delete()
        messages.success(request, "Gift catalog entry deleted successfully.")

    except GiftCatalog2.DoesNotExist:
        messages.error(request, "Gift catalog entry not found.")
    except Exception as e:
        messages.error(request, f"Error while deleting: {str(e)}")
    if request.user.is_superuser:
        return redirect('gift_catalogs_2026')
    return redirect('home')
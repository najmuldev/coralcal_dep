from django.db import models
from core.models import Territory

# Create your models here.
class NfcCardInfo(models.Model):
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    dr_rpl_id = models.CharField(max_length=10, unique=True)
    dr_name = models.CharField(max_length=155)
    degree = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    institute = models.CharField(max_length=255)
    designation = models.CharField(max_length=155)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = "nfc_card_info"
        verbose_name = "NFC Card Info"
        verbose_name_plural = "NFC Card Infos"
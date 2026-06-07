from django.db import models
from core.models import Territory

# Create your models here.
class GiftVoucherCatalog(models.Model):
    """
    Model to represent a doctor's gift catalog.
    """
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, related_name='gift_voucher_catalogs_26')
    dr_id = models.CharField(max_length=20, unique=True)
    dr_name = models.CharField(max_length=100, blank=True, null=True)
    class Gift(models.TextChoices):
        GIFT1 = 'Apex', 'Apex'
        GIFT2 = 'Bata', 'Bata'
        GIFT3 = 'Infinity', 'Infinity'
        GIFT4 = 'Aarong', 'Aarong'
    gift = models.CharField(max_length=255, choices=Gift.choices, null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dr_name} - ({self.territory})"
    
    class Meta:
        db_table = 'gift_voucher_catalogs_26'
        verbose_name = "Doctor Gift Voucher Catalog 26"
        verbose_name_plural = "Doctor Gift Voucher Catalogs 26"
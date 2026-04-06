from django.db import models
from core.models import Territory

# Create your models here.
class GiftCatalog2(models.Model):
    """
    Model to represent a doctor's gift catalog.
    """
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, related_name='gift_catalogs_2')
    dr_id = models.CharField(max_length=20, unique=True)
    dr_name = models.CharField(max_length=100, blank=True, null=True)
    class Gift(models.TextChoices):
        GIFT1 = 'President Trolley Bag- 9595', 'President Trolley Bag- 9595'
        GIFT2 = 'Philips 1000 Series 4.2 Liter Air Fryer', 'Philips 1000 Series 4.2 Liter Air Fryer'
        GIFT3 = 'Aarong Gift Voucher', 'Aarong Gift Voucher'
        GIFT4 = 'Infinity Gift Voucher', 'Infinity Gift Voucher'
        GIFT5 = 'Apex Gift Voucher', 'Apex Gift Voucher'
        GIFT6 = 'Kiam Induction cooker (H-22) & 4Pc Cookware Combo', 'Kiam Induction cooker (H-22) & 4Pc Cookware Combo'
    gift = models.CharField(max_length=255, choices=Gift.choices, default=Gift.GIFT1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dr_name} - ({self.territory})"
    
    class Meta:
        db_table = 'gift_catalogs_2'
        verbose_name = "Doctor Gift Catalog 2"
        verbose_name_plural = "Doctor Gift Catalogs 2"
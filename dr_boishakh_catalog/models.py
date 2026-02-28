from django.db import models
from core.models import Territory

# Create your models here.
class PohelaBoishakhCatalog(models.Model):
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE,)
    dr_id = models.CharField(max_length=20, unique=True)
    dr_name = models.CharField(max_length=100, blank=True, null=True)
    class Sizes(models.TextChoices):
        SM= "SM/38"
        L= "L/40"
        XL= "XL/42"
        XXL= "XXL/44"
        XXXl= "XXXL/46"
    size = models.CharField(max_length=20, choices=Sizes.choices, default=Sizes.L)
    gifts = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dr_name} - ({self.territory})"
    
    class Meta:
        db_table = 'pohela_boishakh_catalogs'
        verbose_name = "Pohela Boishakh Catalog"
        verbose_name_plural = "Pohela Boishakh Catalogs"

from django.db import models
from core.models import Territory

# Create your models here.
class PlantModule(models.Model):
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    dr_id = models.CharField(max_length=20, unique=True)
    dr_name = models.CharField(max_length=100, blank=True, null=True)
    specialty = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    plants = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'plant_module'
        verbose_name = 'Plant Module'
        verbose_name_plural = 'Plant Module'
        
    def __str__(self):
        return self.dr_id + self.dr_name
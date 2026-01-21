from django.db import models
from core.models import Territory

# Create your models here.
# Create your models here.
class DoctorDevelopment(models.Model):
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    dr_id = models.CharField(max_length=20, unique=True)
    dr_name = models.CharField(max_length=100, blank=True, null=True)
    class Gift(models.TextChoices):
        Gift1 = 'Araong gift card', 'araong gift card'
        Gift2 = 'Mega Mall gift card', 'Mega Mall gift card'
        Gift3 = 'Watch', 'Watch',
        Gift4 = 'Kiam 7pcs set', 'Kiam 7pcs set',
    gift = models.CharField(max_length=100, choices=Gift.choices, default=Gift.Gift1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dr_name

    class Meta:
        db_table = 'doctor_development'
        verbose_name = "Doctor Develop 1Q26"
        verbose_name_plural = "Doctors Develop 1Q26"
from django.db import models
from core.models import Territory
# Create your models here.
class DoctorAiCourse(models.Model):
    territory = models.OneToOneField(Territory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rpl_id = models.CharField(max_length=20)
    specialty = models.CharField(max_length=255)
    designation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'doctors_ai_course'
        verbose_name = 'Doctors AI Course'
        verbose_name_plural = 'Doctors AI Courses'
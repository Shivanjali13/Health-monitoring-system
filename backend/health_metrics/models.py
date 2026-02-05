from django.db import models
from django.conf import settings

# Create your models here.

class HealthMetric(models.Model):
    user = models.ForeignKey(settings.Auth_USER_MODEL, on_delete=models.CASCADE, related_name='health_metrics')
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    blood_pressure_systolic = models.IntegerField(help_text="Systolic blood pressure in mmHg")
    blood_pressure_diastolic = models.IntegerField(help_text="Diastolic blood pressure in mmHg")
    heart_rate = models.IntegerField(help_text="Heart rate in bpm")
    recorded_at = models.DateTimeField(auto_now_add=True)
    steps = models.IntegerField(default=0, help_text="Number of steps taken daily")
    
    class Meta:
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['user', 'recorded_at']),
        ]
        
    def __str__(self):
        return f"{self.user.email} - {self.recorded_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
class Anomaly(models.Model):
    SEVERITY_CHOICES=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    user = models.ForeignKey(settings.Auth_USER_MODEL, on_delete=models.CASCADE, related_name='anomalies')
    metric = models.ForeignKey(HealthMetric, on_delete=models.CASCADE, related_name='anomalies')
    value = models.DecimalField(max_digits=5, decimal_places=2, help_text="Value of the anomalous metric")
    detected_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-detected_at']
        indexes = [
            models.Index(fields=['user', 'detected_at']),
        ]
        
    def __str__(self):
        return f"{self.user.email} - {self.recorded_at}"
    
class Anomaly(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    user = models.ForeignKey(settings.Auth_USER_MODEL, on_delete=models.CASCADE, related_name='anomalies')
    metric = models.ForeignKey(HealthMetric, on_delete=models.CASCADE, related_name='anomalies')
    metric_name = models.CharField(max_length=50)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    description = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-detected_at']
        verbose_name_plural = "Anomalies"
        
    def __str__(self):
        return f"{self.user.email} - {self.metric_name} - {self.severity}"
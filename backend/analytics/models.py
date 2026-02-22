from django.db import models
from django.conf import settings

class WeightPrediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weight_predictions')
    prediction_date = models.DateField()  
    predicted_weight = models.DecimalField(max_digits=5, decimal_places=2)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Prediction confidence (0-100)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-prediction_date']
        unique_together = ['user', 'prediction_date']

    def __str__(self):
        return f"{self.user.email} - {self.prediction_date}: {self.predicted_weight}kg"

class DiabetesRiskAssessment(models.Model):
    RISK_LEVELS = [
        ('LOW', 'Low Risk'),
        ('MODERATE', 'Moderate Risk'),
        ('HIGH', 'High Risk'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diabetes_assessments')
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Risk score (0-100)")
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS)
    factors = models.JSONField(help_text="Contributing risk factors")
    recommendations = models.TextField()
    assessed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-assessed_at']

    def __str__(self):
        return f"{self.user.email} - {self.risk_level} ({self.risk_score}%)"

class HealthTip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_tips')
    tip_text = models.TextField()
    category = models.CharField(max_length=50, help_text="e.g., diet, exercise, sleep")
    priority = models.IntegerField(default=1, help_text="1=low, 5=high")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.category}: {self.tip_text[:50]}"
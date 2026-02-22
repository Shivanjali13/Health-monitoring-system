from django.contrib import admin
from .models import WeightPrediction, DiabetesRiskAssessment, HealthTip

@admin.register(WeightPrediction)
class WeightPredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'prediction_date', 'predicted_weight', 'confidence_score', 'created_at')
    list_filter = ('prediction_date', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-prediction_date',)

@admin.register(DiabetesRiskAssessment)
class DiabetesRiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'risk_level', 'risk_score', 'assessed_at')
    list_filter = ('risk_level', 'assessed_at')
    search_fields = ('user__email',)
    ordering = ('-assessed_at',)

@admin.register(HealthTip)
class HealthTipAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'priority', 'is_read', 'created_at')
    list_filter = ('category', 'priority', 'is_read', 'created_at')
    search_fields = ('user__email', 'tip_text')
    ordering = ('-priority', '-created_at')
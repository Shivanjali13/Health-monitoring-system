from django.contrib import admin
from .models import HealthMetric, Anomaly

@admin.register(HealthMetric)
class HealthMetricAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'blood_glucose', 'heart_rate', 'recorded_at')
    list_filter = ('recorded_at', 'user')
    search_fields = ('user__email',)
    ordering = ('-recorded_at',)

@admin.register(Anomaly)
class AnomalyAdmin(admin.ModelAdmin):
    list_display = ('user', 'metric_name', 'severity', 'is_resolved', 'detected_at')
    list_filter = ('severity', 'is_resolved', 'detected_at')
    search_fields = ('user__email', 'description')
    ordering = ('-detected_at',)
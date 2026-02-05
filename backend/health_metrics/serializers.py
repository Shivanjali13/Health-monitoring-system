from rest_framework import serializers
from .models import HealthMetric, Anomaly

class HealthMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthMetric
        fields = '__all__'
        read_only_fields = ('user', 'recorded_at')

class HealthMetricCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthMetric
        fields = ('weight', 'blood_pressure_systolic', 'blood_pressure_diastolic', 
                  'blood_glucose', 'heart_rate', 'steps')

class AnomalySerializer(serializers.ModelSerializer):
    class Meta:
        model = Anomaly
        fields = '__all__'
        read_only_fields = ('detected_at',)
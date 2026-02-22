from rest_framework import serializers
from .models import WeightPrediction, DiabetesRiskAssessment, HealthTip

class WeightPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightPrediction
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class DiabetesRiskAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiabetesRiskAssessment
        fields = '__all__'
        read_only_fields = ('user', 'assessed_at')

class HealthTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthTip
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class HealthTipUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthTip
        fields = ('is_read',)
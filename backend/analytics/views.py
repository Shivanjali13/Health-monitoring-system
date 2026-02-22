from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.cache import cache
from datetime import datetime, timedelta

from .models import WeightPrediction, DiabetesRiskAssessment, HealthTip
from .serializers import (
    WeightPredictionSerializer, 
    DiabetesRiskAssessmentSerializer, 
    HealthTipSerializer,
    HealthTipUpdateSerializer
)
from health_metrics.models import HealthMetric, Anomaly
from .ml.weight_predictor import WeightPredictor
from .ml.diabetes_assessor import DiabetesRiskAssessor
from .ml.anomaly_detector import AnomalyDetector
from .ml.health_tips_generator import HealthTipsGenerator

class WeightPredictionView(APIView):
    """
    Generate weight predictions for the next 7 days
    """
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        cache_key = f"weight_prediction_{user.id}"
        
        # Check cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Get user's health metrics
        health_metrics = HealthMetric.objects.filter(user=user).order_by('-recorded_at')
        
        if health_metrics.count() < 3:
            return Response(
                {"error": "Insufficient data. Please log at least 3 health metric entries."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate predictions
        predictor = WeightPredictor()
        predictions = predictor.predict_future_weights(health_metrics, days_ahead=7)
        
        if not predictions:
            return Response(
                {"error": "Unable to generate predictions. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Save predictions to database
        for pred in predictions:
            WeightPrediction.objects.update_or_create(
                user=user,
                prediction_date=pred['date'],
                defaults={
                    'predicted_weight': pred['weight'],
                    'confidence_score': pred['confidence']
                }
            )
        
        # Get trend analysis
        trend = predictor.get_trend_analysis(health_metrics)
        
        response_data = {
            "predictions": predictions,
            "trend": trend,
            "current_weight": float(health_metrics.first().weight),
            "message": "Weight predictions generated successfully"
        }
        
        # Cache for 1 hour
        cache.set(cache_key, response_data, 3600)
        
        return Response(response_data)

class DiabetesRiskView(APIView):
    """
    Calculate diabetes risk assessment
    """
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        cache_key = f"diabetes_risk_{user.id}"
        
        # Check cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Get health metrics
        health_metrics = HealthMetric.objects.filter(user=user).order_by('-recorded_at')
        
        if not health_metrics.exists():
            return Response(
                {"error": "No health data found. Please log your health metrics first."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Assess risk
        assessor = DiabetesRiskAssessor()
        assessment_data = assessor.assess_risk(user, health_metrics)
        
        if not assessment_data:
            return Response(
                {"error": "Unable to assess diabetes risk."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Save assessment (convert to Decimal for database)
        from decimal import Decimal
        assessment = DiabetesRiskAssessment.objects.create(
            user=user,
            risk_score=Decimal(str(assessment_data['risk_score'])),
            risk_level=assessment_data['risk_level'],
            factors=assessment_data['factors'],
            recommendations=assessment_data['recommendations']
        )
        
        # Return response with native Python types (already handled in assessor)
        response_data = {
            "assessment_id": assessment.id,
            "risk_score": assessment_data['risk_score'],
            "risk_level": assessment_data['risk_level'],
            "factors": assessment_data['factors'],
            "recommendations": assessment_data['recommendations'],
            "assessed_at": assessment.assessed_at.isoformat()  # Convert datetime to string
        }
        
        # Cache for 6 hours
        cache.set(cache_key, response_data, 21600)
        
        return Response(response_data)

class AnomalyListView(generics.ListAPIView):
    """
    List all unresolved anomalies for the user
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = 'health_metrics.serializers.AnomalySerializer'
    
    def get_queryset(self):
        return Anomaly.objects.filter(
            user=self.request.user,
            is_resolved=False
        ).order_by('-severity', '-detected_at')

class HealthTipsView(APIView):
    """
    Generate personalized health tips
    """
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        
        # Get health data
        health_metrics = HealthMetric.objects.filter(user=user).order_by('-recorded_at')
        
        # Get latest diabetes assessment
        diabetes_assessment = DiabetesRiskAssessment.objects.filter(
            user=user
        ).order_by('-assessed_at').first()
        
        # Get active anomalies
        anomalies = Anomaly.objects.filter(
            user=user,
            is_resolved=False
        ).order_by('-severity')[:5]
        
        # Generate tips
        generator = HealthTipsGenerator()
        tips_data = generator.generate_tips(
            user, 
            health_metrics, 
            diabetes_assessment, 
            anomalies
        )
        
        # Save tips to database
        saved_tips = []
        for tip_data in tips_data:
            # Check if similar tip already exists (unread)
            existing = HealthTip.objects.filter(
                user=user,
                category=tip_data['category'],
                tip_text=tip_data['text'],  # ✅ Check exact text
                is_read=False
            ).first()
            
            if not existing:
                tip = HealthTip.objects.create(
                    user=user,
                    tip_text=tip_data['text'],
                    category=tip_data['category'],
                    priority=tip_data['priority']
                )
                saved_tips.append(tip)
        
        # Get all unread tips
        unread_tips = HealthTip.objects.filter(
            user=user,
            is_read=False
        ).order_by('-priority', '-created_at')[:10]
        
        serializer = HealthTipSerializer(unread_tips, many=True)
        
        return Response({
            "tips": serializer.data,
            "total_unread": unread_tips.count()
        })

class HealthTipDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a health tip (mark as read)
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = HealthTipSerializer
    
    def get_queryset(self):
        return HealthTip.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return HealthTipUpdateSerializer
        return HealthTipSerializer

class AnalyticsDashboardView(APIView):
    """
    Comprehensive analytics dashboard
    """
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        
        # Get latest metrics
        latest_metric = HealthMetric.objects.filter(user=user).order_by('-recorded_at').first()
        
        if not latest_metric:
            return Response(
                {"error": "No health data found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get predictions
        latest_predictions = WeightPrediction.objects.filter(
            user=user
        ).order_by('-prediction_date')[:7]
        
        # Get diabetes risk
        latest_diabetes = DiabetesRiskAssessment.objects.filter(
            user=user
        ).order_by('-assessed_at').first()
        
        # Get anomalies
        active_anomalies = Anomaly.objects.filter(
            user=user,
            is_resolved=False
        ).count()
        
        # Get unread tips
        unread_tips = HealthTip.objects.filter(
            user=user,
            is_read=False
        ).count()
        
        return Response({
            "weight_predictions": WeightPredictionSerializer(latest_predictions, many=True).data,
            "diabetes_risk": DiabetesRiskAssessmentSerializer(latest_diabetes).data if latest_diabetes else None,
            "active_anomalies": active_anomalies,
            "unread_tips": unread_tips,
            "last_updated": latest_metric.recorded_at
        })
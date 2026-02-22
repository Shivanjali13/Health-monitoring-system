from celery import shared_task
from django.contrib.auth import get_user_model
from health_metrics.models import HealthMetric
from .ml.anomaly_detector import AnomalyDetector
from .ml.health_tips_generator import HealthTipsGenerator
from .models import HealthTip, DiabetesRiskAssessment
from .ml.diabetes_assessor import DiabetesRiskAssessor

User = get_user_model()

@shared_task
def detect_anomalies_task(metric_id):
    """
    Background task to detect anomalies
    """
    try:
        metric = HealthMetric.objects.get(id=metric_id)
        user = metric.user
        
        health_metrics = HealthMetric.objects.filter(
            user=user
        ).order_by('-recorded_at')
        
        detector = AnomalyDetector()
        anomalies = detector.detect_anomalies(user, metric, health_metrics)
        
        return f"Detected {len(anomalies)} anomalies for user {user.email}"
    
    except HealthMetric.DoesNotExist:
        return f"Metric {metric_id} not found"
    except Exception as e:
        return f"Error: {str(e)}"

@shared_task
def generate_daily_health_tips():
    """
    Generate daily health tips for all active users
    """
    users = User.objects.filter(is_active=True)
    tips_generated = 0
    
    for user in users:
        try:
            health_metrics = HealthMetric.objects.filter(
                user=user
            ).order_by('-recorded_at')
            
            if not health_metrics.exists():
                continue
            
            # Get diabetes assessment
            diabetes = DiabetesRiskAssessment.objects.filter(
                user=user
            ).order_by('-assessed_at').first()
            
            # Generate tips
            generator = HealthTipsGenerator()
            tips_data = generator.generate_tips(user, health_metrics, diabetes)
            
            # Save tips
            for tip_data in tips_data[:3]:  # Save top 3 tips
                HealthTip.objects.create(
                    user=user,
                    tip_text=tip_data['text'],
                    category=tip_data['category'],
                    priority=tip_data['priority']
                )
                tips_generated += 1
        
        except Exception as e:
            print(f"Error generating tips for {user.email}: {e}")
            continue
    
    return f"Generated {tips_generated} tips for {users.count()} users"

@shared_task
def calculate_diabetes_risk_batch():
    """
    Calculate diabetes risk for all users (weekly task)
    """
    users = User.objects.filter(is_active=True)
    assessments_created = 0
    
    for user in users:
        try:
            health_metrics = HealthMetric.objects.filter(
                user=user
            ).order_by('-recorded_at')
            
            if not health_metrics.exists():
                continue
            
            assessor = DiabetesRiskAssessor()
            assessment_data = assessor.assess_risk(user, health_metrics)
            
            if assessment_data:
                DiabetesRiskAssessment.objects.create(
                    user=user,
                    risk_score=assessment_data['risk_score'],
                    risk_level=assessment_data['risk_level'],
                    factors=assessment_data['factors'],
                    recommendations=assessment_data['recommendations']
                )
                assessments_created += 1
        
        except Exception as e:
            print(f"Error assessing risk for {user.email}: {e}")
            continue
    
    return f"Created {assessments_created} risk assessments"
import numpy as np
from datetime import datetime, timedelta
from django.db import models

class DiabetesRiskAssessor:
    """
    Assess diabetes risk based on health metrics
    Using simplified risk scoring algorithm
    """
    
    def __init__(self):
        # Risk factor weights
        self.weights = {
            'age': 0.15,
            'bmi': 0.25,
            'glucose': 0.30,
            'blood_pressure': 0.15,
            'family_history': 0.15,
        }
    
    def calculate_bmi(self, weight_kg, height_cm):
        """Calculate BMI"""
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 2)
    
    def score_age(self, age):
        """Score age risk (0-100)"""
        if age < 40:
            return 10
        elif age < 50:
            return 30
        elif age < 60:
            return 50
        else:
            return 70
    
    def score_bmi(self, bmi):
        """Score BMI risk (0-100)"""
        if bmi < 18.5:
            return 20
        elif bmi < 25:
            return 10
        elif bmi < 30:
            return 40
        elif bmi < 35:
            return 70
        else:
            return 90
    
    def score_glucose(self, glucose_mg_dl):
        """Score blood glucose risk (0-100)"""
        if glucose_mg_dl < 100:
            return 10
        elif glucose_mg_dl < 126:
            return 50  # Pre-diabetes range
        else:
            return 90  # Diabetes range
    
    def score_blood_pressure(self, systolic, diastolic):
        """Score blood pressure risk (0-100)"""
        if systolic < 120 and diastolic < 80:
            return 10
        elif systolic < 140 and diastolic < 90:
            return 40
        else:
            return 70
    
    def assess_risk(self, user, health_metrics):
        """
        Comprehensive diabetes risk assessment
        """
        if not health_metrics.exists():
            return None
        
        # Get latest metrics
        latest = health_metrics.first()
        
        # Calculate average glucose over last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_metrics = health_metrics.filter(recorded_at__gte=thirty_days_ago)
        
        if recent_metrics.exists():
            avg_glucose = float(recent_metrics.aggregate(
                avg=models.Avg('blood_glucose')
            )['avg'] or 0)
            avg_systolic = float(recent_metrics.aggregate(
                avg=models.Avg('blood_pressure_systolic')
            )['avg'] or 0)
            avg_diastolic = float(recent_metrics.aggregate(
                avg=models.Avg('blood_pressure_diastolic')
            )['avg'] or 0)
        else:
            avg_glucose = float(latest.blood_glucose)
            avg_systolic = float(latest.blood_pressure_systolic)
            avg_diastolic = float(latest.blood_pressure_diastolic)
        
        # Calculate BMI
        weight = float(latest.weight)
        height = float(user.height) if user.height else 170.0  # Default height
        bmi = self.calculate_bmi(weight, height)
        
        # Get age
        age = int(user.age) if user.age else 30  # Default age
        
        # Calculate individual scores
        age_score = self.score_age(age)
        bmi_score = self.score_bmi(bmi)
        glucose_score = self.score_glucose(avg_glucose)
        bp_score = self.score_blood_pressure(avg_systolic, avg_diastolic)
        
        # Weighted risk score
        risk_score = float(
            age_score * self.weights['age'] +
            bmi_score * self.weights['bmi'] +
            glucose_score * self.weights['glucose'] +
            bp_score * self.weights['blood_pressure']
        )
        
        # Determine risk level
        if risk_score < 30:
            risk_level = 'LOW'
        elif risk_score < 60:
            risk_level = 'MODERATE'
        else:
            risk_level = 'HIGH'
        
        # Identify risk factors (all as Python native types)
        factors = {
            'bmi': {
                'value': float(bmi),
                'score': float(bmi_score),
                'status': 'normal' if bmi < 25 else 'high'
            },
            'glucose': {
                'value': float(avg_glucose),
                'score': float(glucose_score),
                'status': 'normal' if avg_glucose < 100 else 'elevated'
            },
            'blood_pressure': {
                'systolic': float(avg_systolic),
                'diastolic': float(avg_diastolic),
                'score': float(bp_score),
                'status': 'normal' if avg_systolic < 120 else 'elevated'
            },
            'age': {
                'value': int(age),
                'score': float(age_score)
            }
        }
        
        # Generate recommendations
        recommendations = self.generate_recommendations(factors, risk_level)
        
        return {
            'risk_score': float(round(risk_score, 2)),
            'risk_level': risk_level,
            'factors': factors,
            'recommendations': recommendations
        }
    
    def generate_recommendations(self, factors, risk_level):
        """Generate personalized recommendations"""
        recommendations = []
        
        if factors['bmi']['status'] == 'high':
            recommendations.append("Consider a balanced diet and regular exercise to achieve a healthy BMI (18.5-24.9).")
        
        if factors['glucose']['status'] == 'elevated':
            recommendations.append("Monitor blood glucose regularly. Reduce sugar and refined carbohydrate intake.")
            recommendations.append("Consult your healthcare provider about glucose management.")
        
        if factors['blood_pressure']['status'] == 'elevated':
            recommendations.append("Monitor blood pressure regularly. Reduce sodium intake and manage stress.")
        
        if risk_level == 'HIGH':
            recommendations.append("⚠️ High risk detected. Please consult a healthcare professional for comprehensive evaluation.")
        elif risk_level == 'MODERATE':
            recommendations.append("Moderate risk detected. Focus on lifestyle improvements and regular monitoring.")
        else:
            recommendations.append("✅ Low risk. Continue maintaining healthy habits!")
        
        recommendations.append("Regular physical activity (150 minutes/week) is recommended.")
        recommendations.append("Maintain a healthy sleep schedule (7-9 hours per night).")
        
        return '\n'.join(recommendations)
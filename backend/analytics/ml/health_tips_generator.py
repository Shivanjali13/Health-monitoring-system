import random
from datetime import datetime, timedelta

class HealthTipsGenerator:
    """
    Generate personalized health tips based on user's health metrics
    """
    
    def __init__(self):
        self.tips_database = {
            'weight_management': [
                "Aim for a balanced diet with plenty of vegetables, lean proteins, and whole grains.",
                "Track your daily calorie intake to maintain a healthy weight.",
                "Consider meal prep on weekends to make healthy eating easier during busy weekdays.",
                "Stay hydrated - sometimes thirst is mistaken for hunger.",
                "Avoid eating late at night; try to finish dinner 3 hours before bedtime.",
            ],
            'exercise': [
                "Aim for at least 150 minutes of moderate aerobic activity per week.",
                "Include strength training exercises at least twice a week.",
                "Take the stairs instead of the elevator when possible.",
                "Try a 10-minute walk after meals to help with digestion and blood sugar control.",
                "Find an exercise buddy to stay motivated and accountable.",
            ],
            'blood_pressure': [
                "Reduce sodium intake to less than 2,300mg per day.",
                "Practice stress-reduction techniques like meditation or deep breathing.",
                "Limit alcohol consumption to moderate levels.",
                "Maintain a healthy weight to help control blood pressure.",
                "Monitor your blood pressure regularly at home.",
            ],
            'blood_glucose': [
                "Choose complex carbohydrates over simple sugars.",
                "Eat smaller, more frequent meals to maintain stable blood sugar.",
                "Include fiber-rich foods in your diet to slow glucose absorption.",
                "Check your blood glucose levels before and after meals to understand food impacts.",
                "Pair carbohydrates with protein or healthy fats to stabilize blood sugar.",
            ],
            'heart_health': [
                "Incorporate omega-3 fatty acids from fish, nuts, or supplements.",
                "Limit saturated and trans fats in your diet.",
                "Get at least 7-9 hours of quality sleep each night.",
                "Manage stress through yoga, meditation, or hobbies you enjoy.",
                "Quit smoking if you smoke - it's never too late to benefit.",
            ],
            'general_wellness': [
                "Stay socially connected with friends and family.",
                "Practice good sleep hygiene - keep a consistent sleep schedule.",
                "Limit screen time, especially before bed.",
                "Take breaks from sitting every hour - move and stretch.",
                "Schedule regular check-ups with your healthcare provider.",
            ],
        }
    
    def generate_tips(self, user, health_metrics, diabetes_assessment=None, anomalies=None):
        """
        Generate personalized health tips based on user data
        """
        tips = []
    
        if not health_metrics.exists():
            return self._get_default_tips()
    
        # Get latest metrics
        latest = health_metrics.first()
    
    # Get recent metrics for trend analysis
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_metrics = health_metrics.filter(recorded_at__gte=thirty_days_ago)
    
    # Analyze weight trend
        tips.extend(self._analyze_weight(user, latest, recent_metrics))
    
    # Analyze blood glucose
        tips.extend(self._analyze_glucose(latest, recent_metrics))
    
    # Analyze blood pressure
        tips.extend(self._analyze_blood_pressure(latest, recent_metrics))
    
    # Analyze heart rate
        tips.extend(self._analyze_heart_rate(latest))
    
    # Analyze activity level
        tips.extend(self._analyze_activity(latest, recent_metrics))
    
    # Add diabetes-specific tips if at risk
        if diabetes_assessment and diabetes_assessment.risk_level in ['MODERATE', 'HIGH']:
            tips.extend(self._get_diabetes_tips(diabetes_assessment.risk_level))
    
    # Add anomaly-specific tips
        if anomalies:
            tips.extend(self._get_anomaly_tips(anomalies))
    
    # Add general wellness tips
        tips.extend(self._get_general_tips())
    
    # Remove duplicates by tip text
        seen_texts = set()
        unique_tips = []
        for tip in tips:
            if tip['text'] not in seen_texts:
                seen_texts.add(tip['text'])
                unique_tips.append(tip)
    
    # Sort by priority (highest first)
        unique_tips.sort(key=lambda x: x['priority'], reverse=True)
    
    # Limit to top 5 tips
        return unique_tips[:5]
    
    def _analyze_weight(self, user, latest, recent_metrics):
        """Analyze weight trends"""
        tips = []
        
        if recent_metrics.count() < 2:
            return tips
        
        weights = list(recent_metrics.values_list('weight', flat=True))
        weights = [float(w) for w in weights]
        
        # Calculate trend
        weight_change = weights[0] - weights[-1]
        
        if weight_change > 2:  # Gained more than 2kg
            tips.append({
                'text': "Your weight has increased recently. " + random.choice(self.tips_database['weight_management']),
                'category': 'weight_management',
                'priority': 4
            })
        elif weight_change < -2:  # Lost more than 2kg
            if user.height:
                bmi = self._calculate_bmi(weights[0], float(user.height))
                if bmi < 18.5:
                    tips.append({
                        'text': "Your weight loss may be excessive. Consider consulting a nutritionist.",
                        'category': 'weight_management',
                        'priority': 5
                    })
        
        return tips
    
    def _analyze_glucose(self, latest, recent_metrics):
        """Analyze blood glucose levels"""
        tips = []
        
        glucose = float(latest.blood_glucose)
        
        if glucose > 126:  # Diabetes range
            tips.append({
                'text': "⚠️ Your blood glucose is in the diabetes range. Please consult your doctor immediately.",
                'category': 'blood_glucose',
                'priority': 5
            })
        elif glucose > 100:  # Pre-diabetes range
            tips.append({
                'text': random.choice(self.tips_database['blood_glucose']),
                'category': 'blood_glucose',
                'priority': 4
            })
        
        # Check for high variability
        if recent_metrics.count() >= 5:
            glucose_values = [float(g) for g in recent_metrics.values_list('blood_glucose', flat=True)]
            import numpy as np
            std_dev = np.std(glucose_values)
            
            if std_dev > 15:  # High variability
                tips.append({
                    'text': "Your blood glucose levels show high variability. Try to maintain consistent meal times and portions.",
                    'category': 'blood_glucose',
                    'priority': 3
                })
        
        return tips
    
    def _analyze_blood_pressure(self, latest, recent_metrics):
        """Analyze blood pressure"""
        tips = []
        
        systolic = latest.blood_pressure_systolic
        diastolic = latest.blood_pressure_diastolic
        
        if systolic >= 140 or diastolic >= 90:  # Hypertension
            tips.append({
                'text': "⚠️ Your blood pressure is elevated. " + random.choice(self.tips_database['blood_pressure']),
                'category': 'blood_pressure',
                'priority': 5
            })
        elif systolic >= 130 or diastolic >= 85:  # Pre-hypertension
            tips.append({
                'text': random.choice(self.tips_database['blood_pressure']),
                'category': 'blood_pressure',
                'priority': 3
            })
        
        return tips
    
    def _analyze_heart_rate(self, latest):
        """Analyze heart rate"""
        tips = []
        
        hr = latest.heart_rate
        
        if hr > 100:  # Tachycardia
            tips.append({
                'text': "Your resting heart rate is elevated. Consider stress management and regular exercise.",
                'category': 'heart_health',
                'priority': 3
            })
        elif hr < 60:  # Bradycardia (but could be normal for athletes)
            tips.append({
                'text': "Your heart rate is low. If you're not an athlete, consider discussing this with your doctor.",
                'category': 'heart_health',
                'priority': 2
            })
        
        return tips
    
    def _analyze_activity(self, latest, recent_metrics):
        """Analyze physical activity"""
        tips = []
        
        steps = latest.steps
        
        if steps < 5000:
            tips.append({
                'text': random.choice(self.tips_database['exercise']),
                'category': 'exercise',
                'priority': 3
            })
        elif steps > 15000:
            tips.append({
                'text': "Great job on staying active! Remember to include rest days to prevent injury.",
                'category': 'exercise',
                'priority': 1
            })
        
        return tips
    
    def _get_diabetes_tips(self, risk_level):
        """Get diabetes-specific tips"""
        tips = []
        
        if risk_level == 'HIGH':
            tips.append({
                'text': "⚠️ High diabetes risk detected. Schedule a comprehensive evaluation with your doctor.",
                'category': 'blood_glucose',
                'priority': 5
            })
        
        tips.append({
            'text': random.choice(self.tips_database['blood_glucose']),
            'category': 'blood_glucose',
            'priority': 4
        })
        
        return tips
    
    def _get_anomaly_tips(self, anomalies):
        """Get tips based on detected anomalies"""
        tips = []
        
        for anomaly in anomalies[:3]:  # Top 3 anomalies
            if anomaly.severity in ['HIGH', 'MEDIUM']:
                tips.append({
                    'text': f"⚠️ {anomaly.description} Consider consulting your healthcare provider.",
                    'category': 'anomaly_alert',
                    'priority': 5 if anomaly.severity == 'HIGH' else 4
                })
        
        return tips
    
    def _get_general_tips(self):
        """Get general wellness tips"""
        return [{
            'text': random.choice(self.tips_database['general_wellness']),
            'category': 'general_wellness',
            'priority': 1
        }]
    
    def _get_default_tips(self):
        """Get default tips for new users"""
        return [
            {
                'text': "Welcome! Start by logging your daily health metrics consistently.",
                'category': 'general_wellness',
                'priority': 3
            },
            {
                'text': random.choice(self.tips_database['exercise']),
                'category': 'exercise',
                'priority': 2
            },
            {
                'text': random.choice(self.tips_database['general_wellness']),
                'category': 'general_wellness',
                'priority': 1
            }
        ]
    
    def _calculate_bmi(self, weight_kg, height_cm):
        """Calculate BMI"""
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)

import numpy as np
from datetime import datetime, timedelta
from health_metrics.models import Anomaly

class AnomalyDetector:
    """
    Detect anomalies in health metrics using statistical methods
    """
    
    def __init__(self):
        self.threshold_multiplier = 2.5  # Standard deviations for anomaly
    
    def detect_anomalies(self, user, latest_metric, health_metrics):
        """
        Detect anomalies in the latest health metric
        """
        if health_metrics.count() < 5:
            return []  # Need baseline data
        
        anomalies = []
        
        # Get historical data (last 30 days, excluding latest)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        historical = health_metrics.filter(
            recorded_at__gte=thirty_days_ago
        ).exclude(id=latest_metric.id)
        
        if historical.count() < 3:
            return []
        
        # Check each metric
        metrics_to_check = [
            ('weight', 'Weight'),
            ('blood_pressure_systolic', 'Systolic Blood Pressure'),
            ('blood_pressure_diastolic', 'Diastolic Blood Pressure'),
            ('blood_glucose', 'Blood Glucose'),
            ('heart_rate', 'Heart Rate'),
        ]
        
        for field, display_name in metrics_to_check:
            anomaly = self.check_metric_anomaly(
                user, latest_metric, historical, field, display_name
            )
            if anomaly:
                anomalies.append(anomaly)
        
        return anomalies
    
    def check_metric_anomaly(self, user, latest_metric, historical, field, display_name):
        """
        Check if a specific metric is anomalous
        """
        # Get historical values
        historical_values = list(historical.values_list(field, flat=True))
        historical_values = [float(v) for v in historical_values]
        
        # Calculate statistics
        mean = np.mean(historical_values)
        std = np.std(historical_values)
        
        # Get current value
        current_value = float(getattr(latest_metric, field))
        
        # Calculate z-score
        if std == 0:
            return None
        
        z_score = abs((current_value - mean) / std)
        
        # Detect anomaly
        if z_score > self.threshold_multiplier:
            # Determine severity
            if z_score > 4:
                severity = 'HIGH'
            elif z_score > 3:
                severity = 'MEDIUM'
            else:
                severity = 'LOW'
            
            # Determine direction
            if current_value > mean:
                direction = 'increased'
                comparison = f"{current_value:.2f} vs average {mean:.2f}"
            else:
                direction = 'decreased'
                comparison = f"{current_value:.2f} vs average {mean:.2f}"
            
            description = (
                f"{display_name} has {direction} significantly. "
                f"Current: {comparison}. "
                f"This is {z_score:.1f} standard deviations from your normal range."
            )
            
            # Create or get anomaly
            anomaly, created = Anomaly.objects.get_or_create(
                user=user,
                metric=latest_metric,
                metric_name=field,
                defaults={
                    'severity': severity,
                    'description': description,
                }
            )
            
            return anomaly
        
        return None
    
    def get_critical_anomalies(self, user):
        """
        Get unresolved critical anomalies
        """
        return Anomaly.objects.filter(
            user=user,
            is_resolved=False,
            severity__in=['HIGH', 'MEDIUM']
        ).order_by('-detected_at')[:5]
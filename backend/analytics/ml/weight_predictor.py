import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import joblib
import os
from django.conf import settings
from django.db import models

class WeightPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'weight_predictor.pkl')
        self.scaler_path = os.path.join(settings.BASE_DIR, 'ml_models', 'weight_scaler.pkl')
    
    def prepare_data(self, health_metrics):
        """
        Prepare training data from health metrics queryset
        """
        if not health_metrics.exists() or health_metrics.count() < 3:
            return None, None
        
        # Convert to pandas DataFrame
        data = []
        for metric in health_metrics:
            days_diff = (metric.recorded_at.date() - health_metrics.last().recorded_at.date()).days
            data.append({
                'days': days_diff,
                'weight': float(metric.weight),
                'steps': metric.steps,
                'heart_rate': metric.heart_rate,
            })
        
        df = pd.DataFrame(data)
        
        # Features: days, steps, heart_rate
        X = df[['days', 'steps', 'heart_rate']].values
        y = df['weight'].values
        
        return X, y
    
    def train(self, health_metrics):
        """
        Train the weight prediction model
        """
        X, y = self.prepare_data(health_metrics)
        
        if X is None:
            return False
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        return True
    
    def load_model(self):
        """
        Load trained model from disk
        """
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            return True
        return False
    
    def predict_future_weights(self, health_metrics, days_ahead=7):
        """
        Predict weights for the next N days
        """
        if health_metrics.count() < 3:
            return None
        
        # Train or load model
        if not self.load_model():
            if not self.train(health_metrics):
                return None
        
        # Get latest metrics for baseline
        latest = health_metrics.first()
        avg_steps = health_metrics.aggregate(avg_steps=models.Avg('steps'))['avg_steps'] or 5000
        avg_hr = health_metrics.aggregate(avg_hr=models.Avg('heart_rate'))['avg_hr'] or 70
        
        # Predict for next N days
        predictions = []
        last_date = latest.recorded_at.date()
        
        for day in range(1, days_ahead + 1):
            future_date = last_date + timedelta(days=day)
            
            # Prepare features
            X_future = np.array([[day, avg_steps, avg_hr]])
            X_future_scaled = self.scaler.transform(X_future)
            
            # Predict
            predicted_weight = self.model.predict(X_future_scaled)[0]
            
            # Calculate confidence (R² score approximation)
            confidence = max(0, min(100, 85 - (day * 2)))  # Decreases with time
            
            predictions.append({
                'date': future_date,
                'weight': round(predicted_weight, 2),
                'confidence': round(confidence, 2)
            })
        
        return predictions
    
    def get_trend_analysis(self, health_metrics):
        """
        Analyze weight trend (gaining, losing, stable)
        """
        if health_metrics.count() < 2:
            return 'insufficient_data'
        
        recent = list(health_metrics[:5].values_list('weight', flat=True))
        
        if len(recent) < 2:
            return 'insufficient_data'
        
        # Calculate trend
        weights = [float(w) for w in recent]
        avg_change = (weights[0] - weights[-1]) / len(weights)
        
        if avg_change > 0.2:
            return 'gaining'
        elif avg_change < -0.2:
            return 'losing'
        else:
            return 'stable'
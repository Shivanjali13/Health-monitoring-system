from django.urls import path
from .views import (
    WeightPredictionView,
    DiabetesRiskView,
    AnomalyListView,
    HealthTipsView,
    HealthTipDetailView,
    AnalyticsDashboardView,
)

urlpatterns = [
    path('weight-prediction/', WeightPredictionView.as_view(), name='weight-prediction'),
    path('diabetes-risk/', DiabetesRiskView.as_view(), name='diabetes-risk'),
    path('anomalies/', AnomalyListView.as_view(), name='anomalies-list'),
    path('health-tips/', HealthTipsView.as_view(), name='health-tips'),
    path('health-tips/<int:pk>/', HealthTipDetailView.as_view(), name='health-tip-detail'),
    path('dashboard/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
]
from django.urls import path
from .views import (
    HealthMetricListCreateView,
    HealthMetricDetailView,
    UserAnomaliesView,
    HealthSummaryView
)

urlpatterns = [
    path('metrics/', HealthMetricListCreateView.as_view(), name='health-metrics-list'),
    path('metrics/<int:pk>/', HealthMetricDetailView.as_view(), name='health-metric-detail'),
    path('anomalies/', UserAnomaliesView.as_view(), name='user-anomalies'),
    path('summary/', HealthSummaryView.as_view(), name='health-summary'),
]
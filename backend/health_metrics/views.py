from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.cache import cache
from .models import HealthMetric, Anomaly
from .serializers import HealthMetricSerializer, HealthMetricCreateSerializer, AnomalySerializer

class HealthMetricListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return HealthMetric.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return HealthMetricCreateSerializer
        return HealthMetricSerializer
    
    def perform_create(self, serializer):
        metric = serializer.save(user=self.request.user)
        # Trigger anomaly detection (we'll implement this in ML section)
        from analytics.tasks import detect_anomalies
        detect_anomalies.delay(metric.id)

class HealthMetricDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HealthMetricSerializer
    
    def get_queryset(self):
        return HealthMetric.objects.filter(user=self.request.user)

class UserAnomaliesView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnomalySerializer
    
    def get_queryset(self):
        return Anomaly.objects.filter(user=self.request.user, is_resolved=False)

class HealthSummaryView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        cache_key = f"health_summary_{request.user.id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        metrics = HealthMetric.objects.filter(user=request.user).order_by('-recorded_at')[:30]
        
        if not metrics.exists():
            return Response({"message": "No health data available"}, status=status.HTTP_404_NOT_FOUND)
        
        latest = metrics.first()
        summary = {
            "latest_metrics": HealthMetricSerializer(latest).data,
            "total_records": metrics.count(),
            "active_anomalies": Anomaly.objects.filter(user=request.user, is_resolved=False).count()
        }
        
        cache.set(cache_key, summary, 300)  # Cache for 5 minutes
        return Response(summary)
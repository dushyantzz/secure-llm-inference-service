from fastapi import APIRouter, Depends, Response
from app.metrics import metrics_tracker
from app.auth import get_current_user
import prometheus_client

router = APIRouter()

@router.get("/metrics/prometheus")
async def prometheus_metrics(current_user = Depends(get_current_user)):
    # For demo: convert metrics_tracker data to Prometheus text format
    data = metrics_tracker.get_metrics()
    # Define Prometheus metrics
    response_count = prometheus_client.Gauge('total_requests', 'Total API requests')
    successful_requests = prometheus_client.Gauge('successful_requests', 'Successful requests')
    failed_requests = prometheus_client.Gauge('failed_requests', 'Failed requests')
    avg_latency = prometheus_client.Gauge('average_latency_ms', 'Average Latency (ms)')
    p95_latency = prometheus_client.Gauge('p95_latency_ms', '95th Percentile Latency (ms)')

    response_count.set(data.get('total_requests', 0))
    successful_requests.set(data.get('successful_requests', 0))
    failed_requests.set(data.get('failed_requests', 0))
    avg_latency.set(data.get('average_latency_ms', 0))
    p95_latency.set(data.get('p95_latency_ms', 0))

    content = prometheus_client.generate_latest()
    return Response(content, media_type='text/plain')

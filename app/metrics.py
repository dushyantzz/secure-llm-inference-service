from typing import List
from datetime import datetime
import statistics


class MetricsTracker:
    """Track performance metrics for the API"""
    
    def __init__(self):
        self.latencies: List[float] = []
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = datetime.utcnow()
    
    def record_request(self, latency_ms: float, success: bool):
        """Record a request with its latency"""
        self.latencies.append(latency_ms)
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
    
    def get_metrics(self) -> dict:
        """Get current metrics summary"""
        if not self.latencies:
            return {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "average_latency_ms": 0,
                "p95_latency_ms": 0,
                "uptime_seconds": 0
            }
        
        sorted_latencies = sorted(self.latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "average_latency_ms": round(statistics.mean(self.latencies), 2),
            "p95_latency_ms": round(sorted_latencies[p95_index], 2) if p95_index < len(sorted_latencies) else 0,
            "uptime_seconds": round(uptime, 2)
        }


metrics_tracker = MetricsTracker()
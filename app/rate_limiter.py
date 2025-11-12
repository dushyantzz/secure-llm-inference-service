from fastapi import HTTPException, status
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List
from app.config import settings


class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, List[datetime]] = defaultdict(list)
    
    def check_rate_limit(self, user_id: str) -> bool:
        """Check if user has exceeded rate limit"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=settings.RATE_LIMIT_WINDOW)
        
        # Clean old requests
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[user_id]) >= settings.RATE_LIMIT_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_WINDOW} seconds."
            )
        
        # Add current request
        self.requests[user_id].append(now)
        return True


rate_limiter = RateLimiter()
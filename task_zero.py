from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse, Response
from starlette import status
from typing import List

from utils.limiters import WindowedRateLimiter
from utils.serializers import (
    RateLimiterSerializer,
    RateLimiterResponse,
    BatchRateLimiterSerializer,
    RateLimiterResponse
)
from utils.constants import REQUEST_RATE, REQUEST_WINDOW
from openapischema import OpenApiDesc

task_zero_router = APIRouter(prefix="/api", tags=["task_zero"], default_response_class=JSONResponse)





class RateLimiterView:
    limiter = WindowedRateLimiter(rate=REQUEST_RATE, seconds=REQUEST_WINDOW)

    @task_zero_router.post(path = "/rate-limiter",
                           summary="This API mimics a fixed-window rate limiting policy by processing single request one at a time.",
                           description = OpenApiDesc.user_rate_limiter_post_desc,
                           response_model=RateLimiterResponse)
    async def rate_limiter(data: RateLimiterSerializer, response: Response):
        allow = RateLimiterView.limiter.should_allow_request(**data.model_dump())
        if not allow:
            response.status_code = status.HTTP_400_BAD_REQUEST
        
        return dict(user_id=data.user_id, allow=allow)



class BatchRateLimiterView:
    limiter = WindowedRateLimiter(rate=REQUEST_RATE, seconds=REQUEST_WINDOW)

    @task_zero_router.post(path = "/batch-rate-limiter",
                           summary="This API mimics a fixed-window rate limiting policy by processing multiple requests at a time.",
                           description = OpenApiDesc.batch_rate_limiter_post_desc,
                           response_model=List[RateLimiterResponse])
    async def batch_rate_limiter(data: BatchRateLimiterSerializer):
        allowed = list()
        for item in data.model_dump():
            allow = BatchRateLimiterView.limiter.should_allow_request(**item)
            allowed.append(dict(user_id=item["user_id"], allow=allow))
        
        return allowed

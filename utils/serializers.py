from pydantic import BaseModel, ConfigDict, PositiveInt, Field, RootModel
from typing import Optional, Any, Dict, List


class BaseSerializer(BaseModel):
    model_config = ConfigDict(extra="ignore")
    

class RateLimiterSerializer(BaseSerializer):
    user_id: str = Field(..., description="Identifier of the requesting user.", example="alice")
    timestamp: PositiveInt = Field(..., description="Request time in seconds (non-negative).", example=10)


class BatchRateLimiterSerializer(RootModel[List[RateLimiterSerializer]]):

    model_config = ConfigDict(
                    json_schema_extra={
                        "example": [
                            {"user_id": "alice", "timestamp": 1},
                            {"user_id": "bob", "timestamp": 2},
                            {"user_id": "alice", "timestamp": 10},
                            {"user_id": "charlie", "timestamp": 20},
                            {"user_id": "bob", "timestamp": 30},
                            {"user_id": "alice", "timestamp": 40},
                            {"user_id": "bob", "timestamp": 41},
                            {"user_id": "alice", "timestamp": 61}
                        ]
                    })


class BatchUserRateLimiterSerializer(RootModel[List[RateLimiterSerializer]]):

    model_config = ConfigDict(
                    json_schema_extra={
                        "example": [
                            {"user_id": "alice", "timestamp": 1},
                            {"user_id": "bob", "timestamp": 2},
                            {"user_id": "alice", "timestamp": 10},
                            {"user_id": "alice", "timestamp": 20},
                            {"user_id": "bob", "timestamp": 30},
                            {"user_id": "alice", "timestamp": 40},
                            {"user_id": "alice", "timestamp": 41},
                            {"user_id": "alice", "timestamp": 58},
                            {"user_id": "bob", "timestamp": 58},
                            {"user_id": "bob", "timestamp": 61}
                        ]
                    })



class RateLimiterResponse(BaseSerializer):
    user_id: str
    allow: bool

    
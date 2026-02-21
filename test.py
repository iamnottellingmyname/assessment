import pytest
from fastapi.testclient import TestClient
from starlette import status
from app import app
from task_zero import (
    RateLimiterView as T0RateLimiterView,
    BatchRateLimiterView as T0BatchRateLimiterView
)
from task_one import (
    RateLimiterView as T1RateLimiterView,
    BatchRateLimiterView as T1BatchRateLimiterView
)
from utils.limiters import WindowedRateLimiter, WindowedUserRateLimiter
from utils.constants import REQUEST_RATE, REQUEST_WINDOW


client = TestClient(app)


@pytest.fixture(autouse=True, scope="function")
def reset_limiter():
    T0RateLimiterView.limiter = WindowedRateLimiter(rate=REQUEST_RATE, seconds=REQUEST_WINDOW)
    T1RateLimiterView.limiter = WindowedUserRateLimiter(rate=REQUEST_RATE, seconds=REQUEST_WINDOW)
    T0BatchRateLimiterView.limiter = WindowedRateLimiter(rate=REQUEST_RATE, seconds=REQUEST_WINDOW)
    T1BatchRateLimiterView.limiter = WindowedUserRateLimiter(rate=REQUEST_RATE, seconds=REQUEST_WINDOW)


global_window_rate_data = [
        {
            "user_id": "alice",
            "timestamp": 1
        },
        {
            "user_id": "alice",
            "timestamp": 10
        },
        {
            "user_id": "alice",
            "timestamp": 20
        },
        {
            "user_id": "alice",
            "timestamp": 30
        },
        {
            "user_id": "alice",
            "timestamp": 40
        },
        {
            "user_id": "alice",
            "timestamp": 50
        }
    ]


global_user_window_rate_data=[
    {
        "timestamp": 1,
        "user_id": "alice"
    },
    {
        "timestamp": 2,
        "user_id": "bob"
    },
    {
        "timestamp": 10,
        "user_id": "alice"
    },
    {
        "timestamp": 20,
        "user_id": "alice"
    },
    {
        "timestamp": 30,
        "user_id": "bob"
    },
    {
        "timestamp": 40,
        "user_id": "alice"
    },
    {
        "timestamp": 41,
        "user_id": "alice"
    },
    {
        "timestamp": 58,
        "user_id": "alice"
    },
    {
        "timestamp": 58,
        "user_id": "bob"
    },
    {
        "timestamp": 61,
        "user_id": "bob"
    }
]


def test_global_window_rate_allowed():
    response = client.post(
        "/api/rate-limiter",
        json=global_window_rate_data[0]
    )

    assert response.status_code == 200
    assert response.json()["allow"] is True



def test_global_window_rate_unallowed():
    datlen = len(global_window_rate_data)
    for idx in range(datlen):
        response = client.post(
            "/api/rate-limiter",
            json=global_window_rate_data[idx]
        )

        data = response.json()
        if idx==(datlen-1):
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert data["allow"] is False
        else:
            assert response.status_code == status.HTTP_200_OK
            assert data["allow"] is True



def test_batch_global_window_rate_allowed():
    response = client.post(
        "/api/batch-user-rate-limiter",
        json=global_window_rate_data
    )
    
    assert response.status_code == 200
    
    results = response.json()

    assert results[0]["allow"] is True
    assert results[-1]["allow"] is False



def test_user_window_rate_allowed():
    response = client.post(
        "/api/user-rate-limiter",
        json=global_user_window_rate_data[0]
    )

    assert response.status_code == 200
    assert response.json()["allow"] is True



def test_user_window_rate_unallowed():
    datlen = len(global_user_window_rate_data)
    for idx in range(datlen):
        response = client.post(
            "/api/user-rate-limiter",
            json=global_user_window_rate_data[idx]
        )

        data = response.json()
        if idx==7:
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert data["allow"] is False
        else:
            assert response.status_code == status.HTTP_200_OK
            assert data["allow"] is True



def test_batch_user_window_rate_allowed():
    response = client.post(
        "/api/batch-user-rate-limiter",
        json=global_user_window_rate_data
    )
    
    assert response.status_code == 200
    
    results = response.json()

    assert results[0]["allow"] is True
    assert results[-3]["allow"] is False
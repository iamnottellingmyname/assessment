## Introduction

Before diving into the setup and implementation details, I would like to briefly explain why I chose FastAPI for this task instead of Django or Flask.

- **Django** would be unnecessarily heavy for this requirement. Since this task focuses solely on implementing a rate limiter, we do not require features such as ORM, admin panel, or other built-in components.

- **Flask** is lightweight and simple, but it does not provide built-in OpenAPI schema generation or automatic documentation without additional libraries.

I chose **FastAPI** because it is a high-performance ASGI-based framework that offers automatic request validation, native OpenAPI schema generation, and built-in Swagger and ReDoc documentation. This allows the implementation of a clean, production-ready API with minimal boilerplate.

## Setup

For **Windows**

Bypass execution policy and run:
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\init.ps1
```

For **Linux**

Grant execute permission and run:

```
chmod +x init.sh
./init.sh
```

>**Note:**
>If you encounter any issues while running the script, please open the respective `init` file and execute the commands manually one by one.

Once the server starts, the APIs can be accessed at:

[Swagger UI](http://127.0.0.1:8000/docs)

[Redoc UI](http://127.0.0.1:8000/redoc)

<small>Server URL: `http://127.0.0.1:8000`</small>

Manual Server Start:
```
uvicorn app:app --reload
```

Running Test Cases:
```
pytest test.py
```
<br>

>**Note:**
>Test cases are written against the current configuration in utils/constants.py.
Changing REQUEST_RATE or REQUEST_WINDOW may cause tests to fail.


## Code Assumptions

Requests are processed in non-decreasing timestamp order (which is kinda true in real-world server-side processing each request's timestamp is either the same as or greater than the previous one.)


## Code Considerations and Edge Cases

- It suffers from the **burst problem** at window boundaries, where up to 2N requests can be allowed in a short duration i.e between 55-65 time window as there you can send 10 request altough the rate was 5 request per 60 seconds.

- This implementation is not **thread safe** i.e race condition can happen 2 threads can check the count at the same time and allow both the requests.

- Since the **rate(N)** is configurable in the server side in real world scenarios kindly change it in the `utils/constants.py`


## Code Improvements

- Implement **sliding window** or **token bucket** so to overcome this burst problem

- Making it **threadsafe**

- Using **redis with proper cleanup** in the user based rate limiting, reason being that if we have multiple servers or multiple uvicorn workers, the limits get summed up



## Tools Used
- vscode (apart from vscode i like jupyter notebook as well for some tasks)
- llm (Used for discussing design improvements and edge cases)
- git (version management)
- miniconda (I personally prefer using miniconda or uv for package and virtual env management but for the simplicity used venv for this task)



## Project Structure

- task_zero.py, task_one.py – Main task implementations

- utils/limiter.py – Main Rate limiter logic

- utils/constants.py – Configuration (request rate & window size)

- app.py – FastAPI application entry point

- test.py – Test cases

- serializers – Pydantic models for validation

- openapischema.py – Helper file for detailed OpenAPI descriptions

> **Important Note:** 
>REQUEST_RATE (N) and REQUEST_WINDOW are configurable via `constants.py`. The current test cases are aligned with the existing configuration. Any changes to these values will require corresponding updates to the test cases.

## Thought Process (Additional Notes)

**Important Note:**
As per the assessment requirement, this could have been implemented as a simple Python script that reads input file and generates output file but given the enough time I opted to implement it as an API to align and mimic it more closely with how rate limiting is typically handled in real-world systems.

<hr>

Thank you for reviewing this submission :)
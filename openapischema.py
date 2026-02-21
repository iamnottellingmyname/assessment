rate_limiter_desc_template="""
## {description}

### Assumptions:
- requests are processed in non-decreasing timestamp order (which is kinda true in real-world server-side processing
  each request's timestamp is either the same as or greater than the previous one.)


### Considerations and Edge Cases:
- it suffers from the **burst problem** at window boundaries, where up to 2N requests can be allowed in a short duration
  i.e between 55-65 time window as there you can send 10 request altough the rate was 5 request per 60 seconds.
- this implementation is **not thread safe** i.e race condition can happen
  2 threads can check the count at the same time and allow both the requests.

### Improvements:
- implement **sliding window** or **token bucket** so to overcome this **burst problem**
- making it **threadsafe**
- **using redis** with proper cleanup in the user based rate limiting, reason being that if we have multiple servers or multiple uvicorn workers, the limits get summed up


**Note:** Since the rate(N) is configurable in the server side kindly change it in the utils/constants.py
"""


class OpenApiDesc:

  rate_limiter_post_desc = rate_limiter_desc_template.format(
    description = "Evaluates whether **an incoming request(single)** is permitted under the global fixed-window rate limiting policy."
  )

  batch_rate_limiter_post_desc = rate_limiter_desc_template.format(
    description = "Evaluates whether **the multiple incoming requests** are permitted under the global fixed-window rate limiting policy."
  )
 
  user_rate_limiter_post_desc = rate_limiter_desc_template.format(
    description = "Evaluates whether **an incoming request(single)** is permitted under the **user wise** fixed-window rate limiting policy."
  )

  batch_user_rate_limiter_post_desc = rate_limiter_desc_template.format(
    description = "Evaluates whether **the multiple incoming requests** are permitted under the **user wise** fixed-window rate limiting policy."
  )

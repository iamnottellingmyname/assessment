from abc import ABC, abstractmethod
from utils.serializers import RateLimiterSerializer


class AbstractRateLimiter(ABC):

    """
    A fixed-window global rate limiter Abstract implementation.
    """


    @abstractmethod
    def should_allow_request(self, user_id: str, timestamp: int) -> bool:
        """
        Evaluates whether an incoming request is permitted under the
        global fixed-window rate limiting policy.

        Enforces a maximum of `self.rate` requests per `self.second` seconds
        fixed window (computed as timestamp // provided window in seconds) across all users.
        If the request falls into a new window, the internal counter is reset.

        Args:
            user_id (str): Identifier of the requesting user.
            timestamp (int): Request time in seconds (non-negative).

        Returns:
            bool: True if the request is allowed; False if the
            current window's limit has been exceeded.

        Raises:
            ValueError: If timestamp is negative.

        Complexity:
            O(1) time and O(1) space per request.
        """
        pass



class WindowedRateLimiter(AbstractRateLimiter):

    """
    A fixed-window global rate limiter implementation.
    """

    def __init__(self, rate: int, seconds: int):
        self.rate = rate
        self.seconds = seconds
        self.count = 0
        self.window = 0


    def should_allow_request(self, user_id: str, timestamp: int) -> bool:

        # The window is calculated using floor division of the timestamp by the provided limiting seconds
        window = timestamp // self.seconds

        # If we are in a new window, reset the rate counter
        if self.window != window:
            self.window = window
            self.count = 0

        # Check if rate limit exceeded and if not then increase the rate counter
        if self.count < self.rate:
            self.count += 1
            return True
        else:
            return False



class WindowedUserRateLimiter(AbstractRateLimiter):

    """
    A user based fixed-window global rate limiter implementation.
    """

    def __init__(self, rate: int, seconds: int):
        self.rate = rate
        self.seconds = seconds
        self.hash = dict()


    def should_allow_request(self, user_id: str, timestamp: int) -> bool:

        # The window is calculated using floor division of the timestamp by the provided limiting seconds
        window = timestamp // self.seconds

        # If we are in a new window, reset the rate counter
        userwindow, count = self.hash.get(user_id, (window, 0))
        
        if userwindow != window:
            userwindow = window
            count = 0

        # Check if rate limit exceeded and if not then increase the rate counter
        if count < self.rate:
            count += 1
            self.hash[user_id] = (userwindow, count)
            return True
        else:
            return False
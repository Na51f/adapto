import time
import requests
from collections import deque

class RateLimiter:
    def __init__(self, short_limit=20, short_window=1, long_limit=100, long_window=120):
        self.short_limit = short_limit
        self.short_window = short_window
        self.long_limit = long_limit
        self.long_window = long_window
        self.short_queue = deque()
        self.long_queue = deque()

    def wait(self):
        current_time = time.time()

        # Clean up old timestamps
        while self.short_queue and current_time - self.short_queue[0] > self.short_window:
            self.short_queue.popleft()
        while self.long_queue and current_time - self.long_queue[0] > self.long_window:
            self.long_queue.popleft()

        # Check if we need to wait
        if len(self.short_queue) >= self.short_limit or len(self.long_queue) >= self.long_limit:
            sleep_time = min(
                self.short_queue[0] + self.short_window - current_time if self.short_queue else 0,
                self.long_queue[0] + self.long_window - current_time if self.long_queue else 0
            )
            time.sleep(max(0, sleep_time))

        # Add current timestamp to queues
        self.short_queue.append(time.time())
        self.long_queue.append(time.time())

def api_request(url, params=None, headers=None):
    rate_limiter = RateLimiter()
    rate_limiter.wait()
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

# Example usage:
# result = api_request('https://api.example.com/endpoint', params={'key': 'value'})
# if result:
#     print(result)

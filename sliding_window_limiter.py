import random
from typing import Dict
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self.user_requests: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        if user_id not in self.user_requests:
            return
        # Remove timestamps outside the current window
        while self.user_requests[user_id] and current_time - self.user_requests[user_id][0] > self.window_size:
            self.user_requests[user_id].popleft()
        # If no requests remain, remove the user entry
        if not self.user_requests[user_id]:
            del self.user_requests[user_id]

    def can_send_message(self, user_id: str) -> bool:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        # Check if the number of requests in the window is below the limit
        return user_id not in self.user_requests or len(self.user_requests[user_id]) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        if not self.can_send_message(user_id):
            return False
        current_time = time.time()
        if user_id not in self.user_requests:
            self.user_requests[user_id] = deque()
        self.user_requests[user_id].append(current_time)
        return True

    def time_until_next_allowed(self, user_id: str) -> float:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        if user_id not in self.user_requests or len(self.user_requests[user_id]) < self.max_requests:
            return 0.0
        # Calculate time until the oldest request expires
        oldest_timestamp = self.user_requests[user_id][0]
        return max(0.0, self.window_size - (current_time - oldest_timestamp))

def test_rate_limiter():
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)
    print("\n=== Симуляція потоку повідомлень ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        time.sleep(random.uniform(0.1, 1.0))

    print("\nОчікуємо 4 секунди...")
    time.sleep(4)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_rate_limiter()
import random
from typing import List, Optional
import time


class ProxyPool:
    def __init__(self, proxies: List[str] = None):
        self.proxies = proxies or []
        self.failed_proxies = {}
        self.max_failures = 3

    def add_proxy(self, proxy: str):
        if proxy not in self.proxies:
            self.proxies.append(proxy)

    def get_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None

        available = [p for p in self.proxies if self.failed_proxies.get(p, 0) < self.max_failures]

        if not available:
            self.failed_proxies.clear()
            available = self.proxies

        return random.choice(available)

    def mark_failed(self, proxy: str):
        if proxy in self.failed_proxies:
            self.failed_proxies[proxy] += 1
        else:
            self.failed_proxies[proxy] = 1

    def mark_success(self, proxy: str):
        if proxy in self.failed_proxies:
            del self.failed_proxies[proxy]


class RetryStrategy:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 30.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def get_delay(self, attempt: int) -> float:
        delay = self.base_delay * (2 ** attempt)
        jitter = random.uniform(0, 1)
        return min(delay + jitter, self.max_delay)

    def should_retry(self, attempt: int, exception: Exception) -> bool:
        if attempt >= self.max_retries:
            return False

        retryable_errors = [
            'ConnectionError',
            'Timeout',
            'HTTPError',
            'SSLError',
        ]

        error_type = type(exception).__name__
        return any(err in error_type for err in retryable_errors)


class RateLimiter:
    def __init__(self, requests_per_second: float = 2.0):
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0

    def wait(self):
        current_time = time.time()
        elapsed = current_time - self.last_request_time

        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)

        self.last_request_time = time.time()

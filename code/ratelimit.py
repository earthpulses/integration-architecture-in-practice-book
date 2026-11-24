"""A token bucket: allow `rate` calls per second, with bursts up to `burst`."""
import threading, time

class TokenBucket:
    def __init__(self, rate, burst=None, clock=time.monotonic, sleep=time.sleep):
        self.rate = float(rate)
        self.capacity = float(burst or rate)
        self.tokens = self.capacity
        self.clock, self.sleep = clock, sleep
        self.updated = clock()
        self.lock = threading.Lock()

    def acquire(self, n=1):
        """Block until n tokens are available, then take them."""
        while True:
            with self.lock:
                now = self.clock()
                gained = (now - self.updated) * self.rate
                self.tokens = min(self.capacity, self.tokens + gained)
                self.updated = now
                if self.tokens >= n:
                    self.tokens -= n
                    return
                wait = (n - self.tokens) / self.rate
            self.sleep(wait)             # sleep outside the lock

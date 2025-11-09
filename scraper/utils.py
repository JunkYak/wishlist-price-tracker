import os
import json
import asyncio
import logging
from datetime import datetime
from functools import wraps
from contextlib import asynccontextmanager


# -----------------------------------------------------
# 🧱 1. Daily JSON Logger (per user or global)
# -----------------------------------------------------
def get_logger(user_email: str | None = None):
    """
    Creates (or reuses) a structured JSON logger.
    If user_email is provided, logs go under /logs/users/<email>/scraper_<date>.json
    Otherwise, logs go to /logs/scraper_<date>.json
    """

    today = datetime.now().strftime("%Y-%m-%d")

    # Decide log path
    if user_email:
        safe_email = user_email.replace("@", "_at_").replace(".", "_")
        log_dir = os.path.join("logs", "users", safe_email)
    else:
        log_dir = os.path.join("logs")

    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"scraper_{today}.json")

    # Create a logger
    logger = logging.getLogger(f"scraper_{user_email or 'global'}")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)

        # Also log to console
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(console)

    return logger


# -----------------------------------------------------
# ⏳ 2. Duration tracker
# -----------------------------------------------------
@asynccontextmanager
async def time_it():
    """
    Async context manager to measure execution time.
    Usage:
        async with time_it() as t:
            await something()
        print(t['duration'])
    """
    start = datetime.now()
    result = {"duration": None}
    try:
        yield result
    finally:
        result["duration"] = (datetime.now() - start).total_seconds()


# -----------------------------------------------------
# 🔁 3. Retry decorator (async-safe)
# -----------------------------------------------------
def retry_async(retries=3, delay=2, backoff=2):
    """
    Async retry decorator with exponential backoff.
    Usage:
        @retry_async(retries=3)
        async def fetch():
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 1
            last_exc = None
            current_delay = delay
            while attempt <= retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    print(f"[retry] Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    attempt += 1
            raise last_exc
        return wrapper
    return decorator

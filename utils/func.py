import asyncio
from typing import Callable
from datetime import datetime


def delayed_notification(timeout: int):
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs):
            start_time = datetime.now()
            task = asyncio.ensure_future(func(*args, **kwargs))
            try:
                # Wait for the task to complete with a timeout
                await asyncio.wait_for(task, timeout)
            except asyncio.TimeoutError:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                print(
                    f"Function {func.__name__} took too long ({duration:.2f} seconds) to complete."
                )

            return await task

        return wrapper

    return decorator




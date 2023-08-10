import asyncio

from typing import Callable
from datetime import datetime


def async_delayed_notification(timeout: int):
    def decorator(func: Callable) -> Callable:
        async def wrapper(self, *args, **kwargs):
            start_time = datetime.now()
            task = asyncio.ensure_future(func(self, *args, **kwargs))
            try:
                # Wait for the task to complete with a timeout
                await asyncio.wait_for(task, timeout)
            except asyncio.TimeoutError:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                print(f"Function {func.__name__} took too long ({duration:.2f} seconds) to complete.")

            return await task

        return wrapper

    return decorator

# 下单的时间，如果 2（n） 秒没有返回，就推送延迟的通知
class AsyncDelayedNotificationMeta(type):
    def __new__(cls, name, bases, class_dict):
        for attr_name, attr_value in class_dict.items():
            if asyncio.iscoroutinefunction(attr_value):
                class_dict[attr_name] = async_delayed_notification(2)(attr_value)
        return super().__new__(cls, name, bases, class_dict)


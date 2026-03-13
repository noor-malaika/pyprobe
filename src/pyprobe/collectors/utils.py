from functools import wraps
from typing import Callable


def metric(fn: Callable):
    """Decorator to mark a method as a metric-producing function."""

    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        return fn(self, *args, **kwargs)

    wrapper.__is_metric__ = True
    return wrapper

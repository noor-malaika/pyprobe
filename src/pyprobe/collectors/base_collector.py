import inspect
from abc import ABC
from typing import Any, Dict, List

from pyprobe.logger import logger


class BaseCollector(ABC):

    def __init__(self):
        self.logger = logger
        self.metrics: List[Dict[str, Any]] = []

    def collect_all(self) -> List[Dict[str, Any]]:
        self.metrics.clear()

        for _, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if getattr(method, "__is_metric__", False):
                try:
                    method()
                except Exception:
                    self.logger.exception(
                        "Error collecting %s metrics", self.__class__.__name__
                    )

        return self.metrics

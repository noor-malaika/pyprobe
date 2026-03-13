import psutil
from typing import List, Dict, Any
from pyprobe.collectors.base_collector import BaseCollector
from pyprobe.collectors.utils import metric


class MemoryCollector(BaseCollector):
    def __init__(self) -> None:
        super().__init__()

    @metric
    def get_memory_usage(self) -> List[Dict[str, Any]]:
        try:
            keys = ["total", "available", "used", "percent"]
            memory = psutil.virtual_memory()
            for key in keys:
                self.metrics.append(
                    {
                        "name": f"probe_memory_{key}_bytes"
                        if key != "percent"
                        else "probe_memory_usage_percent",
                        "value": getattr(memory, key),
                        "type": "gauge",
                        "labels": {},
                    }
                )
        except Exception:
            self.logger.exception("Error collecting memory metrics")
        return self.metrics

    @metric
    def get_swap_usage(self) -> List[Dict[str, Any]]:
        try:
            keys = ["total", "used", "free", "percent"]
            swap = psutil.swap_memory()
            for key in keys:
                self.metrics.append(
                    {
                        "name": f"probe_swap_{key}_bytes"
                        if key != "percent"
                        else "probe_swap_usage_percent",
                        "value": getattr(swap, key),
                        "type": "gauge",
                        "labels": {},
                    }
                )
        except Exception:
            self.logger.exception("Error collecting swap memory metrics")
        return self.metrics

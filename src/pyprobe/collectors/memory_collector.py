import psutil
from typing import List, Dict, Any


class MemoryCollector:
    def __init__(self) -> None:
        pass

    def get_memory_usage(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            keys = ["total", "available", "used", "percent"]
            memory = psutil.virtual_memory()
            for key in keys:
                metrics.append(
                    {
                        "name": f"probe_memory_{key}_bytes"
                        if key != "percent"
                        else "probe_memory_usage_percent",
                        "value": getattr(memory, key),
                        "type": "gauge",
                        "labels": {},
                    }
                )
        except Exception as e:
            print(f"Error collecting memory metrics: {e}")
        return metrics

    def get_swap_usage(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            keys = ["total", "used", "free", "percent"]
            swap = psutil.swap_memory()
            for key in keys:
                metrics.append(
                    {
                        "name": f"probe_swap_{key}_bytes"
                        if key != "percent"
                        else "probe_swap_usage_percent",
                        "value": getattr(swap, key),
                        "type": "gauge",
                        "labels": {},
                    }
                )
        except Exception as e:
            print(f"Error collecting swap memory metrics: {e}")
        return metrics

    def collect_all(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            metrics.extend(self.get_memory_usage())
            metrics.extend(self.get_swap_usage())
        except Exception as e:
            print(f"Error collecting memory metrics: {e}")
        return metrics

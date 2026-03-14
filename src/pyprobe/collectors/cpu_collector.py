import psutil
from typing import List, Dict, Any
from pyprobe.collectors.base_collector import BaseCollector
from pyprobe.collectors.utils import metric


class CpuCollector(BaseCollector):
    def __init__(self) -> None:
        super().__init__()
        self.cpu_count: int
        try:
            self.cpu_count = psutil.cpu_count() or 1  # Fallback to 1 if None
        except Exception:
            self.logger.exception("Error initializing CpuCollector")
            self.cpu_count = 1

    @metric
    def get_cpu_times(self) -> List[Dict[str, Any]]:
        try:
            modes = ["user", "system", "idle", "iowait"]
            cpu_times = psutil.cpu_times()
            for mode in modes:
                self.metrics.append(
                    {
                        "name": "probe_cpu_seconds_total",
                        "value": getattr(cpu_times, mode),
                        "type": "counter",
                        "labels": {"mode": mode},
                    }
                )
        except Exception:
            self.logger.exception("Error collecting CPU times")
        return self.metrics

    @metric
    def get_cpu_usage(self) -> List[Dict[str, Any]]:
        try:
            usage = psutil.cpu_percent(interval=None)
            self.metrics.append(
                {
                    "name": "probe_cpu_usage_percent",
                    "value": usage,
                    "type": "gauge",
                    "labels": {},
                }
            )
        except Exception:
            self.logger.exception("Error collecting CPU usage")
        return self.metrics

    @metric
    def get_cpu_load(self) -> List[Dict[str, Any]]:
        try:
            load_averages = psutil.getloadavg()
            timeframes = ["1", "5", "15"]
            for i, avg in enumerate(load_averages):
                load_percent = (avg * 100) / self.cpu_count
                self.metrics.append(
                    {
                        "name": "probe_avg_load",
                        "value": load_percent,
                        "type": "gauge",
                        "labels": {"mode": f"{timeframes[i]}min"},
                    }
                )
        except Exception:
            self.logger.exception("Error collecting CPU load averages")
        return self.metrics

import psutil
from typing import List, Dict, Any


class CpuCollector:
    def __init__(self) -> None:
        self.cpu_count: int
        try:
            self.cpu_count = psutil.cpu_count() or 1  # Fallback to 1 if None
        except Exception as e:
            print(f"Error initializing CpuCollector: {e}")
            self.cpu_count = 1

    def get_cpu_times(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            modes = ["user", "system", "idle", "iowait"]
            cpu_times = psutil.cpu_times()
            for mode in modes:
                metrics.append(
                    {
                        "name": "probe_cpu_seconds_total",
                        "value": getattr(cpu_times, mode),
                        "type": "counter",
                        "labels": {"mode": mode},
                    }
                )
        except Exception as e:
            print(f"Error collecting CPU times: {e}")
        return metrics

    def get_cpu_usage(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            usage = psutil.cpu_percent(interval=None)
            metrics.append(
                {
                    "name": "probe_cpu_usage_percent",
                    "value": usage,
                    "type": "gauge",
                    "labels": {},
                }
            )
        except Exception as e:
            print(f"Error collecting CPU usage: {e}")
        return metrics

    def get_cpu_load(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            load_averages = psutil.getloadavg()
            timeframes = ["1", "5", "15"]
            for i, avg in enumerate(load_averages):
                load_percent = (avg * 100) / self.cpu_count
                metrics.append(
                    {
                        "name": "probe_avg_load",
                        "value": load_percent,
                        "type": "gauge",
                        "labels": {"mode": f"{timeframes[i]}min"},
                    }
                )
        except Exception as e:
            print(f"Error collecting CPU load averages: {e}")
        return metrics

    def collect_all(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            metrics.extend(self.get_cpu_times())
            metrics.extend(self.get_cpu_usage())
            metrics.extend(self.get_cpu_load())
        except Exception as e:
            print(f"Error collecting CPU metrics: {e}")
        return metrics

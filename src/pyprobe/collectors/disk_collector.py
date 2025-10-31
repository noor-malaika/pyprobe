import psutil
from typing import List, Dict, Any


class DiskCollector:
    def __init__(self) -> None:
        pass

    def get_disk_usage(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            keys = ["total", "used", "free", "percent"]
            usage = psutil.disk_usage("/")
            for key in keys:
                metrics.append(
                    {
                        "name": f"probe_disk_{key}_bytes"
                        if key != "percent"
                        else "probe_disk_usage_percent",
                        "value": getattr(usage, key),
                        "type": "gauge",
                        "labels": {},
                    }
                )
        except Exception as e:
            print(f"Error collecting disk usage metrics: {e}")
        return metrics

    def get_disk_io(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            io_counters = psutil.disk_io_counters()
            keys = ["read_bytes", "write_bytes", "read_count", "write_count"]
            for key in keys:
                metrics.append(
                    {
                        "name": f"probe_disk_io_{key}",
                        "value": getattr(io_counters, key),
                        "type": "counter",
                        "labels": {},
                    }
                )
        except Exception as e:
            print(f"Error collecting disk I/O metrics: {e}")
        return metrics

    def get_disk_partitions(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            partitions = psutil.disk_partitions()
            for partition in partitions:
                metrics.append(
                    {
                        "name": "probe_disk_partition",
                        "value": 1,
                        "type": "gauge",
                        "labels": {
                            "device": partition.device,
                            "mountpoint": partition.mountpoint,
                            "fstype": partition.fstype,
                        },
                    }
                )
        except Exception as e:
            print(f"Error collecting disk partition metrics: {e}")
        return metrics

    def collect_all(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            metrics.extend(self.get_disk_usage())
            metrics.extend(self.get_disk_io())
            metrics.extend(self.get_disk_partitions())
        except Exception as e:
            print(f"Error collecting storage metrics: {e}")
        return metrics

import psutil
from typing import List, Dict, Any
from pyprobe.collectors.base_collector import BaseCollector
from pyprobe.collectors.utils import metric


class DiskCollector(BaseCollector):
    def __init__(self) -> None:
        super().__init__()

    @metric
    def get_disk_usage(self) -> List[Dict[str, Any]]:
        try:
            keys = ["total", "used", "free", "percent"]
            usage = psutil.disk_usage("/")
            for key in keys:
                self.metrics.append(
                    {
                        "name": f"probe_disk_{key}_bytes"
                        if key != "percent"
                        else "probe_disk_usage_percent",
                        "value": getattr(usage, key),
                        "type": "gauge",
                        "labels": {},
                    }
                )
        except Exception:
            self.logger.exception("Error collecting disk usage metrics")
        return self.metrics

    @metric
    def get_disk_io(self) -> List[Dict[str, Any]]:
        try:
            io_counters = psutil.disk_io_counters()
            keys = ["read_bytes", "write_bytes", "read_count", "write_count"]
            for key in keys:
                self.metrics.append(
                    {
                        "name": f"probe_disk_io_{key}",
                        "value": getattr(io_counters, key),
                        "type": "counter",
                        "labels": {},
                    }
                )
        except Exception:
            self.logger.exception("Error collecting disk I/O metrics")
        return self.metrics

    @metric
    def get_disk_partitions(self) -> List[Dict[str, Any]]:
        try:
            partitions = psutil.disk_partitions()
            for partition in partitions:
                self.metrics.append(
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
        except Exception:
            self.logger.exception("Error collecting disk partition metrics")
        return self.metrics

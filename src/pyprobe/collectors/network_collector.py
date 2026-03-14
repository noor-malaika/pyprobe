import psutil
from typing import List, Dict, Any
from pyprobe.collectors.base_collector import BaseCollector
from pyprobe.collectors.utils import metric


class NetworkCollector(BaseCollector):
    def __init__(self) -> None:
        super().__init__()

    @metric
    def get_net_io_counters(self) -> List[Dict[str, Any]]:
        try:
            io_counters = psutil.net_io_counters()
            keys = [
                "bytes_sent",
                "bytes_recv",
                "packets_sent",
                "packets_recv",
                "errin",
                "errout",
                "dropin",
                "dropout",
            ]
            for key in keys:
                self.metrics.append(
                    {
                        "name": f"probe_network_{key}",
                        "value": getattr(io_counters, key),
                        "type": "counter",
                        "labels": {},
                    }
                )
        except Exception:
            self.logger.exception("Error collecting network I/O metrics")
        return self.metrics

    @metric
    def get_net_connections(self) -> List[Dict[str, Any]]:
        try:
            keys = ["family", "type", "laddr", "raddr", "status", "pid"]
            connections = psutil.net_connections()
            for connection in connections:
                for key in keys:
                    self.metrics.append(
                        {
                            "name": "probe_network_connection",
                            "value": getattr(connection, key),
                            "type": "gauge",
                            "labels": {"type": key},
                        }
                    )
        except Exception:
            self.logger.exception("Error collecting network connections metrics")
        return self.metrics

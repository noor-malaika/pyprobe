import psutil
from typing import List, Dict, Any


class NetworkCollector:
    def __init__(self) -> None:
        pass

    def get_net_io_counters(self) -> List[Dict[str, Any]]:
        metrics = []
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
                metrics.append(
                    {
                        "name": f"probe_network_{key}",
                        "value": getattr(io_counters, key),
                        "type": "counter",
                        "labels": {},
                    }
                )
        except Exception as e:
            print(f"Error collecting network I/O metrics: {e}")
        return metrics

    def get_net_connections(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            keys = ["family", "type", "laddr", "raddr", "status", "pid"]
            connections = psutil.net_connections()
            for connection in connections:
                for key in keys:
                    metrics.append(
                        {
                            "name": "probe_network_connection",
                            "value": getattr(connection, key),
                            "type": "gauge",
                            "labels": {"type": key},
                        }
                    )
        except Exception as e:
            print(f"Error collecting network connections metrics: {e}")
        return metrics

    def collect_all(self) -> List[Dict[str, Any]]:
        metrics = []
        try:
            metrics.extend(self.get_net_io_counters())
            metrics.extend(self.get_net_connections())
        except Exception as e:
            print(f"Error collecting network metrics: {e}")
        return metrics

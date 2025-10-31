from fastapi import FastAPI, Response
from typing import List, Any
from pyprobe.registry import MetricRegistry
from pyprobe.collectors.cpu_collector import CpuCollector
from pyprobe.collectors.memory_collector import MemoryCollector
from pyprobe.collectors.network_collector import NetworkCollector
from pyprobe.collectors.disk_collector import DiskCollector

app = FastAPI()


@app.get("/metrics")
def retrieve_metrics() -> Response:
    metric_registry = MetricRegistry()
    collectors: List[Any] = [
        CpuCollector,
        MemoryCollector,
        NetworkCollector,
        DiskCollector,
    ]
    for collector in collectors:
        metric_registry.register_collector(collector())
    metric_text = metric_registry.get_metrics()
    return Response(content=metric_text, media_type="text/plain")

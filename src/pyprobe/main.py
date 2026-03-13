import argparse
from typing import List, Any

import uvicorn
from fastapi import FastAPI, Response

from pyprobe.registry import MetricRegistry
from pyprobe.collectors.cpu_collector import CpuCollector
from pyprobe.collectors.memory_collector import MemoryCollector
from pyprobe.collectors.network_collector import NetworkCollector
from pyprobe.collectors.disk_collector import DiskCollector


app = FastAPI()


def collect_metrics_text() -> str:
    metric_registry = MetricRegistry()
    collectors: List[Any] = [
        CpuCollector,
        MemoryCollector,
        NetworkCollector,
        DiskCollector,
    ]
    for collector in collectors:
        metric_registry.register_collector(collector())
    return metric_registry.get_metrics()


@app.get("/metrics")
def retrieve_metrics() -> Response:
    return Response(content=collect_metrics_text(), media_type="text/plain")


def main(argv: List[str] | None = None) -> None:
    """CLI entry point.

    By default this starts a Uvicorn server serving the FastAPI app.
    Using --metrics prints the current metrics to stdout instead.
    """
    parser = argparse.ArgumentParser(prog="pyprobe")
    parser.add_argument("--host", default="127.0.0.1", help="Listen host")
    parser.add_argument("--port", type=int, default=8000, help="Listen port")
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Print metrics to stdout (does not start server)",
    )

    args = parser.parse_args(argv)

    if args.metrics:
        print(collect_metrics_text())
        return

    uvicorn.run("pyprobe.main:app", host=args.host, port=args.port)

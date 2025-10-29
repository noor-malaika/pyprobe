from fastapi import FastAPI, Response
from registry import MetricRegistry
from collectors.cpu_collector import CpuCollector

app = FastAPI()


@app.get("/metrics")
def retrieve_metrics():
    metric_registry = MetricRegistry()
    metric_registry.register_collector(CpuCollector())
    metric_text = metric_registry.get_metrics()
    return Response(content=metric_text, media_type="text/plain")

from typing import Any, Dict, List

from pyprobe.logger import logger as _logger


class MetricRegistry:
    def __init__(self) -> None:
        self.collectors: List[Any] = []

    def register_collector(self, collector: Any) -> None:
        self.collectors.append(collector)

    def get_metrics(self) -> str:
        all_metrics: List[Dict[str, Any]] = []
        for collector in self.collectors:
            try:
                metrics = collector.collect_all()
                all_metrics.extend(metrics)
            except Exception:
                _logger.exception(
                    "Error collecting metrics from %s", collector.__class__.__name__
                )
        lines = []
        for metric in all_metrics:
            try:
                key = metric["name"]
                if metric["labels"]:
                    labels = ",".join(
                        [f"{k}={v}" for k, v in sorted(metric["labels"].items())]
                    )
                    key = f"{key}{{{labels}}}"
                lines.append(f"{key} {metric['value']}")
            except Exception:
                _logger.exception(
                    "Error preparing metric '%s'", metric.get("name", "<unknown>")
                )
        return "\n".join(lines)

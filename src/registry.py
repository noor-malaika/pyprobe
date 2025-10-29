class MetricRegistry:
    def __init__(self):
        self.collectors = []

    def register_collector(self, collector):
        self.collectors.append(collector)

    def get_metrics(self):
        all_metrics = []
        for collector in self.collectors:
            try:
                metrics = collector.collect_all()
                all_metrics.extend(metrics)
            except Exception as e:
                print(f"Error collecting metrics from {collector.__name__}\n{e}")
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
            except Exception as e:
                print(
                    f"Error preparing metric '{metric.get('name', '<unknown>')}': {e}"
                )
        return "\n".join(lines)

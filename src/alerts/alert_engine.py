from typing import Any


class AlertEngine:

    def __init__(
        self,
        cpu_warning: float = 80.0,
        cpu_critical: float = 90.0,
        memory_warning: float = 80.0,
        memory_critical: float = 90.0,
        disk_warning: float = 80.0,
        disk_critical: float = 90.0,
    ):
        self.thresholds = {
            "cpu": {
                "warning": cpu_warning,
                "critical": cpu_critical,
            },
            "memory": {
                "warning": memory_warning,
                "critical": memory_critical,
            },
            "disk": {
                "warning": disk_warning,
                "critical": disk_critical,
            },
        }

    def _check_metric(
        self,
        metric_name: str,
        value: float
    ) -> dict[str, Any] | None:

        thresholds = self.thresholds[metric_name]

        if value >= thresholds["critical"]:
            severity = "CRITICAL"

        elif value >= thresholds["warning"]:
            severity = "WARNING"

        else:
            return None

        return {
            "metric": metric_name,
            "value": round(value, 2),
            "severity": severity,
            "message": (
                f"{metric_name.upper()} usage is "
                f"{round(value, 2)}%"
            )
        }

    def evaluate(self, metrics: dict) -> list[dict]:

        alerts = []

        cpu_alert = self._check_metric(
            "cpu",
            metrics["cpu"]["usage_percent"]
        )

        if cpu_alert:
            alerts.append(cpu_alert)

        memory_alert = self._check_metric(
            "memory",
            metrics["memory"]["usage_percent"]
        )

        if memory_alert:
            alerts.append(memory_alert)

        disk_alert = self._check_metric(
            "disk",
            metrics["disk"]["usage_percent"]
        )

        if disk_alert:
            alerts.append(disk_alert)

        return alerts

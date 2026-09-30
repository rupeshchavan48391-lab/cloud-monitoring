from prometheus_client import Gauge


# ============================================================
# Prometheus Metrics
# ============================================================

cpu_usage = Gauge(
    "cloudmon_cpu_usage_percent",
    "Current CPU usage percentage"
)

memory_usage = Gauge(
    "cloudmon_memory_usage_percent",
    "Current memory usage percentage"
)

disk_usage = Gauge(
    "cloudmon_disk_usage_percent",
    "Current disk usage percentage"
)

memory_available_mb = Gauge(
    "cloudmon_memory_available_mb",
    "Available memory in megabytes"
)

disk_free_gb = Gauge(
    "cloudmon_disk_free_gb",
    "Free disk space in gigabytes"
)


# ============================================================
# Update Prometheus Metrics
# ============================================================

def update_metrics(metrics: dict):

    cpu_usage.set(
        metrics["cpu"]["usage_percent"]
    )

    memory_usage.set(
        metrics["memory"]["usage_percent"]
    )

    memory_available_mb.set(
        metrics["memory"]["available_mb"]
    )

    disk_usage.set(
        metrics["disk"]["usage_percent"]
    )

    disk_free_gb.set(
        metrics["disk"]["free_gb"]
    )

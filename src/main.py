from contextlib import asynccontextmanager
import asyncio
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response

from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST
)

from src.monitoring.system_monitor import SystemMonitor
from src.monitoring.collector import MonitoringCollector
from src.monitoring.prometheus_metrics import update_metrics
from src.alerts.alert_engine import AlertEngine

from src.database.queries import (
    get_latest_metrics,
    get_alert_history
)


# ============================================================
# Core Components
# ============================================================

monitor = SystemMonitor()

alert_engine = AlertEngine()

collector = MonitoringCollector(
    interval=30
)

collector_task = None


# ============================================================
# Application Lifespan
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    global collector_task

    # Start background monitoring collector
    collector_task = asyncio.create_task(
        collector.run()
    )

    print("[SYSTEM] Monitoring collector started")

    yield

    # Stop monitoring collector gracefully
    if collector_task:

        collector_task.cancel()

        try:
            await collector_task

        except asyncio.CancelledError:
            pass

    print("[SYSTEM] Monitoring collector stopped")


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="CloudMon AI",
    description="AI-Powered Cloud Monitoring and Incident Response Platform",
    version="0.1.0",
    lifespan=lifespan
)


# ============================================================
# Root Endpoint
# ============================================================

@app.get("/")
def root():

    return {
        "project": "CloudMon AI",
        "status": "running",
        "version": "0.1.0",
        "dashboard": "/dashboard",
        "docs": "/docs"
    }


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "cloudmon-api"
    }


# ============================================================
# Current System Metrics
# ============================================================

@app.get("/metrics")
def metrics():

    return monitor.get_all_metrics()


# ============================================================
# Prometheus Metrics Endpoint
# ============================================================

@app.get("/metrics/prometheus")
def prometheus_metrics():

    # Collect current system metrics
    current_metrics = monitor.get_all_metrics()

    # Update Prometheus gauges
    update_metrics(
        current_metrics
    )

    # Return metrics in Prometheus format
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


# ============================================================
# Current Alerts
# ============================================================

@app.get("/alerts")
def alerts():

    current_metrics = monitor.get_all_metrics()

    current_alerts = alert_engine.evaluate(
        current_metrics
    )

    return {
        "alert_count": len(current_alerts),
        "alerts": current_alerts
    }


# ============================================================
# Historical Metrics
# ============================================================

@app.get("/metrics/history")
def metrics_history(
    limit: int = 20
):

    # Protect database from excessive queries
    limit = min(
        max(limit, 1),
        500
    )

    rows = get_latest_metrics(
        limit
    )

    return {
        "count": len(rows),

        "metrics": [

            {
                "id": row[0],
                "timestamp": row[1],
                "cpu_usage": row[2],
                "memory_usage": row[3],
                "disk_usage": row[4],
                "bytes_sent": row[5],
                "bytes_received": row[6]
            }

            for row in rows
        ]
    }


# ============================================================
# Historical Alerts
# ============================================================

@app.get("/alerts/history")
def alerts_history(
    limit: int = 20
):

    # Protect database from excessive queries
    limit = min(
        max(limit, 1),
        500
    )

    rows = get_alert_history(
        limit
    )

    return {
        "count": len(rows),

        "alerts": [

            {
                "id": row[0],
                "timestamp": row[1],
                "metric": row[2],
                "value": row[3],
                "severity": row[4],
                "message": row[5]
            }

            for row in rows
        ]
    }


# ============================================================
# Professional CloudMon Dashboard
# ============================================================

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard():

    dashboard_file = (
        Path(__file__).parent
        / "dashboard"
        / "index.html"
    )

    return dashboard_file.read_text(
        encoding="utf-8"
    )

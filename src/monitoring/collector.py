import asyncio

from src.monitoring.system_monitor import SystemMonitor
from src.alerts.alert_engine import AlertEngine
from src.database.connection import get_connection


class MonitoringCollector:

    def __init__(self, interval: int = 30):
        self.interval = interval
        self.monitor = SystemMonitor()
        self.alert_engine = AlertEngine()

    def collect_and_store(self):

        metrics = self.monitor.get_all_metrics()

        cpu = metrics["cpu"]["usage_percent"]
        memory = metrics["memory"]["usage_percent"]
        disk = metrics["disk"]["usage_percent"]

        network = metrics["network"]

        alerts = self.alert_engine.evaluate(metrics)

        with get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO metrics (
                        cpu_usage,
                        memory_usage,
                        disk_usage,
                        bytes_sent,
                        bytes_received
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        cpu,
                        memory,
                        disk,
                        network["bytes_sent"],
                        network["bytes_received"],
                    )
                )

                for alert in alerts:

                    cursor.execute(
                        """
                        INSERT INTO alerts (
                            metric,
                            value,
                            severity,
                            message
                        )
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            alert["metric"],
                            alert["value"],
                            alert["severity"],
                            alert["message"],
                        )
                    )

            connection.commit()

        return metrics, alerts

    async def run(self):

        while True:

            try:
                metrics, alerts = self.collect_and_store()

                print(
                    f"[MONITOR] "
                    f"CPU={metrics['cpu']['usage_percent']}% "
                    f"RAM={metrics['memory']['usage_percent']}% "
                    f"DISK={metrics['disk']['usage_percent']}%"
                )

                if alerts:
                    print(
                        f"[ALERT] {len(alerts)} alert(s) detected"
                    )

            except Exception as error:

                print(
                    f"[MONITOR ERROR] {error}"
                )

            await asyncio.sleep(self.interval)

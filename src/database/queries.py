from src.database.connection import get_connection


def get_latest_metrics(limit: int = 20):

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    timestamp,
                    cpu_usage,
                    memory_usage,
                    disk_usage,
                    bytes_sent,
                    bytes_received
                FROM metrics
                ORDER BY timestamp DESC
                LIMIT %s
                """,
                (limit,)
            )

            rows = cursor.fetchall()

    return rows


def get_alert_history(limit: int = 20):

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    timestamp,
                    metric,
                    value,
                    severity,
                    message
                FROM alerts
                ORDER BY timestamp DESC
                LIMIT %s
                """,
                (limit,)
            )

            rows = cursor.fetchall()

    return rows

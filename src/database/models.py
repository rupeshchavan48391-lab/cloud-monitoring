from src.database.connection import get_connection


def create_tables():

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS metrics (
                    id BIGSERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    cpu_usage DOUBLE PRECISION NOT NULL,
                    memory_usage DOUBLE PRECISION NOT NULL,
                    disk_usage DOUBLE PRECISION NOT NULL,
                    bytes_sent BIGINT NOT NULL,
                    bytes_received BIGINT NOT NULL
                );
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS alerts (
                    id BIGSERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    metric VARCHAR(50) NOT NULL,
                    value DOUBLE PRECISION NOT NULL,
                    severity VARCHAR(20) NOT NULL,
                    message TEXT NOT NULL
                );
                """
            )

        connection.commit()

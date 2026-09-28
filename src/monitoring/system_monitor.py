import psutil
import time


class SystemMonitor:

    def __init__(self):
        self.start_time = time.time()

    def get_cpu_metrics(self):
        return {
            "usage_percent": psutil.cpu_percent(interval=0.5),
            "cpu_count": psutil.cpu_count()
        }

    def get_memory_metrics(self):
        memory = psutil.virtual_memory()

        return {
            "total_mb": round(memory.total / (1024 ** 2), 2),
            "used_mb": round(memory.used / (1024 ** 2), 2),
            "available_mb": round(memory.available / (1024 ** 2), 2),
            "usage_percent": memory.percent
        }

    def get_disk_metrics(self):
        disk = psutil.disk_usage("/")

        return {
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "free_gb": round(disk.free / (1024 ** 3), 2),
            "usage_percent": disk.percent
        }

    def get_network_metrics(self):
        network = psutil.net_io_counters()

        return {
            "bytes_sent": network.bytes_sent,
            "bytes_received": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_received": network.packets_recv
        }

    def get_uptime(self):
        return round(time.time() - self.start_time, 2)

    def get_all_metrics(self):

        return {
            "cpu": self.get_cpu_metrics(),
            "memory": self.get_memory_metrics(),
            "disk": self.get_disk_metrics(),
            "network": self.get_network_metrics(),
            "application": {
                "uptime_seconds": self.get_uptime()
            }
        }

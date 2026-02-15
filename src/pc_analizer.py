import psutil

import json


def get_pc_info():
    info = {
        "cpu": psutil.cpu_times_percent()._asdict(),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict(),
        "processes": len(list(psutil.process_iter())),
        "boot_time": psutil.boot_time(),
    }

    return json.dumps(info, indent=2)

import os
import platform
import socket
import subprocess
from datetime import datetime

def _run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return result.stdout.strip()
    except Exception:
        return ""

def get_system_status():
    cpu = _get_cpu()
    ram = _get_ram()
    disk = _get_disk()
    os_info = f"{platform.system()} {platform.release()}"
    hostname = socket.gethostname()
    uptime = _get_uptime()
    try:
        internet = "ONLINE" if socket.gethostbyname(socket.gethostname()) else "OFFLINE"
    except Exception:
        internet = "UNKNOWN"
    return {
        'cpu': cpu,
        'ram': ram,
        'disk': disk,
        'os': os_info,
        'hostname': hostname,
        'uptime': uptime,
        'network': internet,
    }

def _get_cpu():
    if platform.system() == 'Windows':
        output = _run_command('wmic cpu get loadpercentage /value')
        for line in output.splitlines():
            if line.lower().startswith('loadpercentage'):
                val = line.split('=')[1].strip()
                try:
                    return f"{float(val):.1f}%"
                except Exception:
                    pass
        return "N/A"
    else:
        output = _run_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        try:
            return f"{float(output):.1f}%"
        except Exception:
            return "N/A"

def _get_ram():
    if platform.system() == 'Windows':
        output = _run_command('wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /value')
        total = None
        free = None
        for line in output.splitlines():
            if line.lower().startswith('totalvisiblememorysize'):
                total = int(line.split('=')[1].strip())
            elif line.lower().startswith('freephysicalmemory'):
                free = int(line.split('=')[1].strip())
        if total and free is not None:
            used = total - free
            return f"{used/(1024*1024):.0f} MB / {total/(1024*1024):.0f} MB"
        return "N/A"
    else:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        info = {l.split(':')[0].strip(): l.split(':')[1].strip().split()[0] for l in lines}
        total = int(info.get('MemTotal', 0))
        available = int(info.get('MemAvailable', 0))
        if total:
            used = total - available
            return f"{used//1024} MB / {total//1024} MB"
        return "N/A"

def _get_disk():
    path = os.path.splitdrive(os.getcwd())[0] + '\\' if platform.system() == 'Windows' else '/'
    try:
        usage = os.statvfs(path) if hasattr(os, 'statvfs') else None
        if usage:
            total = usage.f_frsize * usage.f_blocks
            free = usage.f_frsize * usage.f_bfree
            return f"{free//(1024*1024*1024):.2f} GB free"
    except Exception:
        pass
    output = _run_command(f'wmic logicaldisk where "DeviceID=\"{path[0]}:\"" get Size,FreeSpace /value')
    free = None
    for line in output.splitlines():
        if line.lower().startswith('freespace'):
            free = int(line.split('=')[1].strip())
    if free is not None:
        return f"{free//(1024*1024*1024):.2f} GB free"
    return "N/A"

def _get_uptime():
    if platform.system() == 'Windows':
        output = _run_command('wmic os get lastbootuptime /value')
        for line in output.splitlines():
            if line.lower().startswith('lastbootuptime'):
                boot_str = line.split('=')[1].strip()[:14]
                try:
                    boot_time = datetime.strptime(boot_str, '%Y%m%d%H%M%S')
                    uptime_seconds = (datetime.now() - boot_time).total_seconds()
                    hours = int(uptime_seconds // 3600)
                    minutes = int((uptime_seconds % 3600) // 60)
                    return f"{hours}h {minutes}m"
                except Exception:
                    pass
        return "N/A"
    else:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

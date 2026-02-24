from __future__ import annotations

import json
import platform
import shutil
import socket
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import cpuinfo
import psutil


def _run_command(args: list[str]) -> str | None:
    """Run a command and return stdout, or None if unavailable/failing."""
    if not args:
        return None
    if shutil.which(args[0]) is None:
        return None
    try:
        result = subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    output = (result.stdout or "").strip()
    return output or None


def _collect_cpu_info() -> dict:
    info = {}
    try:
        cpu = cpuinfo.get_cpu_info() or {}
    except Exception:
        cpu = {}

    info["brand"] = cpu.get("brand_raw")
    info["arch"] = cpu.get("arch")
    info["hz_advertised"] = cpu.get("hz_advertised_friendly")
    info["hz_actual"] = cpu.get("hz_actual_friendly")
    info["count_logical"] = psutil.cpu_count(logical=True)
    info["count_physical"] = psutil.cpu_count(logical=False)
    return info


def _collect_memory_info() -> dict:
    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()
    return {
        "ram_total_bytes": vm.total,
        "ram_available_bytes": vm.available,
        "ram_total_gb": round(vm.total / (1024**3), 2),
        "swap_total_bytes": sm.total,
    }


def _collect_disk_info() -> dict:
    disks = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except Exception:
            continue
        disks.append(
            {
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total_bytes": usage.total,
                "used_bytes": usage.used,
                "free_bytes": usage.free,
            }
        )
    return {"partitions": disks}


def _collect_gpu_info() -> dict:
    # NVIDIA (Linux/Windows, sometimes WSL)
    nvidia = _run_command(
        [
            "nvidia-smi",
            "--query-gpu=name,driver_version,memory.total",
            "--format=csv,noheader,nounits",
        ]
    )
    gpus = []
    if nvidia:
        for line in nvidia.splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 3:
                gpus.append(
                    {
                        "vendor": "nvidia",
                        "name": parts[0],
                        "driver_version": parts[1],
                        "memory_total_mb": parts[2],
                    }
                )

    # macOS fallback (coarse; no memory values)
    if not gpus and platform.system().lower() == "darwin":
        displays = _run_command(["system_profiler", "SPDisplaysDataType"])
        if displays:
            for line in displays.splitlines():
                text = line.strip()
                if text.startswith("Chipset Model:"):
                    gpus.append(
                        {
                            "vendor": "apple_or_other",
                            "name": text.split(":", 1)[1].strip(),
                        }
                    )

    return {"gpus": gpus}


def collect_hardware_info(include_hostname: bool = False) -> dict:
    """
    Collect a cross-platform hardware/system snapshot.

    Parameters
    ----------
    include_hostname : bool
        Include host name and node fields when True.
    """
    system = platform.uname()
    info = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "os": {
            "system": system.system,
            "release": system.release,
            "version": system.version,
            "machine": system.machine,
            "processor": system.processor,
            "platform": platform.platform(),
        },
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
        },
        "cpu": _collect_cpu_info(),
        "memory": _collect_memory_info(),
        "disk": _collect_disk_info(),
        "gpu": _collect_gpu_info(),
    }

    if include_hostname:
        info["host"] = {"hostname": socket.gethostname(), "node": system.node}

    return info


def write_hardware_info(
    output_path: str | Path = "hardware.json", include_hostname: bool = False
) -> Path:
    """
    Capture hardware info and write it to JSON.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = collect_hardware_info(include_hostname=include_hostname)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


#!/usr/bin/env python3
from __future__ import annotations

import time

try:
    import psutil
except Exception:
    psutil = None

def get_uptime() ->float:
    if psutil:
        try:
            return time.time() - psutil.boot_time()
        except Exception:
            pass
    try:
        with open('proc/time', 'r') as f:
            return float(f.read().strip())
    except Exception:
        return 0.0
    
# live_scheduler.py — Backend utility for process fetching and scheduling simulation
import psutil
import random

def get_live_processes(limit=10):
    """Collect a sample of running system processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            info = proc.info
            processes.append({
                "pid": info['pid'],
                "name": info['name'],
                "arrival": random.randint(0, 10),
                "burst": random.randint(1, 5)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        if len(processes) >= limit:
            break
    return processes

def simulate_scheduler(processes, algo="fcfs"):
    """Simulate CPU scheduling based on algorithm"""
    schedule = []
    time = 0
    for p in processes:
        start = time
        finish = start + p['burst']
        waiting = random.uniform(0.2, 3.0)
        turnaround = waiting + p['burst']
        schedule.append({
            "pid": p['pid'],
            "name": p['name'],
            "start": start,
            "finish": finish,
            "waiting": waiting,
            "turnaround": turnaround
        })
        time = finish
    return schedule

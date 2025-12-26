# main.py
from simulation.cpu_scheduler import fcfs_scheduler, sjf_scheduler, round_robin_scheduler, draw_gantt_chart
import pandas as pd
import argparse
import os

# ---------------- Argument Parser ----------------
parser = argparse.ArgumentParser(description="CPU Scheduling Simulator")
parser.add_argument("--algo", choices=["fcfs", "sjf", "rr"], required=True, help="Choose scheduling algorithm")
parser.add_argument("--quantum", type=int, default=2, help="Time quantum for Round Robin")
args = parser.parse_args()

# ---------------- Input Processes ----------------
processes = [
    {'pid': 'P1', 'arrival': 0, 'burst': 5},
    {'pid': 'P2', 'arrival': 2, 'burst': 3},
    {'pid': 'P3', 'arrival': 4, 'burst': 1}
]

# ---------------- Run Algorithm ----------------
if args.algo == "fcfs":
    schedule_log, decisions = fcfs_scheduler(processes.copy())
    label = "FCFS"
elif args.algo == "sjf":
    schedule_log, decisions = sjf_scheduler(processes.copy())
    label = "SJF"
elif args.algo == "rr":
    schedule_log, decisions = round_robin_scheduler(processes.copy(), quantum=args.quantum)
    label = f"Round Robin (q={args.quantum})"
else:
    raise ValueError("Unsupported algorithm")

# ---------------- Performance Metrics ----------------
avg_wait = sum(p['waiting'] for p in schedule_log) / len(schedule_log)
avg_turnaround = sum(p['turnaround'] for p in schedule_log) / len(schedule_log)

# CPU Utilization & Throughput
total_burst = sum(p['burst'] for p in schedule_log)
total_time = max(p['finish'] for p in schedule_log)
cpu_utilization = (total_burst / total_time) * 100
throughput = len(schedule_log) / total_time

print(f"\n🔹 {label} Results:")
for entry in schedule_log:
    print(f"{entry['pid']} → Start: {entry['start']}, Finish: {entry['finish']}, Waiting: {entry['waiting']}, Turnaround: {entry['turnaround']}")

print("\n📊 Averages & Metrics:")
print(f"Average Waiting Time: {avg_wait:.2f}")
print(f"Average Turnaround Time: {avg_turnaround:.2f}")
print(f"CPU Utilization: {cpu_utilization:.2f}%")
print(f"Throughput: {throughput:.2f} processes/unit time")

# ---------------- Save Logs ----------------
df_log = pd.DataFrame(schedule_log)
df_log.to_csv(f"{args.algo}_log.csv", index=False)

df_decisions = pd.DataFrame(decisions)
df_decisions.to_csv(f"{args.algo}_xai_decisions.csv", index=False)

# ---------------- Save Performance Summary ----------------
summary_file = "performance_summary.csv"
summary_data = {
    "Algorithm": [label],
    "Average Waiting Time": [avg_wait],
    "Average Turnaround Time": [avg_turnaround],
    "CPU Utilization (%)": [cpu_utilization],
    "Throughput": [throughput]
}

df_summary = pd.DataFrame(summary_data)
if os.path.exists(summary_file):
    old_df = pd.read_csv(summary_file)
    df_summary = pd.concat([old_df, df_summary], ignore_index=True)
df_summary.to_csv(summary_file, index=False)
print(f"\n✅ Performance summary saved to {summary_file}")

# ---------------- Optional Gantt Chart ----------------
draw_gantt_chart(schedule_log, title=f"{label} Scheduling Gantt Chart")

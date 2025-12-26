# xai_dashboard.py — Futuristic XAI OS Command Center (matte black, 3D, simulators, offline sandbox)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import psutil, time, os, glob, io
from sklearn.ensemble import IsolationForest
from fpdf import FPDF

# Backend helpers (must be UI-free)
import live_scheduler  # get_live_processes(), simulate_scheduler()

# ---------------- App Setup ----------------
st.set_page_config(page_title="XAI-OS Command Center", layout="wide", initial_sidebar_state="expanded")

# --- Matte Black + Holographic Glass CSS ---
st.markdown("""
<style>
:root{
  --bg:#0c0e12; --panel:#12151b; --glass:rgba(255,255,255,0.06);
  --accent:#00e5ff; --accent2:#7fff00; --warn:#ffb000; --danger:#ff4d4f;
  --text:#d6dde8; --sub:#9aa4b2; --silver:#cfd6e0;
}
html, body, [class*="css"] { background:var(--bg) !important; color:var(--text); }
section.main > div { padding-top: 6px; }
h1,h2,h3,h4,h5 { letter-spacing: .5px; }
.sidebar .sidebar-content{ background:var(--panel); }
.stButton>button, .stDownloadButton>button {
  border:1px solid var(--accent); color:var(--text); background:linear-gradient(120deg, rgba(0,229,255,.15), rgba(127,255,0,.12));
  border-radius:14px; padding:6px 14px; transition:all .25s ease; box-shadow:0 0 0 rgba(0,229,255,0);
}
.stButton>button:hover, .stDownloadButton>button:hover { transform:translateY(-1px) scale(1.01); box-shadow:0 8px 30px rgba(0,229,255,.15); }
.block-container { padding-top: 10px; }
.glass {
  background: linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
  border: 1px solid rgba(255,255,255,.10); border-radius: 18px; padding: 14px 14px; backdrop-filter: blur(6px);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.06), 0 10px 30px rgba(0,0,0,.45);
}
.kpi { border-left:3px solid var(--accent); padding-left:10px; }
.small { color:var(--sub); font-size:.9rem; }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "JetBrains Mono", "Liberation Mono", monospace; }
hr{border:none;height:1px;background:linear-gradient(90deg, transparent, rgba(255,255,255,.15), transparent);}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🧭 Navigation")
tab = st.sidebar.radio(
    "Select View",
    [
        "🖥️ Live System Scheduler (AI-Powered)",
        "📊 Individual Algorithm Log",
        "📈 Algorithm Comparison",
        "🧮 Memory & Paging (Hit Ratio / Page Faults)",
        "💿 Disk Scheduling Simulator",
        "🧪 3D CPU Pulse",
        "🛠️ Optimizer (Make Code Simpler & Faster)",
        "🧰 Offline Code Sandbox"
    ],
    key="nav_main"
)

st.title("🧠 XAI-OS — Futuristic AI Command Center")
st.caption("Matte black terminal vibes • Glass UI • Live analytics • Explainable schedulers • Offline simulators")

# -----------------------------------------
# Utilities
def kpi(col, label, value, help_txt=None):
    with col:
        st.markdown(f"<div class='glass kpi'><div class='small'>{label}</div><div style='font-size:1.6rem'>{value}</div></div>", unsafe_allow_html=True)
        if help_txt: st.caption(help_txt)

def perf_from_schedule(df):
    out = {}
    if df is None or df.empty: return out
    if {'waiting','turnaround'}.issubset(df.columns):
        out['avg_wait'] = df['waiting'].mean()
        out['avg_tat'] = df['turnaround'].mean()
    # Throughput = completed / makespan
    if {'start','finish'}.issubset(df.columns):
        makespan = max(df['finish'].max() - df['start'].min(), 1e-9)
        out['throughput'] = len(df) / makespan
        busy = (df['finish'] - df['start']).sum()
        out['cpu_util'] = 100.0 * busy / makespan if makespan>0 else 0.0
        out['eff'] = (out['throughput'] / max(df['burst'].mean(), 1e-9)) if 'burst' in df.columns else np.nan
    return out

# -----------------------------------------
# Tab: Live System Scheduler (kept + extended)
if tab == "🖥️ Live System Scheduler (AI-Powered)":
    st.subheader("🖥️ Real-Time Explainable Scheduling with Anomaly Detection")
    with st.container():
        left, mid, right = st.columns([1,1,1])
        algo = left.selectbox("Algorithm", ["fcfs","sjf","rr"], key="live_algo")
        refresh_rate = mid.slider("Auto-refresh (s)", 3, 20, 7, key="live_refresh")
        contam = right.slider("Anomaly sensitivity (contamination)", 0.01, 0.5, 0.2, 0.01, key="live_contam")
    features_choice = st.multiselect("Features for anomaly detection", ["waiting","turnaround"], default=["waiting","turnaround"], key="live_feats")
    auto_refresh = st.toggle("🔁 Auto-refresh", value=True, key="live_autorefresh")
    placeholder = st.empty()

    def render_once():
        with placeholder.container():
            with st.spinner("Fetching live system data…"):
                procs = live_scheduler.get_live_processes(limit=12)
                sched = live_scheduler.simulate_scheduler(procs, algo=algo)
                df = pd.DataFrame(sched)

                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory()

                # anomaly detect
                if not df.empty and len(features_choice) > 0 and len(df) >= 5:
                    try:
                        feats = df[features_choice].fillna(0)
                        model = IsolationForest(contamination=contam, random_state=42)
                        preds = model.fit_predict(feats)
                        df["anomaly"] = np.where(preds == -1, "Anomaly", "Normal")
                    except Exception:
                        df["anomaly"] = "Normal"
                else:
                    df["anomaly"] = "Normal"

                # KPIs
                c1, c2, c3, c4 = st.columns(4)
                kpi(c1, "🧠 CPU Usage", f"{cpu:.1f}%")
                kpi(c2, "💾 Memory", f"{mem.percent:.1f}%")
                pf = perf_from_schedule(df)
                kpi(c3, "⏱ Avg Waiting", f"{pf.get('avg_wait', np.nan):.2f}" if 'avg_wait' in pf else "–")
                kpi(c4, "📈 Throughput", f"{pf.get('throughput', np.nan):.2f}/s" if 'throughput' in pf else "–")

                st.markdown("<div class='glass'>", unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True, height=260)
                st.markdown("</div>", unsafe_allow_html=True)

                if not df.empty and {'start','finish','pid'}.issubset(df.columns):
                    colors = {'Normal':'#00e5ff', 'Anomaly':'#ff4d4f'}
                    fig = px.timeline(
                        df, x_start='start', x_end='finish', y='pid',
                        color='anomaly', color_discrete_map=colors, text='name',
                        title=f"Live Process Scheduling — {algo.upper()} (Anomalies Highlighted)"
                    )
                    fig.update_yaxes(autorange="reversed")
                    fig.update_layout(height=420, title_x=0.2, template='plotly_dark')
                    st.plotly_chart(fig, use_container_width=True)

                st.subheader("System Utilization")
                sys_df = pd.DataFrame({"Metric":["CPU %","Memory %"], "Value":[cpu, mem.percent]})
                sys_fig = px.bar(sys_df, x="Metric", y="Value", color="Metric", range_y=[0,100], title="Current Utilization")
                sys_fig.update_layout(template='plotly_dark', height=280)
                st.plotly_chart(sys_fig, use_container_width=True)

                # anomalies extract
                if "Anomaly" in df["anomaly"].values:
                    st.warning("⚠️ Anomalies detected — high waiting/turnaround.")
                    bad = df[df["anomaly"]=="Anomaly"][["pid","name","waiting","turnaround","start","finish"]]
                    st.dataframe(bad, use_container_width=True)
                    csv = bad.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "⬇️ Download anomalies (CSV)",
                        data=csv, file_name=f"anomalies_{int(time.time())}.csv",
                        mime="text/csv", key=f"dl_anom_{time.time()}"
                    )
                else:
                    st.success("✅ No anomalies in this cycle.")

                st.caption("Tip: lower contamination → fewer flags (higher precision).")

    if auto_refresh:
        while True:
            render_once()
            time.sleep(refresh_rate)
    else:
        render_once()

# -----------------------------------------
elif tab == "📊 Individual Algorithm Log":
    st.subheader("📂 Decision Logs (per algorithm)")
    st.write("Loaded from:", os.getcwd())
    st.write("Last refreshed:", time.ctime())
    files = sorted(glob.glob("*_xai_decisions.csv"))
    if not files:
        st.warning("No *_xai_decisions.csv files found. Run main.py first.")
    else:
        f = st.selectbox("Select a CSV", files, key="log_file")
        try:
            df = pd.read_csv(f)
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, height=380)
            st.markdown("</div>", unsafe_allow_html=True)

            if {'start','finish','pid'}.issubset(df.columns):
                fig = px.timeline(df, x_start='start', x_end='finish', y='pid', color='pid', text='pid',
                                  title="Process Execution Timeline")
                fig.update_yaxes(autorange="reversed")
                fig.update_layout(template='plotly_dark', height=420)
                st.plotly_chart(fig, use_container_width=True)

            pf = perf_from_schedule(df)
            c1,c2,c3 = st.columns(3)
            kpi(c1,"Avg Waiting", f"{pf.get('avg_wait',np.nan):.2f}" if 'avg_wait' in pf else "–")
            kpi(c2,"Avg Turnaround", f"{pf.get('avg_tat',np.nan):.2f}" if 'avg_tat' in pf else "–")
            kpi(c3,"Throughput", f"{pf.get('throughput',np.nan):.2f}/s" if 'throughput' in pf else "–")
        except Exception as e:
            st.error(f"Could not load: {e}")

# -----------------------------------------
elif tab == "📈 Algorithm Comparison":
    st.subheader("🏁 Comparative Analytics")
    path = "performance_summary.csv"
    if not os.path.exists(path):
        st.warning("performance_summary.csv not found. Run main.py batch first.")
    else:
        df = pd.read_csv(path)
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        for metric in ["Average Waiting Time","Average Turnaround Time","CPU Utilization (%)","Throughput"]:
            if metric in df.columns:
                fig = px.bar(df, x="Algorithm", y=metric, color="Algorithm", title=f"{metric} Comparison")
                fig.update_layout(template='plotly_dark', height=360)
                st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------
elif tab == "🧮 Memory & Paging (Hit Ratio / Page Faults)":
    st.subheader("🧮 Paging Simulator (FIFO / LRU)")
    ref_str = st.text_input("Reference String (space-separated)", "7 0 1 2 0 3 0 4 2 3 0 3 2", key="refstr")
    frames = st.slider("Frames", 1, 10, 3, key="frames")
    algo = st.selectbox("Replacement Policy", ["FIFO","LRU"], key="mem_algo")
    run = st.button("Run Simulation", key="run_paging")
    def simulate_paging(refs, frames, policy="FIFO"):
        frameset, frame_list = set(), []
        faults, hits = 0,0
        recent = []  # for LRU
        timeline = []
        for t, page in enumerate(refs):
            hit = page in frameset
            if hit:
                hits+=1
                if policy=="LRU":
                    if page in recent: recent.remove(page)
                    recent.append(page)
            else:
                faults+=1
                if len(frameset)<frames:  # empty slot
                    frameset.add(page); frame_list.append(page)
                else:
                    if policy=="FIFO":
                        evict = frame_list.pop(0); frameset.remove(evict)
                        frameset.add(page); frame_list.append(page)
                    else: # LRU
                        evict = recent.pop(0); frameset.remove(evict)
                        frameset.add(page); recent.append(page)
                if policy=="LRU" and page not in recent: recent.append(page)
            timeline.append({"t":t,"page":page,"hit":hit,"frames":list(frameset)})
        hit_ratio = hits / max(len(refs),1)
        return pd.DataFrame(timeline), faults, hit_ratio
    if run:
        try:
            refs = [int(x) for x in ref_str.strip().split()]
            tl, faults, hit_ratio = simulate_paging(refs, frames, algo)
            c1,c2 = st.columns(2)
            kpi(c1,"📉 Page Faults", faults)
            kpi(c2,"📈 Hit Ratio", f"{hit_ratio*100:.1f}%")
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.dataframe(tl, use_container_width=True, height=320)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Bad input: {e}")

# -----------------------------------------
elif tab == "💿 Disk Scheduling Simulator":
    st.subheader("💿 Disk Head Scheduling (FCFS / SSTF / SCAN / C-SCAN)")
    seq_str = st.text_input("Request Sequence (space-separated)", "98 183 37 122 14 124 65 67", key="req_seq")
    start_head = st.number_input("Start Head", 0, 199, 53, key="start_head")
    algo = st.selectbox("Policy", ["FCFS","SSTF","SCAN","C-SCAN"], key="disk_algo")
    direction = st.selectbox("Initial Direction (for SCAN/C-SCAN)", ["up","down"], key="disk_dir")
    run = st.button("Run Disk Scheduling", key="run_disk")
    def disk_schedule(reqs, start, algo="FCFS", direction="up", max_cyl=199):
        order = []; head = start; total = 0
        pending = reqs.copy()
        if algo=="FCFS":
            order = pending
        elif algo=="SSTF":
            cur = head; pool = pending.copy()
            while pool:
                nxt = min(pool, key=lambda x: abs(x-cur))
                order.append(nxt); pool.remove(nxt); cur = nxt
        elif algo in ["SCAN","C-SCAN"]:
            up = sorted([r for r in pending if r>=head])
            down = sorted([r for r in pending if r<head], reverse=True)
            if algo=="SCAN":
                order = (up + down) if direction=="up" else (down + up)
            else: # C-SCAN
                order = (up + down[::-1]) if direction=="up" else (down + up[::-1])
        # distance
        cur = head
        segments = []
        for r in order:
            dist = abs(r - cur); total += dist
            segments.append({"from":cur,"to":r,"move":dist})
            cur = r
        return pd.DataFrame(segments), order, total
    if run:
        try:
            reqs = [int(x) for x in seq_str.strip().split()]
            segs, order, total = disk_schedule(reqs, start_head, algo, direction)
            c1,c2 = st.columns(2)
            kpi(c1, "🔧 Total Head Movement", total, "lower is better")
            kpi(c2, "📦 Requests Served", len(order))
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.dataframe(pd.DataFrame({"Sequence":order}), use_container_width=True, height=220)
            st.markdown("</div>", unsafe_allow_html=True)
            # simple line path
            fig = go.Figure()
            xs = [start_head] + order
            ys = list(range(len(xs)))
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", line=dict(width=3), name="Head Path"))
            fig.update_layout(template='plotly_dark', height=420, title="Disk Head Movement (cylinder vs step)",
                              xaxis_title="Cylinder", yaxis_title="Step")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Bad input: {e}")

# -----------------------------------------
elif tab == "🧪 3D CPU Pulse":
    st.subheader("🧪 3D CPU Pulse (reacts to live CPU usage)")
    frames = st.slider("History Length", 20, 150, 60, key="pulse_len")
    xs = list(range(frames))
    ys = np.zeros(frames)
    zs = np.zeros(frames)
    for i in range(frames):
        cpu = psutil.cpu_percent(interval=0.05)
        ys[i] = np.sin(i/4) * (0.5 + cpu/200)  # amplitude up with CPU
        zs[i] = cpu
    fig = go.Figure(data=[go.Scatter3d(
        x=xs, y=ys, z=zs, mode='lines',
        line=dict(width=6, color=zs, colorscale='Viridis')
    )])
    fig.update_layout(template='plotly_dark', height=520,
                      scene=dict(
                        xaxis_title='Time step', yaxis_title='Pulse', zaxis_title='CPU %',
                        camera=dict(eye=dict(x=1.6,y=1.6,z=1.2))
                      ),
                      title="Futuristic Pulse • color = CPU% • amplitude reacts to load")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------
elif tab == "🛠️ Optimizer (Make Code Simpler & Faster)":
    st.subheader("🛠️ Practical Optimization Checklist")
    st.markdown("""
<div class='glass mono'>
<b>Python / Streamlit Simplifications</b>
1) Avoid repeated heavy computations in loops → cache models/data with <code>@st.cache_data</code> or <code>@st.cache_resource</code>.<br>
2) Replace nested if/else with dict-based dispatch (cleaner + faster).<br>
3) Vectorize with NumPy/Pandas; avoid per-row Python loops.<br>
4) Precompute Plotly figures only when inputs change; reuse figure objects.<br>
5) Reduce DataFrame size (astype('category'), float32); drop unused cols before display.<br>
6) Use unique <code>key=</code> on widgets generated in loops to prevent Streamlit duplication errors.<br>
7) For background-like updates, use timed reruns instead of blocking loops (<code>time.sleep</code> minimal).<br>
8) Profile with <code>cProfile</code> & <code>snakeviz</code>; identify top hotspots.<br>
9) Separate UI (Streamlit) from logic (plain .py helpers) for testability and maintainability.<br>
10) Keep functions pure (deterministic inputs→outputs) to simplify reasoning and caching.
<br><br>
<b>Memory Efficiency</b>
• Use generators/yield for streams; <br>
• Prefer lists of dicts → DataFrame once; <br>
• Downcast numeric dtypes; <br>
• Clear large objects (del / reassign) after use.
<br><br>
<b>Feasibility</b>
• Keep dependencies minimal (psutil, pandas, numpy, plotly, sklearn).<br>
• No internet required for theme/fonts; use system monospace fallback.<br>
• Move simulators into <code>live_scheduler.py</code> or <code>simulation/</code> to keep UI file small.
</div>
""", unsafe_allow_html=True)

# -----------------------------------------
elif tab == "🧰 Offline Code Sandbox":
    st.subheader("🧰 Offline Code Sandbox (local-only)")
    st.caption("Run Python locally. For other languages, save code to files (download) — execution requires local compilers.")
    lang = st.selectbox("Language", ["Python","C","C++","Java","JavaScript","Go","Rust","Kotlin","Swift","Bash","HTML","CSS","SQL","Other"], key="sb_lang")
    code = st.text_area("Code", height=260, key="sb_code", placeholder="# Write your code here...")
    colA, colB, colC = st.columns([1,1,1])
    run_py = colA.button("▶️ Run (Python only)", key="sb_run")
    dl = colB.button("⬇️ Download File", key="sb_dl")
    clr = colC.button("🧹 Clear", key="sb_clear")
    if run_py and lang=="Python":
        import contextlib, traceback, sys
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(code, {})
            st.success("✅ Output")
            st.code(buf.getvalue() or "(no output)", language="bash")
        except Exception:
            st.error("❌ Runtime Error")
            st.code(traceback.format_exc(), language="python")
    if dl:
        ext_map = {"Python":"py","C":"c","C++":"cpp","Java":"java","JavaScript":"js","Go":"go","Rust":"rs","Kotlin":"kt",
                   "Swift":"swift","Bash":"sh","HTML":"html","CSS":"css","SQL":"sql","Other":"txt"}
        fn = f"sandbox_snippet.{ext_map.get(lang,'txt')}"
        st.download_button("Save Code", code.encode("utf-8"), file_name=fn, mime="text/plain", key=f"dl_code_{time.time()}")
    if clr:
        st.session_state["sb_code"] = ""

# -----------------------------------------
# END

import pandas as pd

# -----------------------------
# First-Come-First-Serve (FCFS)
# -----------------------------
def fcfs(df):
    time = 0
    out = []
    for _, p in df.sort_values("Arrival").iterrows():
        time = max(time, p.Arrival)
        wt = time - p.Arrival
        time += p.Burst
        tat = time - p.Arrival
        out.append([p.Process, wt, tat])
    return pd.DataFrame(out, columns=["Process", "Waiting Time", "Turnaround Time"])


# -----------------------------a
# Shortest Job First (Non-Preemptive)
# -----------------------------
def sjf(df):
    time, done, out = 0, [], []
    while len(done) < len(df):
        ready = df[(df.Arrival <= time) & (~df.Process.isin(done))]
        if ready.empty:
            time += 1
            continue
        p = ready.sort_values("Burst").iloc[0]
        wt = time - p.Arrival
        time += p.Burst
        tat = time - p.Arrival
        done.append(p.Process)
        out.append([p.Process, wt, tat])
    return pd.DataFrame(out, columns=["Process", "Waiting Time", "Turnaround Time"])


# -----------------------------
# Priority Scheduling (Non-Preemptive)
# -----------------------------
def priority_scheduling(df):
    time, done, out = 0, [], []
    while len(done) < len(df):
        ready = df[(df.Arrival <= time) & (~df.Process.isin(done))]
        if ready.empty:
            time += 1
            continue
        p = ready.sort_values("Priority").iloc[0]  # lower number = higher priority
        wt = time - p.Arrival
        time += p.Burst
        tat = time - p.Arrival
        done.append(p.Process)
        out.append([p.Process, wt, tat])
    return pd.DataFrame(out, columns=["Process", "Waiting Time", "Turnaround Time"])


# -----------------------------
# Round Robin Scheduling
# -----------------------------
def round_robin(df, q):
    time = 0
    queue = []
    remaining = dict(zip(df.Process, df.Burst))
    arrived = set()
    wt = {p: 0 for p in df.Process}
    tat = {p: 0 for p in df.Process}

    while remaining:
        # Add newly arrived processes
        for p in df.Process:
            if df[df.Process == p].Arrival.values[0] <= time and p not in arrived:
                queue.append(p)
                arrived.add(p)

        if not queue:
            time += 1
            continue

        cur = queue.pop(0)
        exec_time = min(q, remaining[cur])
        time += exec_time
        remaining[cur] -= exec_time

        # Add newly arrived during execution
        for p in df.Process:
            if df[df.Process == p].Arrival.values[0] <= time and p not in arrived:
                queue.append(p)
                arrived.add(p)

        if remaining[cur] == 0:
            tat[cur] = time - df[df.Process == cur].Arrival.values[0]
            wt[cur] = tat[cur] - df[df.Process == cur].Burst.values[0]
            del remaining[cur]
        else:
            queue.append(cur)

    out = [[p, wt[p], tat[p]] for p in df.Process]
    return pd.DataFrame(out, columns=["Process", "Waiting Time", "Turnaround Time"])



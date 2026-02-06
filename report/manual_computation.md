# 📊 Manual Computation Guide for CPU Scheduling Algorithms

This guide provides step-by-step instructions for manually calculating CPU scheduling algorithm results. Understanding manual computation helps verify simulation results and deepens your understanding of scheduling concepts.

---

## 📋 Table of Contents

1. [Common Terminology](#common-terminology)
2. [First-Come-First-Serve (FCFS)](#1-first-come-first-serve-fcfs)
3. [Shortest Job First (SJF)](#2-shortest-job-first-sjf)
4. [Priority Scheduling](#3-priority-scheduling)
5. [Round Robin (RR)](#4-round-robin-rr)
6. [Performance Metrics Calculation](#5-performance-metrics-calculation)
7. [Practice Problems](#6-practice-problems)

---

## Common Terminology

| Term | Symbol | Definition |
|------|--------|------------|
| **Arrival Time** | AT | Time when process enters ready queue |
| **Burst Time** | BT | Time required by CPU for execution |
| **Completion Time** | CT | Time when process finishes execution |
| **Turnaround Time** | TAT | Total time from arrival to completion (TAT = CT - AT) |
| **Waiting Time** | WT | Time spent waiting in ready queue (WT = TAT - BT) |
| **Response Time** | RT | Time from arrival to first execution |
| **Time Quantum** | TQ | Fixed time slice for Round Robin |

---

## 1. First-Come-First-Serve (FCFS)

### Algorithm
- Processes are executed in order of arrival
- Non-preemptive: once started, runs to completion
- Simple queue-based implementation

### Step-by-Step Calculation

**Given Example:**
| Process | Arrival Time | Burst Time |
|---------|-------------|------------|
| P1      | 0           | 5          |
| P2      | 2           | 3          |
| P3      | 4           | 2          |

**Step 1: Sort by Arrival Time**
```
P1 (AT=0), P2 (AT=2), P3 (AT=4)
```

**Step 2: Calculate Completion Times**
```
Time = 0
P1: Start at max(0, 0) = 0, End at 0 + 5 = 5
Time = 5
P2: Start at max(5, 2) = 5, End at 5 + 3 = 8
Time = 8
P3: Start at max(8, 4) = 8, End at 8 + 2 = 10
```

**Step 3: Calculate TAT and WT**
```
P1: TAT = 5 - 0 = 5, WT = 5 - 5 = 0
P2: TAT = 8 - 2 = 6, WT = 6 - 3 = 3
P3: TAT = 10 - 4 = 6, WT = 6 - 2 = 4
```

**Results Table:**
| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1      | 0  | 5  | 5  | 5   | 0  |
| P2      | 2  | 3  | 8  | 6   | 3  |
| P3      | 4  | 2  | 10 | 6   | 4  |

**Averages:**
- Average TAT = (5 + 6 + 6) / 3 = 5.67
- Average WT = (0 + 3 + 4) / 3 = 2.33

### Gantt Chart
```
| P1 (0-5) | P2 (5-8) | P3 (8-10) |
```

---

## 2. Shortest Job First (SJF)

### Algorithm
- Select process with shortest burst time from available processes
- Non-preemptive version: no interruption once started
- Minimizes average waiting time

### Step-by-Step Calculation

**Given Example:**
| Process | Arrival Time | Burst Time |
|---------|-------------|------------|
| P1      | 0           | 7          |
| P2      | 2           | 4          |
| P3      | 4           | 1          |
| P4      | 5           | 4          |

**Step 1: Initialize**
```
Time = 0, Done = []
```

**Step 2: Time = 0**
```
Available: P1 (AT=0, BT=7)
Select: P1 (only available)
Start: 0, End: 0 + 7 = 7
Done: [P1]
```

**Step 3: Time = 7**
```
Available: P2 (AT=2, BT=4), P3 (AT=4, BT=1), P4 (AT=5, BT=4)
Select: P3 (shortest BT=1)
Start: 7, End: 7 + 1 = 8
Done: [P1, P3]
```

**Step 4: Time = 8**
```
Available: P2 (AT=2, BT=4), P4 (AT=5, BT=4)
Select: P2 (tie, arrived first)
Start: 8, End: 8 + 4 = 12
Done: [P1, P3, P2]
```

**Step 5: Time = 12**
```
Available: P4 (AT=5, BT=4)
Select: P4
Start: 12, End: 12 + 4 = 16
Done: [P1, P3, P2, P4]
```

**Results Table:**
| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1      | 0  | 7  | 7  | 7   | 0  |
| P2      | 2  | 4  | 12 | 10  | 6  |
| P3      | 4  | 1  | 8  | 4   | 3  |
| P4      | 5  | 4  | 16 | 11  | 7  |

**Averages:**
- Average TAT = (7 + 10 + 4 + 11) / 4 = 8.0
- Average WT = (0 + 6 + 3 + 7) / 4 = 4.0

### Gantt Chart
```
| P1 (0-7) | P3 (7-8) | P2 (8-12) | P4 (12-16) |
```

---

## 3. Priority Scheduling

### Algorithm
- Select process with highest priority (lowest number) from available processes
- Non-preemptive: runs to completion once started
- Lower number = Higher priority

### Step-by-Step Calculation

**Given Example:**
| Process | Arrival Time | Burst Time | Priority |
|---------|-------------|------------|----------|
| P1      | 0           | 10         | 3        |
| P2      | 0           | 5          | 1        |
| P3      | 0           | 8          | 2        |
| P4      | 0           | 4          | 4        |

**Step 1: Time = 0**
```
Available: All processes (AT=0)
Priorities: P2(1), P3(2), P1(3), P4(4)
Select: P2 (highest priority)
Start: 0, End: 0 + 5 = 5
Done: [P2]
```

**Step 2: Time = 5**
```
Available: P1, P3, P4
Priorities: P3(2), P1(3), P4(4)
Select: P3
Start: 5, End: 5 + 8 = 13
Done: [P2, P3]
```

**Step 3: Time = 13**
```
Available: P1, P4
Priorities: P1(3), P4(4)
Select: P1
Start: 13, End: 13 + 10 = 23
Done: [P2, P3, P1]
```

**Step 4: Time = 23**
```
Available: P4
Select: P4
Start: 23, End: 23 + 4 = 27
Done: [P2, P3, P1, P4]
```

**Results Table:**
| Process | AT | BT | Priority | CT | TAT | WT |
|---------|----|----|----------|----|-----|----|
| P1      | 0  | 10 | 3        | 23 | 23  | 13 |
| P2      | 0  | 5  | 1        | 5  | 5   | 0  |
| P3      | 0  | 8  | 2        | 13 | 13  | 5  |
| P4      | 0  | 4  | 4        | 27 | 27  | 23 |

**Averages:**
- Average TAT = (23 + 5 + 13 + 27) / 4 = 17.0
- Average WT = (13 + 0 + 5 + 23) / 4 = 10.25

### Gantt Chart
```
| P2 (0-5) | P3 (5-13) | P1 (13-23) | P4 (23-27) |
```

---

## 4. Round Robin (RR)

### Algorithm
- Each process gets a small unit of CPU time (time quantum)
- After quantum expires, process moves to end of queue
- Preemptive: processes can be interrupted

### Step-by-Step Calculation

**Given Example:**
| Process | Arrival Time | Burst Time |
|---------|-------------|------------|
| P1      | 0           | 5          |
| P2      | 1           | 4          |
| P3      | 2           | 2          |
| P4      | 3           | 3          |

**Time Quantum = 2**

**Step 1: Initialize**
```
Time = 0
Queue = []
Remaining: P1=5, P2=4, P3=2, P4=3
Arrived = {}
```

**Step 2: Time = 0**
```
New arrivals: P1
Queue: [P1]
Execute P1 for 2 units: Remaining P1=3
Time = 2
New arrivals: P2, P3
Queue: [P2, P3, P1]
```

**Step 3: Time = 2**
```
Execute P2 for 2 units: Remaining P2=2
Time = 4
New arrivals: P4
Queue: [P3, P1, P4, P2]
```

**Step 4: Time = 4**
```
Execute P3 for 2 units: Remaining P3=0 → COMPLETE
TAT(P3) = 4 - 2 = 2, WT(P3) = 2 - 2 = 0
Time = 6
Queue: [P1, P4, P2]
```

**Step 5: Time = 6**
```
Execute P1 for 2 units: Remaining P1=1
Time = 8
Queue: [P4, P2, P1]
```

**Step 6: Time = 8**
```
Execute P4 for 2 units: Remaining P4=1
Time = 10
Queue: [P2, P1, P4]
```

**Step 7: Time = 10**
```
Execute P2 for 2 units: Remaining P2=0 → COMPLETE
TAT(P2) = 10 - 1 = 9, WT(P2) = 9 - 4 = 5
Time = 12
Queue: [P1, P4]
```

**Step 8: Time = 12**
```
Execute P1 for 1 unit: Remaining P1=0 → COMPLETE
TAT(P1) = 12 - 0 = 12, WT(P1) = 12 - 5 = 7
Time = 13
Queue: [P4]
```

**Step 9: Time = 13**
```
Execute P4 for 1 unit: Remaining P4=0 → COMPLETE
TAT(P4) = 13 - 3 = 10, WT(P4) = 10 - 3 = 7
Time = 14
Queue: []
```

**Results Table:**
| Process | AT | BT | CT | TAT | WT | RT |
|---------|----|----|----|-----|----|----|
| P1      | 0  | 5  | 12 | 12  | 7  | 0  |
| P2      | 1  | 4  | 10 | 9   | 5  | 1  |
| P3      | 2  | 2  | 6  | 4   | 2  | 2  |
| P4      | 3  | 3  | 14 | 11  | 8  | 5  |

**Averages:**
- Average TAT = (12 + 9 + 4 + 11) / 4 = 9.0
- Average WT = (7 + 5 + 2 + 8) / 4 = 5.5
- Average RT = (0 + 1 + 2 + 5) / 4 = 2.0

### Gantt Chart
```
| P1(0-2) | P2(2-4) | P3(4-6) | P1(6-8) | P4(8-10) | P2(10-12) | P1(12-13) | P4(13-14) |
```

---

## 5. Performance Metrics Calculation

### Basic Metrics

**Formulas:**
```
Turnaround Time (TAT) = Completion Time - Arrival Time
Waiting Time (WT) = Turnaround Time - Burst Time
Response Time (RT) = First Start Time - Arrival Time
```

**Averages:**
```
Average TAT = Σ(TAT) / Number of Processes
Average WT = Σ(WT) / Number of Processes
Average RT = Σ(RT) / Number of Processes
```

### Advanced Metrics

**CPU Utilization:**
```
CPU Utilization % = (Total Busy Time / Total Time) × 100
```

**Throughput:**
```
Throughput = Number of Processes / Total Time
```

**Fairness Index:**
```
Fairness Index = 1 / (1 + Variance of Waiting Times)
Range: 0 to 1 (1 = perfectly fair)
```

**Efficiency Ratio:**
```
Efficiency = Total Burst Time / Total Time
```

### Example Calculation

Using FCFS results from Section 1:
| Process | WT | TAT |
|---------|----|-----|
| P1      | 0  | 5   |
| P2      | 3  | 6   |
| P3      | 4  | 6   |

**Basic Metrics:**
- Average WT = (0 + 3 + 4) / 3 = 2.33
- Average TAT = (5 + 6 + 6) / 3 = 5.67

**CPU Utilization:**
- Total Busy Time = 5 + 3 + 2 = 10
- Total Time = 10
- CPU Utilization = (10 / 10) × 100 = 100%

**Throughput:**
- Throughput = 3 / 10 = 0.3 processes/unit time

**Fairness:**
- Mean WT = 2.33
- Variance = [(0-2.33)² + (3-2.33)² + (4-2.33)²] / 3 = 2.89
- Fairness Index = 1 / (1 + 2.89) = 0.26

---

## 6. Practice Problems

### Problem 1: FCFS
**Given:**
| Process | AT | BT |
|---------|----|----|
| P1      | 0  | 8  |
| P2      | 1  | 4  |
| P3      | 2  | 9  |
| P4      | 3  | 5  |

**Calculate:**
1. Completion times
2. Turnaround times
3. Waiting times
4. Average TAT and WT
5. CPU utilization

<details>
<summary>Click for Solution</summary>

**Solution:**
| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1      | 0  | 8  | 8  | 8   | 0  |
| P2      | 1  | 4  | 12 | 11  | 7  |
| P3      | 2  | 9  | 21 | 19  | 10 |
| P4      | 3  | 5  | 26 | 23  | 18 |

- Average TAT = (8 + 11 + 19 + 23) / 4 = 15.25
- Average WT = (0 + 7 + 10 + 18) / 4 = 8.75
- CPU Utilization = 100% (no idle time)

</details>

### Problem 2: SJF
**Given:**
| Process | AT | BT |
|---------|----|----|
| P1      | 0  | 6  |
| P2      | 2  | 2  |
| P3      | 3  | 8  |
| P4      | 4  | 3  |
| P5      | 4  | 4  |

**Calculate:**
1. Execution order
2. All times (CT, TAT, WT)
3. Averages

<details>
<summary>Click for Solution</summary>

**Solution:**
Execution Order: P1 → P2 → P4 → P5 → P3

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1      | 0  | 6  | 6  | 6   | 0  |
| P2      | 2  | 2  | 8  | 6   | 4  |
| P3      | 3  | 8  | 21 | 18  | 10 |
| P4      | 3  | 3  | 11 | 7   | 4  |
| P5      | 4  | 4  | 15 | 11  | 7  |

- Average TAT = (6 + 6 + 18 + 7 + 11) / 5 = 9.6
- Average WT = (0 + 4 + 10 + 4 + 7) / 5 = 5.0

</details>

### Problem 3: Round Robin
**Given:**
| Process | AT | BT |
|---------|----|----|
| P1      | 0  | 4  |
| P2      | 1  | 3  |
| P3      | 2  | 2  |

**Time Quantum = 2**

**Calculate:**
1. Gantt chart
2. All times
3. Response times

<details>
<summary>Click for Solution</summary>

**Gantt Chart:**
```
| P1(0-2) | P2(2-4) | P3(4-6) | P1(6-8) | P2(8-9) |
```

| Process | AT | BT | CT | TAT | WT | RT |
|---------|----|----|----|-----|----|----|
| P1      | 0  | 4  | 8  | 8   | 4  | 0  |
| P2      | 1  | 3  | 9  | 8   | 5  | 1  |
| P3      | 2  | 2  | 6  | 4   | 2  | 2  |

- Average TAT = (8 + 8 + 4) / 3 = 6.67
- Average WT = (4 + 5 + 2) / 3 = 3.67
- Average RT = (0 + 1 + 2) / 3 = 1.0

</details>

---

## 📝 Summary Checklist

When manually computing scheduling results:

- [ ] Sort processes by arrival time (if needed)
- [ ] Track current time throughout calculation
- [ ] Identify available processes at each step
- [ ] Apply algorithm selection criteria (FCFS: arrival order, SJF: shortest BT, Priority: highest priority, RR: queue order)
- [ ] Calculate CT, TAT, WT for each process
- [ ] Compute averages
- [ ] Draw Gantt chart for visualization
- [ ] Verify calculations by checking: TAT = CT - AT and WT = TAT - BT

---

## 🔍 Verification Tips

1. **Consistency Check:** TAT should always be ≥ BT (since TAT = BT + WT)
2. **WT Check:** WT should never be negative
3. **Time Continuity:** Gantt chart should have no gaps (unless CPU is idle)
4. **Sum Check:** Total busy time should equal sum of all burst times
5. **Response Time:** For non-preemptive algorithms, RT = WT

---

*This manual computation guide helps you understand the fundamental calculations behind CPU scheduling algorithms. Use it to verify simulation results and prepare for examinations.*

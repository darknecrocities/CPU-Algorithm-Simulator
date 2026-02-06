# 🖥️ Operating System Analysis: CPU Scheduling Algorithms

A comprehensive analysis of CPU scheduling algorithms, their characteristics, performance implications, and real-world applications in modern operating systems.

---

## 📋 Table of Contents

1. [Introduction to CPU Scheduling](#1-introduction-to-cpu-scheduling)
2. [Scheduling Criteria](#2-scheduling-criteria)
3. [Algorithm Analysis](#3-algorithm-analysis)
4. [Performance Comparison](#4-performance-comparison)
5. [Real-World Applications](#5-real-world-applications)
6. [Advanced Topics](#6-advanced-topics)
7. [Case Studies](#7-case-studies)

---

## 1. Introduction to CPU Scheduling

### What is CPU Scheduling?

CPU scheduling is the basis of multiprogrammed operating systems. By switching the CPU among processes, the operating system can make the computer more productive. The objective of multiprogramming is to have some process running at all times, to maximize CPU utilization.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **CPU Burst** | Period when process uses CPU for execution |
| **I/O Burst** | Period when process waits for I/O completion |
| **Dispatcher** | Module that gives control of CPU to selected process |
| **Dispatch Latency** | Time taken to stop one process and start another |
| **Context Switch** | Saving state of old process and loading state of new process |

### Types of Scheduling

1. **Long-term Scheduling** (Job Scheduling)
   - Decides which processes are admitted to the system
   - Controls degree of multiprogramming

2. **Medium-term Scheduling**
   - Handles swapped-out processes
   - Part of swapping function

3. **Short-term Scheduling** (CPU Scheduling)
   - Decides which ready process executes next
   - Executes most frequently (milliseconds)
   - Focus of this analysis

---

## 2. Scheduling Criteria

### Primary Criteria

| Criterion | Goal | Measurement |
|-----------|------|-------------|
| **CPU Utilization** | Maximize | Percentage of time CPU is busy |
| **Throughput** | Maximize | Number of processes completed per time unit |
| **Turnaround Time** | Minimize | Time from submission to completion |
| **Waiting Time** | Minimize | Time spent in ready queue |
| **Response Time** | Minimize | Time from request to first response |

### Secondary Criteria

- **Fairness**: All processes should be treated equally
- **Predictability**: Same job should take similar time regardless of system load
- **Priority Enforcement**: Higher priority processes should be preferred
- **Resource Balance**: Keep all system resources busy

### Trade-offs

```
Low Response Time vs. High Throughput
    ↓
Interactive systems need low response time
Batch systems need high throughput

Fairness vs. Priority
    ↓
Equal treatment vs. important jobs first
```

---

## 3. Algorithm Analysis

### 3.1 First-Come-First-Serve (FCFS)

#### Characteristics
- **Type**: Non-preemptive
- **Implementation**: Simple queue (FIFO)
- **Selection**: Process that arrived first

#### Advantages
- ✅ Simple to understand and implement
- ✅ No starvation (all processes eventually run)
- ✅ Low overhead (minimal bookkeeping)

#### Disadvantages
- ❌ Convoy effect: short processes wait behind long ones
- ❌ Poor average waiting time with varying burst times
- ❌ Non-preemptive: unsuitable for time-sharing systems

#### Mathematical Analysis

**Convoy Effect Example:**
```
Processes: P1(BT=24), P2(BT=3), P3(BT=3)
Arrival: All at time 0

Execution Order: P1 → P2 → P3

Waiting Times:
P1: 0
P2: 24
P3: 27
Average WT: (0 + 24 + 27) / 3 = 17

If order was P2 → P3 → P1:
Waiting Times:
P2: 0
P3: 3
P1: 6
Average WT: (0 + 3 + 6) / 3 = 3

Improvement: 82% reduction in average waiting time!
```

#### Best Use Cases
- Batch processing systems
- Background jobs where response time isn't critical
- Systems with similar job lengths

---

### 3.2 Shortest Job First (SJF)

#### Characteristics
- **Type**: Can be preemptive (SRTF) or non-preemptive
- **Implementation**: Priority queue based on burst time
- **Selection**: Process with shortest burst time

#### Advantages
- ✅ Optimal average waiting time (provably minimum)
- ✅ Maximizes throughput
- ✅ Reduces average response time for short jobs

#### Disadvantages
- ❌ Starvation: long processes may never execute
- ❌ Requires prediction of burst times (usually unknown)
- ❌ Preemptive version has high context switch overhead

#### Burst Time Prediction

Since actual burst times are unknown, OS uses estimation:

**Exponential Averaging:**
```
τ(n+1) = α × t(n) + (1-α) × τ(n)

Where:
τ(n+1) = predicted burst time for next CPU burst
t(n)   = actual length of nth CPU burst
α      = smoothing factor (0 ≤ α ≤ 1), typically 0.5
τ(n)   = previous prediction
```

**Example:**
```
α = 0.5, Initial guess = 10

Actual: 6, 4, 6, 4, 13, 13, 13, ...
Predictions:
τ1 = 0.5×6 + 0.5×10 = 8
τ2 = 0.5×4 + 0.5×8 = 6
τ3 = 0.5×6 + 0.5×6 = 6
τ4 = 0.5×4 + 0.5×6 = 5
τ5 = 0.5×13 + 0.5×5 = 9
```

#### Best Use Cases
- Batch systems where job lengths are known
- Systems with predictable workloads
- Environments favoring short interactive tasks

---

### 3.3 Priority Scheduling

#### Characteristics
- **Type**: Can be preemptive or non-preemptive
- **Implementation**: Priority queue
- **Selection**: Process with highest priority (lowest number)

#### Priority Assignment Methods

**Static Priority:**
- Fixed at process creation
- Based on process type, user importance, or payment

**Dynamic Priority:**
- Changes based on execution history
- Aging: priority increases as waiting time increases
- Penalty: priority decreases after using CPU

#### Aging Technique (Solution to Starvation)

```
Priority = Initial_Priority + (Waiting_Time / Time_Quantum)

Example:
Initial Priority: 10
After waiting 100 time units with quantum 10:
New Priority = 10 + (100/10) = 20 (higher priority)
```

#### Advantages
- ✅ Important processes get preference
- ✅ Flexible priority schemes possible
- ✅ Can implement various policies

#### Disadvantages
- ❌ Starvation of low-priority processes
- ❌ Priority inversion problems
- ❌ Difficult to determine appropriate priorities

#### Priority Inversion Problem

**Scenario:**
- High priority process H needs resource held by low priority process L
- Medium priority process M preempts L
- Result: H waits for M and L (inverted priority!)

**Solution: Priority Inheritance**
- L temporarily inherits H's priority
- Prevents M from preempting L
- H gets resource faster

#### Best Use Cases
- Real-time systems
- Systems with varying importance levels
- Multi-user systems with different service levels

---

### 3.4 Round Robin (RR)

#### Characteristics
- **Type**: Preemptive
- **Implementation**: Circular queue with time quantum
- **Selection**: Each process gets equal time slice

#### Time Quantum Selection

**Too Large:**
- Approaches FCFS behavior
- Poor response time
- Low context switch overhead

**Too Small:**
- Many context switches
- High overhead (typically 1-10% of quantum)
- Better response time

**Optimal Range:**
```
Time Quantum ≈ 80% of average burst time
Typical values: 10-100 milliseconds
```

**Context Switch Impact:**
```
If:
- Time Quantum = 20ms
- Context Switch = 1ms
- 50 processes

Overhead = 1/21 = 4.76% of CPU time
```

#### Advantages
- ✅ Fair: all processes get equal CPU time
- ✅ Good average response time
- ✅ No starvation
- ✅ Suitable for time-sharing systems

#### Disadvantages
- ❌ Poor waiting time for long processes
- ❌ Performance depends heavily on time quantum
- ❌ Higher context switch overhead
- ❌ Not optimal for I/O-bound processes

#### Variations

**Virtual Round Robin:**
- Separate queue for I/O-bound processes
- I/O completion moves process to auxiliary queue
- Auxiliary queue gets preference over main queue

**Multilevel Queue:**
- Multiple RR queues with different quanta
- Higher priority queues get smaller quanta
- Processes can move between queues

#### Best Use Cases
- Time-sharing systems
- Interactive systems
- Systems requiring fair CPU distribution
- Multi-user environments

---

## 4. Performance Comparison

### Theoretical Analysis

| Algorithm | Avg WT | Avg RT | Fairness | Overhead | Starvation |
|-----------|--------|--------|----------|----------|------------|
| **FCFS** | Poor | Poor | Fair | Low | No |
| **SJF** | Optimal | Good | Unfair | Low | Yes |
| **Priority** | Variable | Variable | Unfair | Low | Yes |
| **Round Robin** | Fair | Good | Fair | High | No |

### Simulation Results Analysis

**Typical Workload Characteristics:**
- 70% I/O-bound processes (short bursts)
- 30% CPU-bound processes (long bursts)
- Arrival times follow Poisson distribution
- Burst times follow exponential distribution

**Performance Metrics Comparison:**

```
Scenario: 10 processes, mixed workload

Algorithm      | Avg WT | Avg TAT | CPU Util | Throughput
---------------|--------|---------|----------|-----------
FCFS           | 15.2   | 22.4    | 92%      | 0.45
SJF            | 8.7    | 15.9    | 95%      | 0.63
Priority       | 12.1   | 19.3    | 93%      | 0.52
Round Robin    | 11.8   | 18.7    | 89%      | 0.58
               | (q=10) |         |          |
```

### Decision Matrix

**Choose FCFS when:**
- Simple implementation is priority
- Jobs have similar lengths
- Batch processing environment
- Overhead must be minimized

**Choose SJF when:**
- Minimizing average waiting time is critical
- Job lengths are predictable
- Batch system with known workloads
- Can tolerate starvation risk

**Choose Priority when:**
- Different service levels required
- Real-time constraints exist
- System has critical processes
- Can implement aging to prevent starvation

**Choose Round Robin when:**
- Time-sharing environment
- Fairness is important
- Interactive response needed
- Process lengths are unknown

---

## 5. Real-World Applications

### 5.1 Windows Operating System

**Scheduler Type:** Multilevel Feedback Queue (MLFQ) with priority classes

**Characteristics:**
- 32 priority levels (0-31)
- Real-time priorities: 16-31
- Variable priorities: 1-15
- Idle thread: priority 0

**Implementation:**
```
┌─────────────────────────────────────┐
│  Real-Time Priority (16-31)         │
│  - Never adjusted                   │
│  - Absolute priority                │
├─────────────────────────────────────┤
│  High Priority (11-15)              │
│  - Administrative tasks             │
├─────────────────────────────────────┤
│  Normal Priority (6-10)             │
│  - Default for user processes       │
│  - Dynamic adjustment               │
├─────────────────────────────────────┤
│  Idle Priority (1-5)                │
│  - Background tasks                 │
└─────────────────────────────────────┘
```

**Time Quantum:**
- Default: 2 clock ticks (≈20-30ms)
- Foreground applications: 3 ticks
- Background services: 1 tick

### 5.2 Linux (CFS - Completely Fair Scheduler)

**Scheduler Type:** Fair-share scheduling with red-black tree

**Key Features:**
- **Virtual Runtime (vruntime):** Tracks CPU time used
- **Weight-based:** Priorities affect time allocation proportionally
- **Red-black tree:** O(log n) process selection
- **Nanosecond granularity:** High precision timing

**Formula:**
```
vruntime = actual_runtime × (NICE_0_LOAD / process_weight)

Where:
- NICE_0_LOAD = 1024 (default)
- process_weight based on nice value (-20 to +19)
```

**Nice Value Weights:**
```
Nice: -20  -10   0   +10  +19
Weight: 88761 11058 1024  110  15
Ratio: 86.7   10.8   1   0.1  0.01
```

**Target Latency:**
- Default: 6ms (for 2+ tasks)
- Scales with number of tasks: latency = 6ms × (nr_running / 2)

### 5.3 macOS (Mach Scheduler)

**Scheduler Type:** Multilevel feedback queue with work queues

**Features:**
- 128 priority levels (0-127)
- 4 scheduling classes:
  - NORMAL (0-63)
  - SYSTEM (64-95)
  - REALTIME (96-127)
  - KERNEL (fixed priorities)

**Time Quantum:**
- Varies by priority level
- Higher priority = longer quantum
- Range: 10ms to 100ms

### 5.4 Mobile Systems (Android/iOS)

**Android:**
- Linux CFS with modifications
- Cgroups for app groups
- Background execution limits
- Doze mode for battery optimization

**iOS:**
- Mach-based scheduler
- Strict background execution policies
- QoS (Quality of Service) classes:
  - User Interactive
  - User Initiated
  - Default
  - Utility
  - Background

---

## 6. Advanced Topics

### 6.1 Multiprocessor Scheduling

**Approaches:**

1. **Asymmetric Multiprocessing**
   - One processor (master) handles all scheduling
   - Simple but master is bottleneck
   - Used in early multiprocessor systems

2. **Symmetric Multiprocessing (SMP)**
   - Each processor schedules itself
   - Two variants:

   **a) Per-Processor Ready Queue**
   ```
   Pros:
   - No contention for ready queue
   - Better cache affinity
   
   Cons:
   - Load imbalance possible
   - Complex load balancing needed
   ```

   **b) Common Ready Queue**
   ```
   Pros:
   - Automatic load balancing
   - Simpler implementation
   
   Cons:
   - Lock contention on ready queue
   - Cache affinity issues
   ```

**Load Balancing Techniques:**
- **Push Migration:** Periodic task migration from busy to idle CPUs
- **Pull Migration:** Idle CPUs pull tasks from busy ones
- **Affinity Scheduling:** Try to keep process on same CPU for cache efficiency

### 6.2 Real-Time Scheduling

**Types of Real-Time Systems:**

1. **Hard Real-Time**
   - Deadline must be met
   - System fails if deadline missed
   - Examples: Airbag control, pacemakers

2. **Soft Real-Time**
   - Deadline should be met
   - System degrades but continues if deadline missed
   - Examples: Video streaming, online gaming

**Scheduling Algorithms:**

**Rate Monotonic (RM):**
- Static priority based on period
- Shorter period = Higher priority
- Optimal for fixed-priority scheduling
- Utilization bound: n(2^(1/n) - 1) → 69.3% as n→∞

**Earliest Deadline First (EDF):**
- Dynamic priority based on deadline
- Earlier deadline = Higher priority
- Optimal utilization: 100%
- Requires more computation

### 6.3 Thread Scheduling

**User-Level Threads:**
- Thread library manages scheduling
- Kernel unaware of threads
- Scheduling within process

**Kernel-Level Threads:**
- OS schedules threads directly
- More overhead but better parallelism
- Thread blocking doesn't block process

**Scheduling Models:**

1. **Many-to-One:** Many user threads → One kernel thread
2. **One-to-One:** One user thread → One kernel thread
3. **Many-to-Many:** Many user threads → Many kernel threads

### 6.4 Energy-Aware Scheduling

**Challenges:**
- Battery life critical in mobile devices
- CPU power consumption ∝ frequency³
- Trade-off between performance and energy

**Techniques:**

**DVFS (Dynamic Voltage and Frequency Scaling):**
```
Power = Capacitance × Voltage² × Frequency

Reduce frequency → Quadratic power savings
But: Execution time increases
```

**Race-to-Halt:**
- Run at maximum speed then sleep
- More efficient than slow continuous execution
- Due to static power consumption

**Core Parking:**
- Turn off unused CPU cores
- Consolidate tasks on active cores
- Significant power savings

---

## 7. Case Studies

### Case Study 1: Web Server Optimization

**Scenario:**
High-traffic web server handling:
- Static content requests (short, I/O-bound)
- Dynamic content generation (medium, CPU+I/O)
- Database queries (variable, I/O-bound)
- Administrative tasks (low priority)

**Solution: Multilevel Queue with Feedback**

```
┌─────────────────────────────────────────┐
│ Queue 0: Real-time (admin monitoring)   │
│ - Priority: Highest                     │
│ - Quantum: 50ms                         │
│ - Preemptive                            │
├─────────────────────────────────────────┤
│ Queue 1: Interactive (dynamic content)│
│ - Priority: High                        │
│ - Quantum: 20ms                         │
│ - Feedback: I/O completion boosts       │
├─────────────────────────────────────────┤
│ Queue 2: Standard (static content)      │
│ - Priority: Normal                      │
│ - Quantum: 10ms                         │
│ - FCFS within queue                     │
├─────────────────────────────────────────┤
│ Queue 3: Background (logs, cleanup)     │
│ - Priority: Low                         │
│ - Quantum: 5ms                          │
│ - Only when others empty                │
└─────────────────────────────────────────┘
```

**Results:**
- 40% improvement in response time
- 99th percentile latency reduced by 60%
- CPU utilization maintained at 85%

### Case Study 2: Gaming Console Scheduler

**Scenario:**
Gaming console requirements:
- Real-time rendering (16.67ms frame budget at 60fps)
- Audio processing (strict latency requirements)
- Background downloads
- System maintenance

**Solution: Hybrid Priority + EDF**

```
Critical Path (Rendering):
- Hard real-time constraints
- EDF scheduling for frame deadlines
- Dedicated CPU core if possible

Audio Processing:
- High priority, periodic
- Rate monotonic scheduling
- Lock to specific core for cache

Background Tasks:
- Best-effort scheduling
- Run during V-sync intervals
- Aggressive power saving
```

**Implementation:**
- Frame deadline: 16.67ms
- Audio buffer: 5ms latency target
- Background tasks: Only in idle time
- Result: Consistent 60fps, minimal audio lag

### Case Study 3: Cloud Data Center

**Scenario:**
Virtualized environment with:
- Thousands of VMs
- Mixed workloads (batch + interactive)
- Service level agreements (SLAs)
- Energy efficiency requirements

**Solution: Two-Level Scheduling**

**Level 1: VM Scheduler (Global)**
- Fair share allocation
- Weighted based on payment tier
- Work-conserving: unused capacity redistributed

**Level 2: Guest OS Scheduler (Per-VM)**
- Standard Linux CFS
- Modified for virtualized environment
- Aware of stolen time

**Algorithm: Weighted Fair Queuing**
```
VM Allocation = (VM_weight / Total_weight) × Available_capacity

With work conservation:
If VM underutilizes allocation → Others can use excess
```

**Results:**
- 95% SLA compliance
- 30% energy reduction through consolidation
- 99.9% resource utilization

---

## 📊 Summary and Recommendations

### Algorithm Selection Guide

```
┌─────────────────────────────────────────────────────────────┐
│                    DECISION FLOWCHART                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │ Need real-time│──Yes──→ Use Rate Monotonic or EDF        │
│  │ constraints?  │                                          │
│  └───────┬──────┘                                           │
│          │ No                                                │
│          ▼                                                   │
│  ┌──────────────┐                                           │
│  │ Interactive  │──Yes──→ Use Round Robin or MLFQ           │
│  │ time-sharing?│                                          │
│  └───────┬──────┘                                           │
│          │ No                                                │
│          ▼                                                   │
│  ┌──────────────┐                                           │
│  │ Job lengths  │──Known──→ Use SJF                         │
│  │ predictable? │                                          │
│  └───────┬──────┘                                           │
│          │ Unknown                                          │
│          ▼                                                   │
│  ┌──────────────┐                                           │
│  │ Different    │──Yes──→ Use Priority with aging           │
│  │ priorities?  │                                          │
│  └───────┬──────┘                                           │
│          │ No                                                │
│          ▼                                                   │
│     → Use FCFS or Round Robin                               │
│       (Simple and fair)                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Key Takeaways

1. **No single algorithm is best for all scenarios**
   - Match algorithm to workload characteristics
   - Consider hybrid approaches

2. **Modern systems use complex schedulers**
   - Linux CFS: Fair share with O(log n) complexity
   - Windows: Multilevel queue with 32 priorities
   - Both combine multiple scheduling concepts

3. **Context switch overhead matters**
   - Too frequent switching wastes CPU
   - Too infrequent hurts responsiveness
   - Balance is critical

4. **Fairness vs. Efficiency trade-off**
   - Fair schedulers (RR) may sacrifice efficiency
   - Efficient schedulers (SJF) may cause starvation
   - Modern schedulers try to balance both

5. **Real-world schedulers are adaptive**
   - Dynamic priority adjustment
   - Load balancing across cores
   - Energy-aware decisions

---

## 📚 Further Reading

### Books
- "Operating System Concepts" (Silberschatz, Galvin, Gagne)
- "Modern Operating Systems" (Andrew S. Tanenbaum)
- "Understanding the Linux Kernel" (Daniel P. Bovet)

### Papers
- "The Linux Scheduler: A Decade of Wasted Cores" (EuroSys 2016)
- "Energy Aware Scheduling for Real-Time Systems" (IEEE 2019)
- "Fairness and Performance in Multiprocessor Scheduling" (ACM 2020)

### Online Resources
- Linux Kernel Documentation: scheduler/
- Microsoft Docs: Windows Internals
- ACM Queue: Scheduling articles

---

*This analysis provides a comprehensive understanding of CPU scheduling algorithms, their theoretical foundations, practical implementations, and real-world applications in modern operating systems.*

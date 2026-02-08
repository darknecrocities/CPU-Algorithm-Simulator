import streamlit as st
import pandas as pd

# Predefined scenarios for quick testing
PREDEFINED_SCENARIOS = {
    "Custom (Manual Entry)": None,
    "🎮 Gaming Workload (CPU Intensive)": {
        "processes": [
            {"name": "P1", "arrival": 0, "burst": 8, "priority": 2},
            {"name": "P2", "arrival": 1, "burst": 4, "priority": 1},
            {"name": "P3", "arrival": 2, "burst": 9, "priority": 3},
            {"name": "P4", "arrival": 3, "burst": 5, "priority": 2},
        ],
        "description": "CPU-intensive processes with varying priorities"
    },
    "🌐 Web Server (I/O Bound)": {
        "processes": [
            {"name": "P1", "arrival": 0, "burst": 2, "priority": 1},
            {"name": "P2", "arrival": 0, "burst": 1, "priority": 2},
            {"name": "P3", "arrival": 0, "burst": 2, "priority": 1},
            {"name": "P4", "arrival": 1, "burst": 1, "priority": 3},
            {"name": "P5", "arrival": 1, "burst": 2, "priority": 2},
        ],
        "description": "Short, frequent processes typical of web requests"
    },
    "📊 Batch Processing": {
        "processes": [
            {"name": "P1", "arrival": 0, "burst": 15, "priority": 1},
            {"name": "P2", "arrival": 0, "burst": 12, "priority": 2},
            {"name": "P3", "arrival": 0, "burst": 18, "priority": 1},
            {"name": "P4", "arrival": 5, "burst": 10, "priority": 3},
        ],
        "description": "Long-running batch jobs with different priorities"
    },
    "⚡ Real-Time System": {
        "processes": [
            {"name": "P1", "arrival": 0, "burst": 3, "priority": 1},
            {"name": "P2", "arrival": 1, "burst": 2, "priority": 1},
            {"name": "P3", "arrival": 2, "burst": 4, "priority": 2},
            {"name": "P4", "arrival": 2, "burst": 1, "priority": 1},
            {"name": "P5", "arrival": 3, "burst": 3, "priority": 2},
        ],
        "description": "Time-critical processes with strict priorities"
    },
    "🔄 Mixed Workload": {
        "processes": [
            {"name": "P1", "arrival": 0, "burst": 10, "priority": 3},
            {"name": "P2", "arrival": 2, "burst": 2, "priority": 1},
            {"name": "P3", "arrival": 4, "burst": 8, "priority": 2},
            {"name": "P4", "arrival": 5, "burst": 3, "priority": 1},
            {"name": "P5", "arrival": 6, "burst": 5, "priority": 2},
        ],
        "description": "Mix of short and long processes with staggered arrivals"
    }
}

def process_inputs():
    st.sidebar.header("⚙️ Configuration")
    
    # Scenario selection
    st.sidebar.markdown("### 📋 Quick Start")
    selected_scenario = st.sidebar.selectbox(
        "Load Scenario",
        list(PREDEFINED_SCENARIOS.keys()),
        help="Choose a predefined scenario or select 'Custom' to enter your own values"
    )
    
    # Get scenario data
    scenario_data = PREDEFINED_SCENARIOS[selected_scenario]
    
    if scenario_data:
        n_default = len(scenario_data["processes"])
        st.sidebar.info(f"**{selected_scenario}**\n\n{scenario_data['description']}")
    else:
        n_default = 3
    
    # Number of processes
    n = st.sidebar.number_input("Number of Processes", 1, 10, n_default)
    
    # Algorithm selection with descriptions - MOVED BEFORE process inputs
    st.sidebar.markdown("### 🔧 Algorithm")
    algo = st.sidebar.selectbox(
        "Select Algorithm",
        ["FCFS", "SJN", "Priority", "Round Robin"],
        help="""
        FCFS: First Come First Serve - Simple queue\n
        SJN: Shortest Job First - Optimal for waiting time\n
        Priority: Priority-based scheduling\n
        Round Robin: Time-sliced for fairness
        """
    )
    
    # Initialize data list
    data = []
    
    # Generate input fields
    for i in range(n):
        st.sidebar.markdown(f"**Process P{i+1}**")
        
        # Get default values from scenario if available
        if scenario_data and i < len(scenario_data["processes"]):
            defaults = scenario_data["processes"][i]
            at_default = defaults["arrival"]
            bt_default = defaults["burst"]
            pr_default = defaults["priority"]
        else:
            at_default = i
            bt_default = 5
            pr_default = 1
        
        # Create columns for compact layout - conditional on algorithm
        if algo == "Priority":
            # Show all 3 columns for Priority algorithm
            col1, col2, col3 = st.sidebar.columns(3)
            
            with col1:
                at = st.number_input("AT", 0, value=at_default, key=f"a{i}", 
                                   help="Arrival Time")
            with col2:
                bt = st.number_input("CC", 1, value=bt_default, key=f"b{i}", 
                                   help="Burst Time")
            with col3:
                pr = st.number_input("P", 1, value=pr_default, key=f"p{i}", 
                                   help="Priority (lower = higher priority)")
        else:
            # Show only 2 columns for FCFS, SJF, Round Robin (no priority input)
            col1, col2 = st.sidebar.columns(2)
            
            with col1:
                at = st.number_input("AT", 0, value=at_default, key=f"a{i}", 
                                   help="Arrival Time")
            with col2:
                bt = st.number_input("CC", 1, value=bt_default, key=f"b{i}", 
                                   help="Burst Time")
            # Assign default priority for non-priority algorithms
            pr = 1
        
        data.append([f"P{i+1}", at, bt, pr])
        st.sidebar.markdown("---")
    
    # Time quantum for Round Robin
    q = None
    if algo == "Round Robin":
        st.sidebar.markdown("### ⏱️ Round Robin Settings")
        q = st.sidebar.number_input(
            "Time Quantum", 
            1, 
            value=2,
            help="Time slice for each process. Lower = more context switches"
        )
        
        # Show warning if quantum seems inappropriate
        burst_times = [d[2] for d in data]
        avg_burst = sum(burst_times) / len(burst_times) if burst_times else 0
        if q > avg_burst * 0.5:
            st.sidebar.warning("⚠️ Quantum may be too high for fair scheduling")
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=["Process", "Arrival", "Burst", "Priority"])
    
    # Show process summary
    with st.sidebar.expander("📊 Process Summary", expanded=False):
        st.dataframe(df, width='stretch')
        st.markdown(f"**Total Burst Time:** {df['Burst'].sum()}")
        st.markdown(f"**Avg Burst Time:** {df['Burst'].mean():.2f}")
    
    return df, algo, q

def get_scenario_characteristics(df: pd.DataFrame) -> dict:
    """Extract process characteristics for algorithm recommendation"""
    return {
        'n_processes': len(df),
        'avg_burst': df['Burst'].mean(),
        'arrival_spread': df['Arrival'].max() - df['Arrival'].min(),
        'priorities': len(df['Priority'].unique()),
        'io_ratio': 'mixed'  # Simplified classification
    }

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
    # Main configuration card
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h3 style="color: #f8fafc; margin-bottom: 15px;">⚙️ Configuration</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Scenario selection and Algorithm in one row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 Quick Start**")
        selected_scenario = st.selectbox(
            "Load Scenario",
            list(PREDEFINED_SCENARIOS.keys()),
            help="Choose a predefined scenario or select 'Custom' to enter your own values",
            label_visibility="collapsed"
        )
        
        # Get scenario data
        scenario_data = PREDEFINED_SCENARIOS[selected_scenario]
        
        if scenario_data:
            n_default = len(scenario_data["processes"])
            st.info(f"**{selected_scenario}**\n\n{scenario_data['description']}")
        else:
            n_default = 3
    
    with col2:
        st.markdown("**🔧 Algorithm**")
        algo = st.selectbox(
            "Select Algorithm",
            ["FCFS", "SJN", "Priority", "Round Robin"],
            help="""
            FCFS: First Come First Serve - Simple queue\n
            SJN: Shortest Job Next - Optimal for waiting time\n
            Priority: Priority-based scheduling\n
            Round Robin: Time-sliced for fairness
            """,
            label_visibility="collapsed"
        )
        
        # Algorithm description
        algo_descriptions = {
            "FCFS": "Simple queue - processes served in arrival order",
            "SJN": "Shortest Job Next - optimal for minimizing waiting time",
            "Priority": "Priority-based - higher priority processes first",
            "Round Robin": "Time-sliced - fair allocation with time quantum"
        }
        st.caption(algo_descriptions[algo])
    
    # Number of processes
    st.markdown("**📊 Number of Processes**")
    n = st.slider("Processes", 1, 10, n_default, label_visibility="collapsed")
    
    # Process inputs in expander
    with st.expander("📝 Process Details", expanded=True):
        # Initialize data list
        data = []
        
        # Create a grid layout for process inputs
        # Header row
        header_cols = st.columns([1, 2, 2, 2] if algo == "Priority" else [1, 2, 2])
        with header_cols[0]:
            st.markdown("**Process**")
        with header_cols[1]:
            st.markdown("**Arrival Time**")
        with header_cols[2]:
            st.markdown("**Burst Time**")
        if algo == "Priority":
            with header_cols[3]:
                st.markdown("**Priority**")
        
        st.markdown("---")
        
        # Generate input fields
        for i in range(n):
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
            
            # Create columns for this process
            input_cols = st.columns([1, 2, 2, 2] if algo == "Priority" else [1, 2, 2])
            
            with input_cols[0]:
                st.markdown(f"<div style='padding-top: 8px;'><b>P{i+1}</b></div>", unsafe_allow_html=True)
            
            with input_cols[1]:
                at = st.number_input("AT", 0, value=at_default, key=f"a{i}", 
                                   help="Arrival Time", label_visibility="collapsed")
            
            with input_cols[2]:
                bt = st.number_input("BT", 1, value=bt_default, key=f"b{i}", 
                                   help="Burst Time", label_visibility="collapsed")
            
            if algo == "Priority":
                with input_cols[3]:
                    pr = st.number_input("P", 1, value=pr_default, key=f"p{i}", 
                                       help="Priority (lower = higher priority)", label_visibility="collapsed")
            else:
                pr = 1
            
            data.append([f"P{i+1}", at, bt, pr])
    
    # Time quantum for Round Robin
    q = None
    if algo == "Round Robin":
        with st.expander("⏱️ Round Robin Settings", expanded=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                q = st.number_input(
                    "Time Quantum", 
                    1, 
                    value=2,
                    help="Time slice for each process. Lower = more context switches"
                )
            
            with col2:
                # Show warning if quantum seems inappropriate
                burst_times = [d[2] for d in data]
                avg_burst = sum(burst_times) / len(burst_times) if burst_times else 0
                if q > avg_burst * 0.5:
                    st.warning("⚠️ Quantum may be too high for fair scheduling")
                else:
                    st.success("✅ Quantum setting looks good")
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=["Process", "Arrival", "Burst", "Priority"])
    
    # Show process summary in a nice card
    with st.expander("📊 Process Summary", expanded=False):
        summary_cols = st.columns([2, 1])
        with summary_cols[0]:
            st.dataframe(df, use_container_width=True, hide_index=True)
        with summary_cols[1]:
            st.metric("Total Burst Time", df['Burst'].sum())
            st.metric("Avg Burst Time", f"{df['Burst'].mean():.2f}")
            st.metric("Total Processes", len(df))
    
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

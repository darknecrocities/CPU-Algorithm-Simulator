# app.py
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="CPU Scheduling Algorithm Simulator",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from ui.layout import setup_layout, render_footer
from ui.inputs import process_inputs, get_scenario_characteristics
from ui.results import show_results, show_comparison_results
from ui.chatbot import render_chatbot_ui, initialize_chatbot
from core.algorithms import fcfs, sjf, priority_scheduling, round_robin
from core.gantt import get_schedule_from_algorithm
from core.metrics import PerformanceMetrics

# Initialize layout and styling
setup_layout()

# Initialize session state
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False
if 'all_results' not in st.session_state:
    st.session_state.all_results = {}

# Initialize chatbot
chatbot = initialize_chatbot()

# Main content area with tabs
main_tabs = st.tabs(["🎮 Simulator", "🔬 Comparison Mode", "🤖 AI Advisor"])

with main_tabs[0]:
    # Simulator Tab
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h2>Configure Your Simulation</h2>
            <p style="color: #94a3b8;">Set up processes and choose an algorithm to visualize CPU scheduling</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get inputs
    process_df, algorithm, quantum = process_inputs()
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        run_clicked = st.button("▶️ Run Simulation", width='stretch', type="primary")
    
    with col2:
        compare_clicked = st.button("🔬 Compare All Algorithms", width='stretch')
    
    with col3:
        if st.session_state.simulation_results is not None:
            st.success("✅ Simulation ready - check other tabs!")
    
    # Run single algorithm
    if run_clicked:
        with st.spinner("Running simulation..."):
            if algorithm == "FCFS":
                results = fcfs(process_df)
            elif algorithm == "SJF":
                results = sjf(process_df)
            elif algorithm == "Priority":
                results = priority_scheduling(process_df)
            else:
                results = round_robin(process_df, quantum)
            
            # Calculate metrics
            schedule = get_schedule_from_algorithm(process_df, algorithm, quantum)
            metrics_calc = PerformanceMetrics()
            metrics = metrics_calc.calculate_all_metrics(process_df, results, schedule)
            
            # Store results
            st.session_state.simulation_results = {
                'df': process_df,
                'results': results,
                'algorithm': algorithm,
                'metrics': metrics,
                'quantum': quantum
            }
            
            # Store for comparison
            st.session_state.all_results[algorithm] = (process_df, results, metrics)
        
        st.success(f"✅ {algorithm} simulation completed!")
        st.balloons()
    
    # Run comparison mode
    if compare_clicked:
        with st.spinner("Running all algorithms for comparison..."):
            algorithms = ["FCFS", "SJF", "Priority", "Round Robin"]
            st.session_state.all_results = {}
            
            progress_bar = st.progress(0)
            
            for idx, algo in enumerate(algorithms):
                q = 2 if algo == "Round Robin" else None
                
                if algo == "FCFS":
                    res = fcfs(process_df)
                elif algo == "SJF":
                    res = sjf(process_df)
                elif algo == "Priority":
                    res = priority_scheduling(process_df)
                else:
                    res = round_robin(process_df, q)
                
                # Calculate metrics
                sched = get_schedule_from_algorithm(process_df, algo, q)
                metrics_calc = PerformanceMetrics()
                met = metrics_calc.calculate_all_metrics(process_df, res, sched)
                
                st.session_state.all_results[algo] = (process_df, res, met)
                progress_bar.progress((idx + 1) / len(algorithms))
            
            st.session_state.comparison_mode = True
        
        st.success("✅ All algorithms compared!")
        st.balloons()
    
    # Display results if available
    if st.session_state.simulation_results is not None and not st.session_state.comparison_mode:
        st.markdown("---")
        show_results(
            st.session_state.simulation_results['df'],
            st.session_state.simulation_results['results'],
            st.session_state.simulation_results['algorithm'],
            st.session_state.simulation_results['quantum']
        )

with main_tabs[1]:
    # Comparison Mode Tab
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h2>🔬 Algorithm Comparison</h2>
            <p style="color: #94a3b8;">Compare performance across all scheduling algorithms</p>
        </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.all_results) > 0:
        show_comparison_results(st.session_state.all_results)
    else:
        st.info("👆 Run 'Compare All Algorithms' in the Simulator tab first!")

with main_tabs[2]:
    # AI Advisor Tab (Chatbot)
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h2>🤖 Gemini AI Scheduling Advisor</h2>
            <p style="color: #94a3b8;">Get expert explanations and recommendations powered by Gemini 1.5</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Prepare current data for context
    current_data = None
    if st.session_state.simulation_results is not None:
        current_data = {
            'algorithm': st.session_state.simulation_results['algorithm'],
            'n_processes': len(st.session_state.simulation_results['df']),
            'avg_waiting': st.session_state.simulation_results['metrics']['basic_metrics']['avg_waiting_time'],
            'avg_turnaround': st.session_state.simulation_results['metrics']['basic_metrics']['avg_turnaround_time'],
            'cpu_utilization': st.session_state.simulation_results['metrics']['cpu_utilization']['percentage']
        }
    
    # Render chatbot UI
    render_chatbot_ui(chatbot, current_data)

# Render footer
render_footer()

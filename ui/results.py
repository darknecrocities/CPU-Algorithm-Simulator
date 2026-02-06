# ui/results.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fpdf import FPDF
import io
from datetime import datetime
from core.gantt import GanttChartGenerator, get_schedule_from_algorithm
from core.metrics import PerformanceMetrics, format_metrics_for_display

class ResultsExporter:
    """Handle export of results to various formats"""
    
    @staticmethod
    def export_to_csv(df, results, metrics, filename="scheduling_results"):
        """Export results to CSV format"""
        # Combine process data with results
        combined = pd.merge(df, results, on="Process")
        
        # Create CSV buffer
        csv_buffer = io.StringIO()
        combined.to_csv(csv_buffer, index=False)
        
        return csv_buffer.getvalue()
    
    @staticmethod
    def export_to_pdf(df, results, metrics, algorithm, filename="scheduling_results"):
        """Export results to PDF format"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        
        # Title
        pdf.cell(0, 10, f"CPU Scheduling Results - {algorithm}", ln=True, align="C")
        pdf.ln(10)
        
        # Process Table
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Process Details:", ln=True)
        pdf.set_font("Arial", "", 10)
        
        combined = pd.merge(df, results, on="Process")
        for _, row in combined.iterrows():
            pdf.cell(0, 8, f"{row['Process']}: Arrival={row['Arrival']}, "
                          f"Burst={row['Burst']}, Priority={row['Priority']}, "
                          f"WT={row['Waiting Time']}, TAT={row['Turnaround Time']}", ln=True)
        
        pdf.ln(10)
        
        # Metrics
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Performance Metrics:", ln=True)
        pdf.set_font("Arial", "", 10)
        
        if 'basic_metrics' in metrics:
            pdf.cell(0, 8, f"Average Waiting Time: {metrics['basic_metrics']['avg_waiting_time']}", ln=True)
            pdf.cell(0, 8, f"Average Turnaround Time: {metrics['basic_metrics']['avg_turnaround_time']}", ln=True)
        
        if 'cpu_utilization' in metrics:
            pdf.cell(0, 8, f"CPU Utilization: {metrics['cpu_utilization']['percentage']}%", ln=True)
        
        if 'throughput' in metrics:
            pdf.cell(0, 8, f"Throughput: {metrics['throughput']['processes_per_unit']} processes/unit", ln=True)
        
        # Save to buffer
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        
        return pdf_buffer.getvalue()

def show_results(df, results, algorithm, quantum=None):
    """Display comprehensive results with all features"""
    
    # Initialize generators
    gantt_gen = GanttChartGenerator()
    metrics_calc = PerformanceMetrics()
    
    # Get execution schedule
    schedule = get_schedule_from_algorithm(df, algorithm, quantum)
    
    # Calculate comprehensive metrics
    metrics = metrics_calc.calculate_all_metrics(df, results, schedule)
    formatted_metrics = format_metrics_for_display(metrics)
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "📈 Gantt Chart", 
        "🎯 Metrics Dashboard", 
        "🔍 Detailed Analysis",
        "💾 Export"
    ])
    
    with tab1:
        show_overview_tab(df, results, algorithm, metrics)
    
    with tab2:
        show_gantt_tab(gantt_gen, schedule, algorithm)
    
    with tab3:
        show_metrics_dashboard(metrics, formatted_metrics)
    
    with tab4:
        show_detailed_analysis(df, results, metrics, metrics_calc)
    
    with tab5:
        show_export_tab(df, results, metrics, algorithm)

def show_overview_tab(df, results, algorithm, metrics):
    """Show overview tab with basic results"""
    st.subheader("📋 Process Execution Results")
    
    # Results table
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**Process Details & Results**")
        display_df = pd.merge(df, results, on="Process")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**Quick Stats**")
        
        # Metric cards
        avg_wt = results['Waiting Time'].mean()
        avg_tat = results['Turnaround Time'].mean()
        
        st.metric("Avg Waiting Time", f"{avg_wt:.2f}", 
                delta=f"{avg_wt - df['Burst'].mean():.2f} vs burst")
        st.metric("Avg Turnaround Time", f"{avg_tat:.2f}")
        
        if 'cpu_utilization' in metrics:
            st.metric("CPU Utilization", f"{metrics['cpu_utilization']['percentage']}%")
    
    # Basic bar chart
    st.markdown("**Waiting Time Comparison**")
    fig = px.bar(results, x='Process', y='Waiting Time',
                 color='Process',
                 color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(
        plot_bgcolor='#1e293b',
        paper_bgcolor='#0f172a',
        font_color='#f8fafc',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

def show_gantt_tab(gantt_gen, schedule, algorithm):
    """Show Gantt chart visualization"""
    st.subheader("📈 Execution Timeline")
    
    # Chart type selection
    chart_type = st.radio(
        "Chart Type",
        ["Standard Gantt", "Animated Timeline"],
        horizontal=True
    )
    
    if chart_type == "Standard Gantt":
        fig = gantt_gen.create_gantt_chart(schedule, f"{algorithm} - Process Execution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = gantt_gen.create_animated_gantt(schedule)
        st.plotly_chart(fig, use_container_width=True)
    
    # Show schedule table
    with st.expander("View Schedule Details"):
        schedule_df = pd.DataFrame(schedule, columns=['Process', 'Start', 'End'])
        schedule_df['Duration'] = schedule_df['End'] - schedule_df['Start']
        st.dataframe(schedule_df, use_container_width=True, hide_index=True)

def show_metrics_dashboard(metrics, formatted_metrics):
    """Show comprehensive metrics dashboard"""
    st.subheader("🎯 Performance Metrics Dashboard")
    
    # Key metrics in grid
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Avg Waiting Time</div>
            </div>
        """.format(formatted_metrics['Basic Metrics']['Average Waiting Time']), 
        unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Avg Turnaround Time</div>
            </div>
        """.format(formatted_metrics['Basic Metrics']['Average Turnaround Time']), 
        unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">CPU Utilization</div>
            </div>
        """.format(formatted_metrics['CPU Utilization']['Percentage']), 
        unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Throughput</div>
            </div>
        """.format(formatted_metrics['Throughput']['Processes per Unit Time']), 
        unsafe_allow_html=True)
    
    # Detailed metrics expanders
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("⏱️ Time Metrics", expanded=True):
            for key, value in formatted_metrics['Basic Metrics'].items():
                st.markdown(f"**{key}:** {value}")
        
        with st.expander("🚀 Throughput & Efficiency"):
            for key, value in formatted_metrics['Throughput'].items():
                st.markdown(f"**{key}:** {value}")
    
    with col2:
        with st.expander("⚡ Response Time", expanded=True):
            for key, value in formatted_metrics['Response Time'].items():
                st.markdown(f"**{key}:** {value}")
        
        with st.expander("⚖️ Fairness Metrics"):
            for key, value in formatted_metrics['Fairness'].items():
                st.markdown(f"**{key}:** {value}")

def show_detailed_analysis(df, results, metrics, metrics_calc):
    """Show detailed analysis with insights"""
    st.subheader("🔍 Detailed Performance Analysis")
    
    # Generate insights
    insights = metrics_calc.generate_insights(metrics)
    
    st.markdown("### 💡 Key Insights")
    for insight in insights:
        st.markdown(f"- {insight}")
    
    # Interactive charts
    st.markdown("### 📊 Visual Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for time distribution
        fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
        fig.add_trace(go.Pie(
            labels=results['Process'],
            values=results['Waiting Time'],
            name="Waiting Time",
            hole=.4,
            marker_colors=px.colors.qualitative.Bold
        ))
        fig.update_layout(
            title="Waiting Time Distribution",
            plot_bgcolor='#1e293b',
            paper_bgcolor='#0f172a',
            font_color='#f8fafc'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Line chart for turnaround times
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=results['Process'],
            y=results['Turnaround Time'],
            mode='lines+markers',
            name='Turnaround Time',
            line=dict(color='#6366f1', width=3),
            marker=dict(size=10)
        ))
        fig.add_trace(go.Scatter(
            x=results['Process'],
            y=results['Waiting Time'],
            mode='lines+markers',
            name='Waiting Time',
            line=dict(color='#ec4899', width=3),
            marker=dict(size=10)
        ))
        fig.update_layout(
            title="Time Metrics Comparison",
            xaxis_title="Process",
            yaxis_title="Time Units",
            plot_bgcolor='#1e293b',
            paper_bgcolor='#0f172a',
            font_color='#f8fafc',
            legend=dict(
                bgcolor='#1e293b',
                bordercolor='#6366f1',
                borderwidth=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Process queue visualization
    st.markdown("### 🔄 Process Queue Visualization")
    show_queue_visualization(df, results)

def show_queue_visualization(df, results):
    """Visualize process queue states"""
    st.markdown("""
        <div class="queue-container">
            <h4>Ready Queue State</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
    """, unsafe_allow_html=True)
    
    # Create visual queue items
    for _, row in df.iterrows():
        wt = results[results['Process'] == row['Process']]['Waiting Time'].values[0]
        color_class = "status-completed" if wt < df['Burst'].mean() else "status-waiting"
        
        st.markdown(f"""
            <div class="queue-item {color_class}" style="display: inline-flex; 
                 align-items: center; justify-content: center; width: 60px; height: 60px;
                 background: linear-gradient(135deg, #6366f1, #4f46e5);
                 color: white; border-radius: 50%; margin: 5px; font-weight: bold;">
                {row['Process']}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Legend
    st.markdown("""
        <div style="display: flex; gap: 20px; justify-content: center; margin-top: 10px;">
            <span><span style="color: #10b981;">●</span> Good (WT < avg)</span>
            <span><span style="color: #f59e0b;">●</span> Moderate (WT ≥ avg)</span>
        </div>
    """, unsafe_allow_html=True)

def show_export_tab(df, results, metrics, algorithm):
    """Show export options"""
    st.subheader("💾 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Export as CSV")
        exporter = ResultsExporter()
        csv_data = exporter.export_to_csv(df, results, metrics)
        
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name=f"scheduling_results_{algorithm}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.markdown("### 📑 Export as PDF")
        pdf_data = exporter.export_to_pdf(df, results, metrics, algorithm)
        
        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_data,
            file_name=f"scheduling_results_{algorithm}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    # Preview
    with st.expander("Preview Data"):
        combined = pd.merge(df, results, on="Process")
        st.dataframe(combined, use_container_width=True)

def show_comparison_results(all_results):
    """Show comparison of multiple algorithms"""
    st.subheader("🔬 Algorithm Comparison")
    
    # Create comparison dataframe
    comparison_data = []
    for algo_name, (df, results, metrics) in all_results.items():
        comparison_data.append({
            'Algorithm': algo_name,
            'Avg Waiting Time': metrics['basic_metrics']['avg_waiting_time'],
            'Avg Turnaround Time': metrics['basic_metrics']['avg_turnaround_time'],
            'CPU Utilization %': metrics['cpu_utilization']['percentage'],
            'Throughput': metrics['throughput']['processes_per_unit'],
            'Avg Response Time': metrics['response_time']['avg_response_time'],
            'Fairness Index': metrics['fairness']['fairness_index']
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Display comparison table
    st.markdown("### 📊 Comparison Table")
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    # Highlight best algorithm
    best_algo = comparison_df.loc[comparison_df['Avg Waiting Time'].idxmin(), 'Algorithm']
    st.success(f"🏆 Best Algorithm (by Waiting Time): **{best_algo}**")
    
    # Comparison charts
    st.markdown("### 📈 Visual Comparison")
    
    # Bar chart comparison
    fig = go.Figure()
    metrics_to_plot = ['Avg Waiting Time', 'Avg Turnaround Time', 'Avg Response Time']
    
    for metric in metrics_to_plot:
        fig.add_trace(go.Bar(
            name=metric,
            x=comparison_df['Algorithm'],
            y=comparison_df[metric],
            text=comparison_df[metric].round(2),
            textposition='auto',
        ))
    
    fig.update_layout(
        title="Algorithm Performance Comparison",
        barmode='group',
        plot_bgcolor='#1e293b',
        paper_bgcolor='#0f172a',
        font_color='#f8fafc',
        legend=dict(
            bgcolor='#1e293b',
            bordercolor='#6366f1',
            borderwidth=1
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Gantt comparison
    st.markdown("### 📅 Execution Timeline Comparison")
    gantt_gen = GanttChartGenerator()
    
    schedules = {}
    for algo_name, (df, results, metrics) in all_results.items():
        # Determine quantum if Round Robin
        quantum = 2 if algo_name == "Round Robin" else None
        schedule = get_schedule_from_algorithm(df, algo_name, quantum)
        schedules[algo_name] = schedule
    
    fig = gantt_gen.create_comparison_gantt(schedules)
    st.plotly_chart(fig, use_container_width=True)

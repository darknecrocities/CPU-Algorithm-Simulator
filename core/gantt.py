# core/gantt.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Tuple

class GanttChartGenerator:
    """Generate Gantt charts for CPU scheduling algorithms"""
    
    def __init__(self):
        self.colors = {
            'P1': '#6366f1', 'P2': '#ec4899', 'P3': '#06b6d4',
            'P4': '#10b981', 'P5': '#f59e0b', 'P6': '#ef4444',
            'P7': '#8b5cf6', 'P8': '#14b8a6', 'P9': '#f97316',
            'P10': '#84cc16', 'IDLE': '#334155'
        }
    
    def generate_timeline_data(self, schedule: List[Tuple[str, int, int]]) -> pd.DataFrame:
        """
        Convert schedule to timeline data for Gantt chart
        
        Args:
            schedule: List of (process_name, start_time, end_time) tuples
        
        Returns:
            DataFrame with timeline data
        """
        data = []
        for process, start, end in schedule:
            duration = end - start
            data.append({
                'Process': process,
                'Start': start,
                'Finish': end,
                'Duration': duration,
                'Color': self.colors.get(process, '#6366f1')
            })
        return pd.DataFrame(data)
    
    def create_gantt_chart(self, schedule: List[Tuple[str, int, int]], 
                          title: str = "Process Execution Timeline") -> go.Figure:
        """
        Create an interactive Gantt chart using Plotly
        
        Args:
            schedule: List of (process_name, start_time, end_time) tuples
            title: Chart title
        
        Returns:
            Plotly Figure object
        """
        df = self.generate_timeline_data(schedule)
        
        fig = go.Figure()
        
        for _, row in df.iterrows():
            fig.add_trace(go.Bar(
                name=row['Process'],
                x=[row['Duration']],
                y=[row['Process']],
                orientation='h',
                base=row['Start'],
                marker_color=row['Color'],
                text=f"{row['Start']} → {row['Finish']}",
                textposition='inside',
                hovertemplate=(
                    f"<b>{row['Process']}</b><br>"
                    f"Start: {row['Start']}<br>"
                    f"End: {row['Finish']}<br>"
                    f"Duration: {row['Duration']}<br>"
                    "<extra></extra>"
                )
            ))
        
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#f8fafc'}
            },
            xaxis_title="Time Units",
            yaxis_title="Processes",
            barmode='stack',
            plot_bgcolor='#1e293b',
            paper_bgcolor='#0f172a',
            font_color='#f8fafc',
            xaxis=dict(
                gridcolor='#334155',
                zerolinecolor='#334155',
                tickfont={'color': '#94a3b8'}
            ),
            yaxis=dict(
                gridcolor='#334155',
                zerolinecolor='#334155',
                tickfont={'color': '#94a3b8'}
            ),
            showlegend=False,
            height=400,
            margin=dict(l=100, r=50, t=80, b=50)
        )
        
        return fig
    
    def create_comparison_gantt(self, schedules: Dict[str, List[Tuple[str, int, int]]]) -> go.Figure:
        """
        Create a comparison Gantt chart for multiple algorithms
        
        Args:
            schedules: Dict of {algorithm_name: schedule_list}
        
        Returns:
            Plotly Figure object
        """
        fig = go.Figure()
        
        y_offset = 0
        algorithm_names = list(schedules.keys())
        
        for algo_name, schedule in schedules.items():
            df = self.generate_timeline_data(schedule)
            
            for _, row in df.iterrows():
                fig.add_trace(go.Bar(
                    name=f"{algo_name} - {row['Process']}",
                    x=[row['Duration']],
                    y=[y_offset],
                    orientation='h',
                    base=row['Start'],
                    marker_color=row['Color'],
                    text=f"{row['Process']}",
                    textposition='inside',
                    showlegend=False,
                    hovertemplate=(
                        f"<b>{algo_name}</b><br>"
                        f"Process: {row['Process']}<br>"
                        f"Start: {row['Start']}<br>"
                        f"End: {row['Finish']}<br>"
                        f"Duration: {row['Duration']}<br>"
                        "<extra></extra>"
                    )
                ))
            
            y_offset += 1
        
        fig.update_layout(
            title={
                'text': "Algorithm Comparison - Execution Timelines",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#f8fafc'}
            },
            xaxis_title="Time Units",
            yaxis=dict(
                tickmode='array',
                tickvals=list(range(len(algorithm_names))),
                ticktext=algorithm_names,
                gridcolor='#334155',
                zerolinecolor='#334155',
                tickfont={'color': '#94a3b8'}
            ),
            xaxis=dict(
                gridcolor='#334155',
                zerolinecolor='#334155',
                tickfont={'color': '#94a3b8'}
            ),
            plot_bgcolor='#1e293b',
            paper_bgcolor='#0f172a',
            font_color='#f8fafc',
            barmode='group',
            height=100 + (len(algorithm_names) * 80),
            margin=dict(l=150, r=50, t=80, b=50)
        )
        
        return fig
    
    def create_animated_gantt(self, schedule: List[Tuple[str, int, int]], 
                             speed: int = 1000) -> go.Figure:
        """
        Create an animated Gantt chart showing execution step by step
        
        Args:
            schedule: List of (process_name, start_time, end_time) tuples
            speed: Animation speed in milliseconds
        
        Returns:
            Plotly Figure object with animation
        """
        df = self.generate_timeline_data(schedule)
        
        frames = []
        max_time = df['Finish'].max()
        
        for t in range(int(max_time) + 1):
            frame_data = []
            for _, row in df.iterrows():
                if row['Start'] <= t:
                    visible_duration = min(t - row['Start'], row['Duration'])
                    if visible_duration > 0:
                        frame_data.append({
                            'Process': row['Process'],
                            'Start': row['Start'],
                            'Duration': visible_duration,
                            'Color': row['Color']
                        })
            
            frames.append(go.Frame(
                data=[go.Bar(
                    x=[d['Duration'] for d in frame_data],
                    y=[d['Process'] for d in frame_data],
                    orientation='h',
                    base=[d['Start'] for d in frame_data],
                    marker_color=[d['Color'] for d in frame_data],
                    text=[f"{d['Start']} → {d['Start'] + d['Duration']}" for d in frame_data],
                    textposition='inside'
                )],
                name=str(t)
            ))
        
        fig = go.Figure(
            data=[go.Bar(
                x=[0],
                y=[df['Process'].iloc[0]],
                orientation='h',
                marker_color=self.colors.get(df['Process'].iloc[0], '#6366f1')
            )],
            frames=frames
        )
        
        fig.update_layout(
            title={
                'text': "Animated Process Execution",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#f8fafc'}
            },
            xaxis_title="Time Units",
            yaxis_title="Processes",
            plot_bgcolor='#1e293b',
            paper_bgcolor='#0f172a',
            font_color='#f8fafc',
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {
                        'label': '▶️ Play',
                        'method': 'animate',
                        'args': [None, {
                            'frame': {'duration': speed, 'redraw': True},
                            'fromcurrent': True,
                            'transition': {'duration': 0}
                        }]
                    },
                    {
                        'label': '⏸️ Pause',
                        'method': 'animate',
                        'args': [[None], {
                            'frame': {'duration': 0, 'redraw': False},
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }]
                    }
                ],
                'x': 0.1,
                'y': 0,
                'bgcolor': '#1e293b',
                'bordercolor': '#6366f1',
                'font': {'color': '#f8fafc'}
            }],
            sliders=[{
                'active': 0,
                'yanchor': 'top',
                'xanchor': 'left',
                'currentvalue': {
                    'font': {'size': 16, 'color': '#f8fafc'},
                    'prefix': 'Time: ',
                    'visible': True,
                    'xanchor': 'right'
                },
                'transition': {'duration': speed, 'easing': 'cubic-in-out'},
                'pad': {'b': 10, 't': 50},
                'len': 0.9,
                'x': 0.1,
                'y': 0,
                'steps': [
                    {
                        'args': [[str(t)], {
                            'frame': {'duration': speed, 'redraw': True},
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }],
                        'label': str(t),
                        'method': 'animate'
                    } for t in range(int(max_time) + 1)
                ],
                'bgcolor': '#1e293b',
                'bordercolor': '#6366f1',
                'font': {'color': '#f8fafc'}
            }],
            height=400,
            margin=dict(l=100, r=50, t=80, b=100)
        )
        
        return fig


def get_schedule_from_algorithm(df, algorithm, quantum=None):
    """
    Generate execution schedule from algorithm results
    
    Args:
        df: Process DataFrame
        algorithm: Algorithm name
        quantum: Time quantum for Round Robin
    
    Returns:
        List of (process_name, start_time, end_time) tuples
    """
    schedule = []
    time = 0
    
    if algorithm == "FCFS":
        for _, p in df.sort_values("Arrival").iterrows():
            time = max(time, p.Arrival)
            start = time
            time += p.Burst
            schedule.append((p.Process, start, time))
    
    elif algorithm == "SJF":
        done = []
        while len(done) < len(df):
            ready = df[(df.Arrival <= time) & (~df.Process.isin(done))]
            if ready.empty:
                time += 1
                continue
            p = ready.sort_values("Burst").iloc[0]
            start = time
            time += p.Burst
            done.append(p.Process)
            schedule.append((p.Process, start, time))
    
    elif algorithm == "Priority":
        done = []
        while len(done) < len(df):
            ready = df[(df.Arrival <= time) & (~df.Process.isin(done))]
            if ready.empty:
                time += 1
                continue
            p = ready.sort_values("Priority").iloc[0]
            start = time
            time += p.Burst
            done.append(p.Process)
            schedule.append((p.Process, start, time))
    
    elif algorithm == "Round Robin":
        remaining = dict(zip(df.Process, df.Burst))
        arrived = set()
        queue = []
        
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
            exec_time = min(quantum, remaining[cur])
            start = time
            time += exec_time
            remaining[cur] -= exec_time
            
            # Add newly arrived during execution
            for p in df.Process:
                if df[df.Process == p].Arrival.values[0] <= time and p not in arrived:
                    queue.append(p)
                    arrived.add(p)
            
            schedule.append((cur, start, time))
            
            if remaining[cur] > 0:
                queue.append(cur)
            else:
                del remaining[cur]
    
    return schedule

# core/metrics.py
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class PerformanceMetrics:
    """Calculate comprehensive performance metrics for CPU scheduling algorithms"""
    
    def __init__(self):
        self.metrics_history = []
    
    def calculate_all_metrics(self, df: pd.DataFrame, results: pd.DataFrame, 
                             schedule: List[Tuple[str, int, int]]) -> Dict:
        """
        Calculate all performance metrics
        
        Args:
            df: Original process DataFrame
            results: Results DataFrame with Waiting Time and Turnaround Time
            schedule: Execution schedule
        
        Returns:
            Dictionary with all calculated metrics
        """
        metrics = {
            'basic_metrics': self._calculate_basic_metrics(results),
            'cpu_utilization': self._calculate_cpu_utilization(df, schedule),
            'throughput': self._calculate_throughput(df, schedule),
            'response_time': self._calculate_response_time(df, schedule),
            'fairness': self._calculate_fairness(results),
            'efficiency': self._calculate_efficiency(results, schedule)
        }
        
        return metrics
    
    def _calculate_basic_metrics(self, results: pd.DataFrame) -> Dict:
        """Calculate basic metrics (avg waiting time, turnaround time)"""
        return {
            'avg_waiting_time': round(results['Waiting Time'].mean(), 2),
            'avg_turnaround_time': round(results['Turnaround Time'].mean(), 2),
            'total_waiting_time': int(results['Waiting Time'].sum()),
            'total_turnaround_time': int(results['Turnaround Time'].sum()),
            'max_waiting_time': int(results['Waiting Time'].max()),
            'min_waiting_time': int(results['Waiting Time'].min()),
            'max_turnaround_time': int(results['Turnaround Time'].max()),
            'min_turnaround_time': int(results['Turnaround Time'].min())
        }
    
    def _calculate_cpu_utilization(self, df: pd.DataFrame, 
                                   schedule: List[Tuple[str, int, int]]) -> Dict:
        """Calculate CPU utilization metrics"""
        if not schedule:
            return {'percentage': 0, 'idle_time': 0, 'busy_time': 0, 'total_time': 0}
        
        total_time = schedule[-1][2]  # End time of last process
        busy_time = sum(end - start for _, start, end in schedule)
        idle_time = total_time - busy_time
        
        return {
            'percentage': round((busy_time / total_time) * 100, 2) if total_time > 0 else 0,
            'busy_time': busy_time,
            'idle_time': idle_time,
            'total_time': total_time
        }
    
    def _calculate_throughput(self, df: pd.DataFrame, 
                            schedule: List[Tuple[str, int, int]]) -> Dict:
        """Calculate throughput metrics"""
        if not schedule:
            return {'processes_per_unit': 0, 'total_processes': 0, 'total_time': 0}
        
        total_time = schedule[-1][2]
        n_processes = len(df)
        
        return {
            'processes_per_unit': round(n_processes / total_time, 4) if total_time > 0 else 0,
            'total_processes': n_processes,
            'total_time': total_time
        }
    
    def _calculate_response_time(self, df: pd.DataFrame, 
                                 schedule: List[Tuple[str, int, int]]) -> Dict:
        """Calculate response time for each process"""
        response_times = {}
        
        for process in df.Process:
            arrival = df[df.Process == process].Arrival.values[0]
            # Find first execution time
            for p, start, end in schedule:
                if p == process:
                    response_times[process] = start - arrival
                    break
        
        if response_times:
            values = list(response_times.values())
            return {
                'per_process': response_times,
                'avg_response_time': round(np.mean(values), 2),
                'max_response_time': max(values),
                'min_response_time': min(values)
            }
        return {'per_process': {}, 'avg_response_time': 0, 'max_response_time': 0, 'min_response_time': 0}
    
    def _calculate_fairness(self, results: pd.DataFrame) -> Dict:
        """Calculate fairness metrics (variance in waiting times)"""
        waiting_times = results['Waiting Time'].values
        turnaround_times = results['Turnaround Time'].values
        
        return {
            'waiting_time_variance': round(np.var(waiting_times), 2),
            'turnaround_time_variance': round(np.var(turnaround_times), 2),
            'waiting_time_std': round(np.std(waiting_times), 2),
            'turnaround_time_std': round(np.std(turnaround_times), 2),
            'fairness_index': round(1 / (1 + np.var(waiting_times)), 4)  # Higher is fairer
        }
    
    def _calculate_efficiency(self, results: pd.DataFrame, 
                             schedule: List[Tuple[str, int, int]]) -> Dict:
        """Calculate efficiency metrics"""
        total_burst = results['Turnaround Time'].sum() - results['Waiting Time'].sum()
        total_time = schedule[-1][2] if schedule else 1
        
        return {
            'efficiency_ratio': round(total_burst / total_time, 4) if total_time > 0 else 0,
            'normalized_avg_turnaround': round(results['Turnaround Time'].mean() / total_burst, 4) if total_burst > 0 else 0
        }
    
    def compare_algorithms(self, algorithms_results: Dict[str, Dict]) -> pd.DataFrame:
        """
        Create comparison table for multiple algorithms
        
        Args:
            algorithms_results: Dict of {algorithm_name: metrics_dict}
        
        Returns:
            DataFrame with comparison data
        """
        comparison_data = []
        
        for algo_name, metrics in algorithms_results.items():
            row = {
                'Algorithm': algo_name,
                'Avg Waiting Time': metrics['basic_metrics']['avg_waiting_time'],
                'Avg Turnaround Time': metrics['basic_metrics']['avg_turnaround_time'],
                'CPU Utilization (%)': metrics['cpu_utilization']['percentage'],
                'Throughput': metrics['throughput']['processes_per_unit'],
                'Avg Response Time': metrics['response_time']['avg_response_time'],
                'Fairness Index': metrics['fairness']['fairness_index']
            }
            comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)
    
    def get_best_algorithm(self, comparison_df: pd.DataFrame, 
                          priority: str = 'balanced') -> str:
        """
        Determine the best algorithm based on metrics
        
        Args:
            comparison_df: DataFrame with algorithm comparisons
            priority: 'waiting_time', 'turnaround_time', 'throughput', 'balanced'
        
        Returns:
            Name of best algorithm
        """
        if comparison_df.empty:
            return "N/A"
        
        if priority == 'waiting_time':
            best = comparison_df.loc[comparison_df['Avg Waiting Time'].idxmin()]
        elif priority == 'turnaround_time':
            best = comparison_df.loc[comparison_df['Avg Turnaround Time'].idxmin()]
        elif priority == 'throughput':
            best = comparison_df.loc[comparison_df['Throughput'].idxmax()]
        else:  # balanced
            # Normalize metrics (lower is better for time metrics, higher for throughput)
            df_norm = comparison_df.copy()
            for col in ['Avg Waiting Time', 'Avg Turnaround Time', 'Avg Response Time']:
                df_norm[col] = 1 - (df_norm[col] - df_norm[col].min()) / (df_norm[col].max() - df_norm[col].min() + 0.001)
            
            df_norm['Throughput'] = (df_norm['Throughput'] - df_norm['Throughput'].min()) / (df_norm['Throughput'].max() - df_norm['Throughput'].min() + 0.001)
            df_norm['CPU Utilization (%)'] = df_norm['CPU Utilization (%)'] / 100
            
            # Calculate composite score
            df_norm['Score'] = (df_norm['Avg Waiting Time'] + 
                               df_norm['Avg Turnaround Time'] + 
                               df_norm['Throughput'] + 
                               df_norm['CPU Utilization (%)']) / 4
            
            best_idx = df_norm['Score'].idxmax()
            best = comparison_df.loc[best_idx]
        
        return best['Algorithm']
    
    def generate_insights(self, metrics: Dict) -> List[str]:
        """Generate insights based on metrics"""
        insights = []
        
        # CPU Utilization insight
        cpu_util = metrics['cpu_utilization']['percentage']
        if cpu_util > 90:
            insights.append(f"✅ Excellent CPU utilization at {cpu_util}%")
        elif cpu_util > 70:
            insights.append(f"⚠️ Good CPU utilization at {cpu_util}%, but could be improved")
        else:
            insights.append(f"❌ Low CPU utilization at {cpu_util}%. Consider optimizing process arrival times.")
        
        # Throughput insight
        throughput = metrics['throughput']['processes_per_unit']
        insights.append(f"📊 Throughput: {throughput} processes per time unit")
        
        # Fairness insight
        fairness = metrics['fairness']['fairness_index']
        if fairness > 0.8:
            insights.append(f"✅ High fairness index ({fairness}): Waiting times are well-balanced")
        elif fairness > 0.5:
            insights.append(f"⚠️ Moderate fairness ({fairness}): Some processes wait significantly longer")
        else:
            insights.append(f"❌ Low fairness ({fairness}): Consider a different algorithm for better balance")
        
        # Response time insight
        avg_response = metrics['response_time']['avg_response_time']
        insights.append(f"⏱️ Average response time: {avg_response} time units")
        
        return insights


def format_metrics_for_display(metrics: Dict) -> Dict:
    """Format metrics for nice display in UI"""
    formatted = {
        'Basic Metrics': {
            'Average Waiting Time': f"{metrics['basic_metrics']['avg_waiting_time']} units",
            'Average Turnaround Time': f"{metrics['basic_metrics']['avg_turnaround_time']} units",
            'Max Waiting Time': f"{metrics['basic_metrics']['max_waiting_time']} units",
            'Min Waiting Time': f"{metrics['basic_metrics']['min_waiting_time']} units"
        },
        'CPU Utilization': {
            'Percentage': f"{metrics['cpu_utilization']['percentage']}%",
            'Busy Time': f"{metrics['cpu_utilization']['busy_time']} units",
            'Idle Time': f"{metrics['cpu_utilization']['idle_time']} units"
        },
        'Throughput': {
            'Processes per Unit Time': f"{metrics['throughput']['processes_per_unit']}",
            'Total Processes': metrics['throughput']['total_processes'],
            'Total Time': f"{metrics['throughput']['total_time']} units"
        },
        'Response Time': {
            'Average': f"{metrics['response_time']['avg_response_time']} units",
            'Max': f"{metrics['response_time']['max_response_time']} units",
            'Min': f"{metrics['response_time']['min_response_time']} units"
        },
        'Fairness': {
            'Fairness Index': f"{metrics['fairness']['fairness_index']}",
            'Waiting Time Variance': f"{metrics['fairness']['waiting_time_variance']}",
            'Interpretation': 'Higher index = more fair' if metrics['fairness']['fairness_index'] > 0.5 else 'Lower index = less fair'
        }
    }
    
    return formatted

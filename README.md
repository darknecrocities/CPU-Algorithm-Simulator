# 🖥️ CPU Scheduling Algorithm Simulator

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini_1.5-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)

An interactive, modern CPU Scheduling Algorithm Simulator built with Streamlit, featuring real-time visualizations, comprehensive performance metrics, and AI-powered explanations using Google's Gemini 1.5.

![CPU Scheduling Simulator](assets/screenshot.png)

## ✨ Features

### 🎯 Core Features
1. **📊 Gantt Chart Visualization** - Interactive timeline showing process execution with color-coded blocks
2. **🔬 Algorithm Comparison Mode** - Run and compare all algorithms simultaneously with side-by-side analysis
3. **💾 Export Results (CSV/PDF)** - Download simulation results in multiple formats for reporting
4. **🎬 Step-by-Step Animation** - Animated execution timeline with play/pause controls
5. **📋 Predefined Scenarios** - Quick-start templates (Gaming, Web Server, Batch Processing, Real-Time, Mixed)
6. **📈 Real-Time Metrics Dashboard** - Live CPU utilization, throughput, and performance indicators
7. **🔄 Process Queue Visualization** - Visual representation of ready queue states
8. **📊 Interactive Charts** - Pie charts, line graphs, and bar charts for data analysis
9. **🤖 Gemini AI Chatbot** - AI-powered advisor for algorithm explanations and recommendations
10. **🎚️ Performance Analysis Metrics** - Comprehensive metrics including fairness index, response time, and efficiency

### 🎨 Design Features
- **Modern Dark Theme** with gradient accents and smooth animations
- **Responsive Layout** optimized for all screen sizes
- **Custom CSS Styling** with hover effects and transitions
- **Theme Toggle** (Dark/Light mode support)
- **Professional UI** with metric cards and data visualizations

## 🚀 Supported Algorithms

| Algorithm | Description | Best For |
|-----------|-------------|----------|
| **FCFS** | First Come First Serve | Simple queue-based systems |
| **SJF** | Shortest Job First | Minimizing waiting time |
| **Priority** | Priority-based scheduling | Critical process handling |
| **Round Robin** | Time-sliced scheduling | Fair CPU time distribution |

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/cpu-scheduling-simulator.git
cd cpu-scheduling-simulator
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
```
streamlit>=1.28.0
pandas>=2.0.0
matplotlib>=3.7.0
plotly>=5.15.0
google-generativeai>=0.3.0
fpdf2>=2.7.0
numpy>=1.24.0
Pillow>=10.0.0
```

## 🎮 Usage

### Running the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Quick Start Guide

1. **Choose a Scenario** (Optional)
   - Select from predefined scenarios in the sidebar
   - Or choose "Custom" to enter your own process data

2. **Configure Processes**
   - Set number of processes (1-10)
   - Enter Arrival Time (AT), Burst Time (BT), and Priority for each process
   - View process summary in the sidebar

3. **Select Algorithm**
   - Choose from FCFS, SJF, Priority, or Round Robin
   - For Round Robin, set the time quantum

4. **Run Simulation**
   - Click "▶️ Run Simulation" for single algorithm
   - Click "🔬 Compare All Algorithms" to compare all four

5. **Explore Results**
   - **Overview Tab**: Basic results and statistics
   - **Gantt Chart Tab**: Visual execution timeline
   - **Metrics Dashboard**: Comprehensive performance metrics
   - **Detailed Analysis**: Insights and interactive charts
   - **Export Tab**: Download results as CSV or PDF

6. **Use AI Advisor**
   - Switch to "🤖 AI Advisor" tab
   - Ask questions about algorithms
   - Get performance analysis and recommendations
   - Use quick action buttons for instant explanations

## 📊 Metrics Explained

### Basic Metrics
- **Waiting Time**: Time spent waiting in ready queue
- **Turnaround Time**: Total time from arrival to completion
- **Response Time**: Time from arrival to first execution

### Advanced Metrics
- **CPU Utilization**: Percentage of time CPU is busy
- **Throughput**: Processes completed per unit time
- **Fairness Index**: Measure of waiting time distribution (1.0 = perfectly fair)
- **Efficiency Ratio**: Ratio of useful work to total time

## 🤖 Gemini AI Integration

The simulator includes a built-in AI advisor powered by Google's Gemini 1.5 that can:

- **Explain Algorithms**: Detailed explanations of FCFS, SJF, Priority, and Round Robin
- **Analyze Results**: Interpret your simulation metrics and provide insights
- **Give Recommendations**: Suggest the best algorithm for your workload
- **Answer Questions**: General OS and scheduling questions

### Using the Chatbot
1. Run a simulation first (provides context)
2. Go to "🤖 AI Advisor" tab
3. Type your question or use quick action buttons
4. Get AI-powered responses with clear formatting

## 📁 Project Structure

```
cpu-scheduling-simulator/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── TODO.md               # Development checklist
├── assets/
│   └── style.css         # Custom CSS styling
├── core/
│   ├── __init__.py
│   ├── algorithms.py     # Scheduling algorithms (FCFS, SJF, etc.)
│   ├── gantt.py          # Gantt chart generation
│   └── metrics.py        # Performance metrics calculation
├── ui/
│   ├── __init__.py
│   ├── layout.py         # Page layout and styling
│   ├── inputs.py         # User input handling
│   ├── results.py        # Results display and export
│   └── chatbot.py        # Gemini AI integration
├── report/
│   ├── manual_computation.md
│   ├── os_analysis.md
│   └── screenshots/
└── utils/                # Utility functions
```

## 🎓 Educational Use

This simulator is perfect for:
- **Students** learning operating systems concepts
- **Instructors** teaching CPU scheduling
- **Developers** understanding algorithm behavior
- **Researchers** analyzing scheduling performance

### Learning Path
1. Start with predefined scenarios to understand different workloads
2. Experiment with custom process configurations
3. Compare algorithms to see their strengths and weaknesses
4. Use the AI advisor to deepen understanding
5. Export results for assignments or reports

## 🔧 Configuration

### API Key Setup
The Gemini API key is pre-configured in `ui/chatbot.py`:
```python
GEMINI_API_KEY = "YOUR_API_KEY"
```

To use your own API key:
1. Get a key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Replace the key in `ui/chatbot.py`
3. Restart the application

### Customization
- Edit `assets/style.css` to change colors and styling
- Modify `ui/layout.py` to adjust page structure
- Update `core/algorithms.py` to add new scheduling algorithms

## 🐛 Troubleshooting

### Common Issues

**Module Not Found Error**
```bash
pip install -r requirements.txt
```

**Streamlit Not Running**
```bash
# Check if streamlit is installed
pip show streamlit

# Reinstall if needed
pip install --upgrade streamlit
```

**Gemini API Errors**
- Check internet connection
- Verify API key is valid
- Check API quota limits

**Port Already in Use**
```bash
streamlit run app.py --server.port 8502
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io) for the amazing web app framework
- [Google Gemini](https://ai.google.dev) for AI capabilities
- [Plotly](https://plotly.com) for interactive visualizations
- [FPDF](https://py-pdf.github.io/fpdf2/) for PDF export functionality

## 👨‍💻👩🏻‍💻 Developer
- Arron Kian Parejas (App Developer)
- Graciella Mhervie Jimenez (Project Manager)
- Jenica Sarah Tongol (Documentation/QA)
- Jian kalel Marquez (Unit Testing/Documentation)

## 📧 Contact

For questions or suggestions, please open an issue on GitHub or contact the maintainer.

---

**Happy Scheduling! 🖥️⚡**

Built with ❤️ using Streamlit and Gemini 1.5

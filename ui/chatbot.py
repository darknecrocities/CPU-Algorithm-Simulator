# ui/chatbot.py
import streamlit as st
import google.generativeai as genai
from typing import List, Dict, Optional
import json
from dotenv import load_dotenv
import os

# Configure Gemini API
load_dotenv()

# Now you can access GEMINI_API_KEY from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class SchedulingChatbot:
    """Gemini-powered chatbot for CPU scheduling explanations and advice"""
    
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.configure_gemini()
        self.conversation_history = []
        self.context = self._load_context()
    
    def configure_gemini(self):
        """Configure Gemini API with the provided key"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-3-flash-preview')
            self.chat = self.model.start_chat(history=[])
            self.is_configured = True
        except Exception as e:
            st.error(f"Failed to configure Gemini API: {str(e)}")
            self.is_configured = False
    
    def _load_context(self) -> str:
        """Load system context for the chatbot"""
        return """You are an expert CPU Scheduling Algorithm Advisor and Educator. 
Your role is to:
1. Explain CPU scheduling algorithms (FCFS, SJF, Priority, Round Robin) in clear, educational terms
2. Analyze scheduling results and provide insights
3. Recommend the best algorithm based on process characteristics
4. Answer questions about operating systems and process management
5. Provide step-by-step explanations of how algorithms work

Always format your responses with:
- Clear headings using markdown
- Bullet points for key information
- Code blocks when showing examples
- Emojis to make explanations engaging
- Practical examples and analogies

Be concise but thorough, and always encourage learning!"""
    
    def get_response(self, user_message: str, current_data: Optional[Dict] = None) -> str:
        """
        Get response from Gemini API
        
        Args:
            user_message: User's question or message
            current_data: Optional current simulation data for context
        
        Returns:
            Gemini's response
        """
        if not self.is_configured:
            return "❌ Chatbot is not properly configured. Please check the API key."
        
        # Build context-aware prompt
        prompt = self._build_prompt(user_message, current_data)
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error getting response: {str(e)}\n\nPlease try again or check your internet connection."
    
    def _build_prompt(self, user_message: str, current_data: Optional[Dict]) -> str:
        """Build context-aware prompt"""
        prompt_parts = [self.context]
        
        # Add current simulation context if available
        if current_data:
            prompt_parts.append(f"\n\nCurrent Simulation Context:")
            prompt_parts.append(f"- Algorithm: {current_data.get('algorithm', 'N/A')}")
            prompt_parts.append(f"- Number of Processes: {current_data.get('n_processes', 'N/A')}")
            prompt_parts.append(f"- Average Waiting Time: {current_data.get('avg_waiting', 'N/A')}")
            prompt_parts.append(f"- Average Turnaround Time: {current_data.get('avg_turnaround', 'N/A')}")
            prompt_parts.append(f"- CPU Utilization: {current_data.get('cpu_utilization', 'N/A')}%")
        
        prompt_parts.append(f"\n\nUser Question: {user_message}")
        prompt_parts.append("\nPlease provide a helpful, educational response with clear formatting.")
        
        return "\n".join(prompt_parts)
    
    def explain_algorithm(self, algorithm: str) -> str:
        """Get detailed explanation of a specific algorithm"""
        prompt = f"""Explain the {algorithm} CPU scheduling algorithm in detail. Include:
1. How it works (step-by-step)
2. Advantages and disadvantages
3. Best use cases
4. Real-world examples
5. Time complexity

Format with clear headings, bullet points, and emojis."""
        
        return self.get_response(prompt)
    
    def analyze_results(self, metrics: Dict, algorithm: str) -> str:
        """Analyze simulation results and provide insights"""
        prompt = f"""Analyze these CPU scheduling results for {algorithm}:
- Average Waiting Time: {metrics.get('avg_waiting', 'N/A')}
- Average Turnaround Time: {metrics.get('avg_turnaround', 'N/A')}
- CPU Utilization: {metrics.get('cpu_utilization', 'N/A')}%
- Throughput: {metrics.get('throughput', 'N/A')}

Provide:
1. Performance assessment
2. What these metrics mean
3. Whether this is good performance
4. Suggestions for improvement
5. Comparison to other algorithms

Use emojis and clear formatting."""
        
        return self.get_response(prompt)
    
    def recommend_algorithm(self, process_characteristics: Dict) -> str:
        """Recommend best algorithm based on process characteristics"""
        prompt = f"""Based on these process characteristics, recommend the best CPU scheduling algorithm:
- Number of processes: {process_characteristics.get('n_processes', 'N/A')}
- Average burst time: {process_characteristics.get('avg_burst', 'N/A')}
- Average arrival time spread: {process_characteristics.get('arrival_spread', 'N/A')}
- Priority levels: {process_characteristics.get('priorities', 'N/A')}
- I/O bound vs CPU bound: {process_characteristics.get('io_ratio', 'N/A')}

Recommend the best algorithm and explain why. Also suggest alternatives."""

        return self.get_response(prompt)

    def explain_algorithm_hardcoded(self, algorithm: str) -> str:
        """Get hardcoded explanation of a specific algorithm"""
        explanations = {
            "FCFS": """
# First-Come-First-Serve (FCFS) Scheduling

## How it Works
FCFS is the simplest scheduling algorithm. Processes are executed in the order they arrive in the ready queue.

## Step-by-Step Process
1. Processes arrive and join the ready queue
2. CPU executes the first process in queue until completion
3. Next process starts when current finishes

## Advantages
- Simple to implement
- Fair in terms of arrival order

## Disadvantages
- Convoy effect: short processes wait for long ones
- Poor average waiting time

## Best Use Cases
- Batch processing systems
- Simple systems with similar process lengths

## Time Complexity
O(n) for scheduling decisions
            """,
            "SJF": """
# Shortest Job First (SJF) Scheduling

## How it Works
Selects the process with the smallest burst time from ready queue.

## Step-by-Step Process
1. Check ready processes
2. Select shortest remaining burst time
3. Execute until completion or preemption

## Advantages
- Optimal for minimizing waiting time
- Proven optimal for single processor

## Disadvantages
- Starvation for long processes
- Requires knowledge of burst times

## Best Use Cases
- Systems with predictable burst times
- Real-time systems

## Time Complexity
O(n²) for finding shortest job
            """,
            "Priority": """
# Priority Scheduling

## How it Works
Processes are assigned priorities and executed based on priority level (lower number = higher priority).

## Step-by-Step Process
1. Assign priorities to processes
2. Execute highest priority process first
3. Continue until all processes complete

## Advantages
- Critical processes get priority
- Flexible priority assignment

## Disadvantages
- Starvation of low priority processes
- Priority inversion possible

## Best Use Cases
- Real-time systems
- Systems with critical tasks

## Time Complexity
O(n²) for priority sorting
            """,
            "Round Robin": """
# Round Robin Scheduling

## How it Works
Each process gets a fixed time slice (quantum) in cyclic order.

## Step-by-Step Process
1. Set time quantum
2. Execute process for quantum or until completion
3. Move to next process in queue
4. Repeat until all processes finish

## Advantages
- Fair CPU distribution
- No starvation
- Good response time

## Disadvantages
- Context switching overhead
- Poor for long processes

## Best Use Cases
- Time-sharing systems
- Interactive systems

## Time Complexity
O(n) with fixed quantum
            """
        }
        return explanations.get(algorithm, "Explanation not available")


def render_chatbot_ui(chatbot: SchedulingChatbot, current_data: Optional[Dict] = None):
    """Render the chatbot interface in Streamlit"""
    
    st.markdown("""
        <div class="chatbot-container">
            <h3 style="color: #6366f1; margin-bottom: 20px;">
                🤖 Gemini AI Scheduling Advisor
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📚 Explain FCFS", width='stretch'):
            explanation = chatbot.explain_algorithm_hardcoded("FCFS")
            st.session_state.chat_history.append({
                'role': 'user',
                'content': 'Explain FCFS algorithm'
            })
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': explanation
            })
            st.rerun()

    with col2:
        if st.button("📚 Explain SJF", width='stretch'):
            explanation = chatbot.explain_algorithm_hardcoded("SJF")
            st.session_state.chat_history.append({
                'role': 'user',
                'content': 'Explain SJF algorithm'
            })
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': explanation
            })
            st.rerun()

    with col3:
        if st.button("📚 Explain Priority", width='stretch'):
            explanation = chatbot.explain_algorithm_hardcoded("Priority")
            st.session_state.chat_history.append({
                'role': 'user',
                'content': 'Explain Priority scheduling'
            })
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': explanation
            })
            st.rerun()

    with col4:
        if st.button("📚 Explain Round Robin", width='stretch'):
            explanation = chatbot.explain_algorithm_hardcoded("Round Robin")
            st.session_state.chat_history.append({
                'role': 'user',
                'content': 'Explain Round Robin algorithm'
            })
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': explanation
            })
            st.rerun()
    
    # Display conversation history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat display area
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f"""
                    <div class="chat-message user">
                        <b>You:</b> {msg['content']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="chat-message assistant">
                        <b>🤖 Gemini:</b><br>{msg['content']}
                    </div>
                """, unsafe_allow_html=True)
    
    # Input area
    st.markdown("---")
    
    # Initialize chat input in session state
    if 'chat_input' not in st.session_state:
        st.session_state.chat_input = ""
    
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        user_input = st.text_input(
            "Ask about CPU scheduling...",
            value=st.session_state.chat_input,
            key="chat_text_input",
            placeholder="e.g., Which algorithm is best for real-time systems?"
        )
    
    with col_button:
        send_button = st.button("Send 📤", width='stretch', type="primary")
    
    # Handle message sending
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Get Gemini response
        with st.spinner("🤖 Gemini is thinking..."):
            response = chatbot.get_response(user_input, current_data)
        
        # Add assistant response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response
        })
        
        # Clear input
        st.session_state.chat_input = ""
        st.rerun()
    
    # Additional quick actions
    st.markdown("---")
    st.markdown("### 🎯 Quick Analysis")
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        if st.button("🔍 Analyze Current Results", width='stretch'):
            if current_data:
                with st.spinner("Analyzing..."):
                    analysis = chatbot.analyze_results(current_data, current_data.get('algorithm', 'Unknown'))
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': 'Analyze my current simulation results'
                    })
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': analysis
                    })
                    st.rerun()
            else:
                st.warning("Run a simulation first!")

    with col6:
        if st.button("💡 Get Recommendations", width='stretch'):
            st.session_state.chat_input = "Which algorithm should I use for my processes?"

    with col7:
        if st.button("🧹 Clear Chat", width='stretch'):
            st.session_state.chat_history = []
            st.rerun()
    
    # End of render_chatbot_ui function
    pass


def initialize_chatbot() -> SchedulingChatbot:
    """Initialize or get existing chatbot from session state"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = SchedulingChatbot()
    return st.session_state.chatbot

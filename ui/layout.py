# ui/layout.py
import streamlit as st
import os

def load_css():
    """Load external CSS file"""
    css_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'style.css')
    try:
        with open(css_path, 'r') as f:
            css_content = f.read()
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def setup_layout():
    """Initialize page layout and styling"""
    # Load custom CSS
    load_css()
    
    # Custom header with animation
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 3em; margin-bottom: 10px;">
                🖥️ CPU Scheduling Simulator
            </h1>
            <p style="color: #94a3b8; font-size: 1.2em;">
                Interactive Algorithm Visualization & Analysis Platform
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Add theme toggle in sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🎨 Appearance")
        theme = st.selectbox(
            "Theme",
            ["Dark", "Light"],
            index=0,
            help="Select your preferred theme"
        )
        
        if theme == "Light":
            st.markdown("""
                <style>
                .stApp {
                    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
                }
                h2, h3, p, label {
                    color: #1e293b !important;
                }
                .metric-box, .metric-card, .gantt-container, .chatbot-container {
                    background: white !important;
                    color: #1e293b !important;
                }
                </style>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.info("💡 Tip: Use the chatbot for algorithm explanations!")

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 20px; color: #64748b;">
            <p>Built with ❤️ using Streamlit | Powered by Gemini 1.5 AI</p>
            <p style="font-size: 0.9em;">CPU Scheduling Algorithm Simulator v2.0</p>
        </div>
    """, unsafe_allow_html=True)

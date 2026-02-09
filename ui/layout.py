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
    
    # Custom header with modern design
    st.markdown("""
        <div style="text-align: center; padding: 30px 0; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 15px; margin-bottom: 20px;">
            <h1 style="font-size: 2.5em; margin-bottom: 10px; color: #f8fafc;">
                🖥️ CPU Scheduling Simulator
            </h1>
            <p style="color: #94a3b8; font-size: 1.1em;">
                Interactive Algorithm Visualization & Analysis Platform
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Theme toggle in main page
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        theme = st.selectbox(
            "🎨 Theme",
            ["Dark", "Light"],
            index=0,
            help="Select your preferred theme",
            label_visibility="collapsed"
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

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 20px; color: #64748b;">
            <p>Dveloped by THE-SIS IT | Powered by Gemini 3.0 AI</p>
            <p style="font-size: 0.9em;">CPU Scheduling Algorithm Simulator v2.0</p>
        </div>
    """, unsafe_allow_html=True)

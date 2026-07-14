import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import time
import base64
from datetime import datetime
import numpy as np

# Import utilities
from utils.csv_processor import CSVProcessor
from utils.gemini_service import GeminiService
from utils.chart_generator import ChartGenerator
from utils.advanced_features import AdvancedAnalytics, DataQualityAnalyzer, ExportManager
from utils.ui_enhancements import ModernUI, DataStoryteller
from utils.insight_engine import InsightEngine, AutomatedReporting

# Page configuration
st.set_page_config(
    page_title="AI-Powered BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecf5 100%);
        transition: background 0.3s ease;
    }
    
    /* Dark theme */
    .dark-theme {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #fff;
    }
    
    .dark-theme .main-header {
        background: linear-gradient(135deg, #2a2a4a 0%, #1a1a3a 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        animation: slideDown 0.5s ease-out;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-message {
        padding: 1.2rem 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s ease-out;
        position: relative;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
        border-bottom-right-radius: 5px;
    }
    
    .assistant-message {
        background: white;
        color: #2c3e50;
        border: 1px solid #e2e8f0;
        margin-right: 2rem;
        border-bottom-left-radius: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    
    .metric-card {
        background: white;
        padding: 1.8rem 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
        border: 1px solid rgba(102,126,234,0.15);
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(102,126,234,0.15);
        border-color: rgba(102,126,234,0.3);
    }
    
    .metric-card:hover::before {
        transform: scaleX(1);
    }
    
    .insight-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 0.8rem;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        color: #2c3e50;
    }
    
    .insight-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.1);
        background: white;
    }
    
    .suggested-query {
        background: white;
        padding: 0.8rem 1rem;
        border-radius: 30px;
        border: 1px solid #e2e8f0;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        margin: 0.2rem;
        font-size: 0.9rem;
        animation: fadeIn 0.5s ease-out;
        color: #4a5568;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    .suggested-query:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: transparent;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(102,126,234,0.3);
    }
    
    /* Upload area */
    .upload-area {
        border: 3px dashed #cbd5e1;
        border-radius: 24px;
        padding: 3rem;
        text-align: center;
        background: white;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(102,126,234,0.2); }
        70% { box-shadow: 0 0 0 10px rgba(102,126,234,0); }
        100% { box-shadow: 0 0 0 0 rgba(102,126,234,0); }
    }
    
    .upload-area:hover {
        border-color: #667eea;
        background: #f8fafc;
        transform: scale(1.02);
        box-shadow: 0 20px 40px rgba(102,126,234,0.1);
    }
    
    /* Loading animation */
    .loader {
        width: 50px;
        height: 50px;
        margin: 20px auto;
        position: relative;
    }
    
    .loader:before {
        content: '';
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 3px solid transparent;
        border-top-color: #667eea;
        border-bottom-color: #764ba2;
        position: absolute;
        top: 0;
        left: 0;
        animation: spin 1s ease-in-out infinite;
    }
    
    .loader:after {
        content: '';
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 3px solid transparent;
        border-left-color: #667eea;
        border-right-color: #764ba2;
        position: absolute;
        top: 5px;
        left: 5px;
        animation: spin 0.8s ease-in-out infinite reverse;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        background-color: transparent;
        transition: all 0.3s ease;
        color: #64748b;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102,126,234,0.1);
        color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #64748b 0%, #475569 100%);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .main-header p {
            font-size: 0.9rem;
        }
        
        .user-message, .assistant-message {
            margin-left: 0.5rem;
            margin-right: 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'csv_processor' not in st.session_state:
    st.session_state.csv_processor = CSVProcessor()

if 'gemini_service' not in st.session_state:
    st.session_state.gemini_service = GeminiService()

if 'chart_generator' not in st.session_state:
    st.session_state.chart_generator = ChartGenerator()

if 'advanced_analytics' not in st.session_state:
    st.session_state.advanced_analytics = AdvancedAnalytics()

if 'data_quality' not in st.session_state:
    st.session_state.data_quality = DataQualityAnalyzer()

if 'export_manager' not in st.session_state:
    st.session_state.export_manager = ExportManager()

if 'insight_engine' not in st.session_state:
    st.session_state.insight_engine = InsightEngine()

if 'data_storyteller' not in st.session_state:
    st.session_state.data_storyteller = DataStoryteller()

if 'session_id' not in st.session_state:
    st.session_state.session_id = None

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hi! Upload a CSV file and I'll help you analyze your data!"}
    ]

if 'current_chart' not in st.session_state:
    st.session_state.current_chart = None

if 'data_info' not in st.session_state:
    st.session_state.data_info = None

if 'chart_history' not in st.session_state:
    st.session_state.chart_history = []

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

if 'alerts' not in st.session_state:
    st.session_state.alerts = []

if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Sidebar
with st.sidebar:
    st.markdown("## 📊 AI BI Dashboard")
    st.markdown("---")
    
    # Theme selector
    st.subheader("🎨 Theme")
    theme = st.radio(
        "Select Theme",
        ["Light", "Dark"],
        horizontal=True,
        key="theme_selector",
        label_visibility="collapsed"
    )
    
    if theme == "Dark" and st.session_state.theme != 'dark':
        st.session_state.theme = 'dark'
        st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            }
            .main-header {
                background: linear-gradient(135deg, #2a2a4a 0%, #1a1a3a 100%);
            }
            .assistant-message {
                background: #2d3748;
                color: #e2e8f0;
                border-color: #4a5568;
            }
            .metric-card {
                background: #2d3748;
                color: #e2e8f0;
            }
            .metric-card h2 {
                color: #e2e8f0;
            }
            .insight-card {
                background: #2d3748;
                color: #e2e8f0;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.session_state.theme = 'light'
    
    st.markdown("---")
    
    # File Upload
    st.subheader("📁 Upload Data")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload your CSV file to start analysis",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        with st.spinner("🔄 Processing your data..."):
            result = st.session_state.csv_processor.process_upload(uploaded_file)
            
            if 'error' in result:
                st.error(f"Error: {result['error']}")
            else:
                st.session_state.session_id = result['session_id']
                st.session_state.data_info = result
                st.success(f"✅ Loaded: {result['filename']}")
                
                # Display metrics with modern cards
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card" style="padding: 1rem;">
                        <div style="font-size: 2rem; color: #667eea;">📊</div>
                        <h3 style="margin: 0.5rem 0;">{result['row_count']:,}</h3>
                        <p style="color: #666;">Rows</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-card" style="padding: 1rem;">
                        <div style="font-size: 2rem; color: #667eea;">📋</div>
                        <h3 style="margin: 0.5rem 0;">{result['col_count']}</h3>
                        <p style="color: #666;">Columns</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Favorites
    if st.session_state.favorites:
        st.subheader("⭐ Favorites")
        for i, fav in enumerate(st.session_state.favorites[-3:]):
            if st.button(f"📈 Favorite {i+1}", key=f"fav_{i}", use_container_width=True):
                st.session_state.current_chart = fav
                st.rerun()
    
    # Chart History
    if st.session_state.chart_history:
        st.subheader("📊 Chart History")
        for i, chart in enumerate(st.session_state.chart_history[-5:]):
            chart_type = chart.get('type', 'Chart').title()
            if st.button(f"📈 {chart_type} {i+1}", key=f"hist_{i}", use_container_width=True):
                st.session_state.current_chart = chart
                st.rerun()
    
    st.markdown("---")
    st.caption("🚀 Powered by Advanced AI | Built with Streamlit")

# Main Header
st.markdown('<div class="main-header"><h1>🤖 AI-Powered Business Intelligence Dashboard</h1><p>Chat with your data • Get AI insights • Create stunning visualizations • Make data-driven decisions</p></div>', unsafe_allow_html=True)

# Initial state - Upload prompt
if not st.session_state.session_id:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="upload-area">
            <div style="font-size: 4rem;">📤</div>
            <h3>Upload Your Data</h3>
            <p>Upload a CSV file to start your analysis journey</p>
            <p style="color: #667eea; font-size: 0.9rem;">Supports: CSV files up to 200MB</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 💡 Sample queries you can ask:
        - "Show me a pie chart of the data"
        - "Create a bar chart comparing columns"
        - "Show trends over time"
        - "Analyze the data distribution"
        - "Generate insights"
        - "Check data quality"
        """)
else:
    # Metrics Row with enhanced cards
    if st.session_state.data_info:
        cols = st.columns(4)
        
        with cols[0]:
            st.markdown(f"""
            <div class='metric-card'>
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #2c3e50;">{st.session_state.data_info['row_count']:,}</div>
                <div style="font-size: 0.9rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">TOTAL RECORDS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown(f"""
            <div class='metric-card'>
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">📋</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #2c3e50;">{st.session_state.data_info['col_count']}</div>
                <div style="font-size: 0.9rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">TOTAL COLUMNS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[2]:
            num_count = len(st.session_state.data_info.get('numeric_cols', []))
            st.markdown(f"""
            <div class='metric-card'>
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🔢</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #2c3e50;">{num_count}</div>
                <div style="font-size: 0.9rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">NUMERIC COLUMNS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[3]:
            cat_count = len(st.session_state.data_info.get('categorical_cols', []))
            st.markdown(f"""
            <div class='metric-card'>
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🏷️</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #2c3e50;">{cat_count}</div>
                <div style="font-size: 0.9rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">CATEGORIES</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main Layout with Enhanced Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💬 Chat & Visualize", 
        "🔍 Data Explorer", 
        "📈 Advanced Analytics",
        "🤖 AI Insights",
        "📊 Data Quality",
        "⚡ Smart Reports"
    ])
    
    with tab1:
        # Chat Interface
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f'<div class="chat-message user-message"><b>👤 You:</b> {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message assistant-message"><b>🤖 Assistant:</b> {message["content"]}</div>', unsafe_allow_html=True)
        
        # Chat Input with enhanced design
        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([5, 1])
            with col1:
                user_input = st.text_input(
                    "Ask about your data...", 
                    placeholder="e.g., Create a pie chart, Show trends, Analyze data...", 
                    label_visibility="collapsed"
                )
            with col2:
                submit = st.form_submit_button("Send 📤", use_container_width=True)
        
        if submit and user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get data
            df = st.session_state.csv_processor.get_session_data(st.session_state.session_id)
            
            if df is not None:
                with st.spinner("🤔 Analyzing your request..."):
                    # Interpret query
                    interpretation = st.session_state.gemini_service.interpret_query(
                        user_input,
                        st.session_state.data_info['columns'],
                        st.session_state.data_info.get('summary', {})
                    )
                    
                    # Generate chart if requested
                    if interpretation['intent'] == 'visualize' and interpretation['chart_type']:
                        x_axis = interpretation['x_axis']
                        if not x_axis and st.session_state.data_info['columns']:
                            x_axis = st.session_state.data_info['columns'][0]
                        
                        chart = st.session_state.chart_generator.generate_chart(
                            df,
                            interpretation['chart_type'],
                            x_axis,
                            interpretation['y_axis'],
                            interpretation['aggregation']
                        )
                        
                        if 'error' not in chart:
                            st.session_state.current_chart = chart
                            st.session_state.chart_history.append(chart)
                            
                            # Generate insights
                            insights = st.session_state.gemini_service.generate_insights(df, chart)
                            
                            response = f"✅ I've created a {interpretation['chart_type']} chart showing {x_axis}!"
                            
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": response,
                                "chart": chart,
                                "insights": insights
                            })
                        else:
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": f"❌ Sorry: {chart['error']}"
                            })
                    else:
                        # Generate general response
                        insights = st.session_state.insight_engine.generate_business_insights(df)
                        response = f"💬 Here's what I found: {insights[0] if insights else 'Ask me to create visualizations!'}"
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "insights": insights
                        })
            
            st.rerun()
        
        # Current Visualization with enhanced controls
        if st.session_state.current_chart:
            st.markdown("### 📊 Current Visualization")
            
            if 'figure' in st.session_state.current_chart:
                fig = go.Figure(st.session_state.current_chart['figure'])
                st.plotly_chart(fig, use_container_width=True)
                
                # Enhanced chart controls
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    if st.button("🗑️ Clear", use_container_width=True):
                        st.session_state.current_chart = None
                        st.rerun()
                with col2:
                    if st.button("🔄 Refresh", use_container_width=True):
                        st.rerun()
                with col3:
                    if st.button("⭐ Favorite", use_container_width=True):
                        if st.session_state.current_chart not in st.session_state.favorites:
                            st.session_state.favorites.append(st.session_state.current_chart)
                            st.success("Added to favorites!")
                with col4:
                    if st.button("📤 Share", use_container_width=True):
                        st.info("Sharing feature coming soon!")
                with col5:
                    if st.button("📥 Download", use_container_width=True):
                        # Export chart
                        export_result = st.session_state.export_manager.export_chart(
                            st.session_state.current_chart['figure'], 'png'
                        )
                        if 'error' not in export_result:
                            b64 = base64.b64encode(export_result['data']).decode()
                            href = f'<a href="data:image/png;base64,{b64}" download="{export_result["filename"]}">Click to download</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            st.success("✅ Chart ready for download!")
            
            # Insights with enhanced display
            st.markdown("### 💡 AI Insights")
            
            # Get latest insights
            insights_shown = False
            for msg in reversed(st.session_state.messages):
                if "insights" in msg:
                    for insight in msg["insights"]:
                        st.markdown(f'<div class="insight-card">💡 {insight}</div>', unsafe_allow_html=True)
                    insights_shown = True
                    break
            
            if not insights_shown:
                # Generate fresh insights
                df = st.session_state.csv_processor.get_session_data(st.session_state.session_id)
                if df is not None:
                    insights = st.session_state.insight_engine.generate_business_insights(df)
                    for insight in insights:
                        st.markdown(f'<div class="insight-card">💡 {insight}</div>', unsafe_allow_html=True)
        
        # Enhanced Suggested Queries
        st.markdown("### 💡 Try These Queries")
        cols = st.columns(4)
        suggestions = [
            "📊 Show pie chart",
            "📈 Create bar chart", 
            "📉 Analyze trends",
            "🤖 Generate insights"
        ]
        for i, suggestion in enumerate(suggestions):
            with cols[i]:
                if st.button(suggestion, key=f"sugg_{i}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": suggestion})
                    st.rerun()
    
    with tab2:
        # Enhanced Data Explorer
        st.subheader("🔍 Data Explorer")
        
        df = st.session_state.csv_processor.get_session_data(st.session_state.session_id)
        
        if df is not None:
            # Column overview with statistics
            st.markdown("### 📋 Column Overview")
            
            col_info = []
            for col in df.columns:
                col_type = str(df[col].dtype)
                missing = df[col].isnull().sum()
                missing_pct = (missing / len(df)) * 100
                unique = df[col].nunique()
                
                col_info.append({
                    'Column': col,
                    'Type': col_type,
                    'Missing': f"{missing} ({missing_pct:.1f}%)",
                    'Unique Values': unique
                })
            
            st.dataframe(pd.DataFrame(col_info), use_container_width=True)
            
            # Data preview with pagination
            st.markdown("### 👁️ Data Preview")
            rows_per_page = st.selectbox("Rows per page", [5, 10, 20, 50, 100], index=1)
            page = st.number_input("Page", min_value=1, max_value=max(1, len(df) // rows_per_page + 1), value=1)
            
            start_idx = (page - 1) * rows_per_page
            end_idx = min(start_idx + rows_per_page, len(df))
            
            st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)
            st.caption(f"Showing {start_idx + 1} to {end_idx} of {len(df)} rows")
            
            # Enhanced column statistics
            st.markdown("### 📊 Detailed Column Statistics")
            
            # Select column for statistics
            selected_col = st.selectbox("Select a column to analyze", df.columns)
            
            if selected_col:
                stats = st.session_state.chart_generator.get_column_stats(df, selected_col)
                if stats:
                    if 'min' in stats:  # Numeric
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Minimum", f"{stats['min']:.2f}")
                            st.metric("Maximum", f"{stats['max']:.2f}")
                        with col2:
                            st.metric("Mean", f"{stats['mean']:.2f}")
                            st.metric("Median", f"{stats['median']:.2f}")
                        with col3:
                            st.metric("Std Deviation", f"{stats['std']:.2f}")
                            st.metric("Variance", f"{stats['std']**2:.2f}")
                        with col4:
                            st.metric("Sum", f"{stats['sum']:.2f}")
                            st.metric("Count", len(df[selected_col].dropna()))
                        
                        # Histogram of numeric column
                        fig = go.Figure()
                        fig.add_trace(go.Histogram(
                            x=df[selected_col].dropna(),
                            nbinsx=30,
                            name=selected_col,
                            marker_color='#667eea'
                        ))
                        fig.update_layout(
                            title=f"Distribution of {selected_col}",
                            xaxis_title=selected_col,
                            yaxis_title="Frequency",
                            template='plotly_white'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                    else:  # Categorical
                        st.write(f"**Unique values:** {stats.get('unique_values', 0)}")
                        st.write(f"**Most common:** {stats.get('most_common', 'N/A')}")
                        
                        if 'top_values' in stats:
                            st.write("**Top 10 values:**")
                            # Create bar chart for top values
                            top_df = pd.DataFrame(
                                list(stats['top_values'].items()), 
                                columns=['Value', 'Count']
                            ).head(10)
                            
                            fig = go.Figure()
                            fig.add_trace(go.Bar(
                                x=top_df['Count'],
                                y=top_df['Value'],
                                orientation='h',
                                marker_color='#667eea',
                                text=top_df['Count'],
                                textposition='outside'
                            ))
                            fig.update_layout(
                                title=f"Top Values in {selected_col}",
                                xaxis_title="Count",
                                yaxis_title="Value",
                                template='plotly_white',
                                height=400
                            )
                            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Enhanced Advanced Analytics
        st.subheader("📈 Advanced Analytics")
        
        df = st.session_state.csv_processor.get_session_data(st.session_state.session_id)
        
        if df is not None:
            # Analytics type selector
            analytics_type = st.radio(
                "Select Analysis Type",
                ["Visualizations", "Correlation Analysis", "Time Series", "Pattern Discovery"],
                horizontal=True
            )
            
            if analytics_type == "Visualizations":
                # Chart type selector
                chart_type = st.selectbox(
                    "Select Chart Type",
                    ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Histogram", "Box Plot", "Area Chart"]
                )
                
                # Get columns
                columns = df.columns.tolist()
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if chart_type in ["Pie Chart", "Histogram"]:
                        x_axis = st.selectbox("Select Column", columns)
                        y_axis = None
                    else:
                        x_axis = st.selectbox("X-Axis (Category/Time)", columns)
                
                with col2:
                    if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot", "Area Chart"]:
                        y_options = numeric_cols if numeric_cols else columns
                        y_axis = st.selectbox("Y-Axis (Value)", y_options)
                    else:
                        y_axis = None
                
                # Aggregation for bar/line
                aggregation = "count"
                if chart_type in ["Bar Chart", "Line Chart", "Area Chart"] and y_axis:
                    aggregation = st.selectbox("Aggregation Method", ["sum", "average", "count", "min", "max"])
                
                # Generate button
                if st.button("🎨 Generate Visualization", use_container_width=True):
                    chart_type_map = {
                        "Bar Chart": "bar",
                        "Line Chart": "line",
                        "Pie Chart": "pie",
                        "Scatter Plot": "scatter",
                        "Histogram": "histogram",
                        "Box Plot": "box",
                        "Area Chart": "area"
                    }
                    
                    chart = st.session_state.chart_generator.generate_chart(
                        df,
                        chart_type_map.get(chart_type, "bar"),
                        x_axis,
                        y_axis,
                        aggregation,
                        title=f"{chart_type} Analysis"
                    )
                    
                    if 'error' not in chart:
                        st.session_state.current_chart = chart
                        st.session_state.chart_history.append(chart)
                        st.success("✅ Chart generated! Check the Chat tab to view it.")
                    else:
                        st.error(f"Error: {chart['error']}")
            
            elif analytics_type == "Correlation Analysis":
                st.markdown("### 🔗 Correlation Analysis")
                
                numeric_df = df.select_dtypes(include=[np.number])
                if len(numeric_df.columns) >= 2:
                    correlation_result = st.session_state.advanced_analytics.correlation_analysis(df)
                    
                    if 'error' not in correlation_result:
                        # Display correlation heatmap
                        if 'heatmap' in correlation_result:
                            fig = go.Figure(correlation_result['heatmap'])
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Display strong correlations
                        if correlation_result.get('strong_correlations'):
                            st.markdown("### 💪 Strong Correlations Found")
                            for corr in correlation_result['strong_correlations']:
                                color = "#10b981" if corr['correlation'] > 0 else "#ef4444"
                                st.markdown(f"""
                                <div style="
                                    background: white;
                                    padding: 1rem;
                                    border-radius: 10px;
                                    margin-bottom: 0.5rem;
                                    border-left: 4px solid {color};
                                ">
                                    <strong>{corr['var1']} ↔ {corr['var2']}</strong><br>
                                    Correlation: {corr['correlation']:.3f} ({corr['strength']})
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Summary
                        st.markdown("### 📊 Summary")
                        st.json(correlation_result['summary'])
                    else:
                        st.warning("Not enough numeric columns for correlation analysis")
                else:
                    st.warning("Need at least 2 numeric columns for correlation analysis")
            
            elif analytics_type == "Time Series":
                st.markdown("### 📈 Time Series Analysis")
                
                # Select date and value columns
                date_cols = df.select_dtypes(include=['datetime64', 'object']).columns.tolist()
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if date_cols and numeric_cols:
                    col1, col2 = st.columns(2)
                    with col1:
                        date_col = st.selectbox("Select Date Column", date_cols)
                    with col2:
                        value_col = st.selectbox("Select Value Column", numeric_cols)
                    
                    if st.button("🔍 Analyze Time Series", use_container_width=True):
                        with st.spinner("Analyzing time series data..."):
                            ts_result = st.session_state.advanced_analytics.time_series_analysis(
                                df, date_col, value_col
                            )
                            
                            if 'error' not in ts_result:
                                # Display time series chart
                                if 'figure' in ts_result:
                                    fig = go.Figure(ts_result['figure'])
                                    st.plotly_chart(fig, use_container_width=True)
                                
                                # Display statistics
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Mean", f"{ts_result['statistics']['mean']:.2f}")
                                    st.metric("Std Dev", f"{ts_result['statistics']['std']:.2f}")
                                with col2:
                                    st.metric("Min", f"{ts_result['statistics']['min']:.2f}")
                                    st.metric("Max", f"{ts_result['statistics']['max']:.2f}")
                                with col3:
                                    st.metric("Trend", ts_result['trend']['direction'])
                                    st.metric("R²", f"{ts_result['trend']['r_squared']:.3f}")
                            else:
                                st.error(ts_result['error'])
                else:
                    st.warning("Need both date and numeric columns for time series analysis")
            
            elif analytics_type == "Pattern Discovery":
                st.markdown("### 🔍 Pattern Discovery")
                
                patterns = st.session_state.insight_engine.discover_patterns(df)
                
                if patterns:
                    for pattern in patterns:
                        with st.expander(f"🎯 {pattern['title']}", expanded=True):
                            st.markdown(f"**{pattern['description']}**")
                            st.markdown(f"*Confidence: {pattern['confidence']}*")
                            if 'details' in pattern:
                                st.json(pattern['details'])
                else:
                    st.info("No significant patterns discovered yet. Try different data or analysis methods.")
    
    with tab4:
        # AI Insights Tab
        st.subheader("🤖 AI-Powered Insights")
        
        df = st.session_state.csv_processor.get_session_data(st.session_state.session_id)
        
        if df is not None:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 🎯 Discovered Patterns")
                patterns = st.session_state.insight_engine.discover_patterns(df)
                
                if patterns:
                    for pattern in patterns:
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
                            padding: 1.5rem;
                            border-radius: 15px;
                            margin-bottom: 1rem;
                            border: 1px solid rgba(102,126,234,0.2);
                        ">
                            <h4 style="color: #2c3e50; margin-bottom: 0.5rem;">{pattern['title']}</h4>
                            <p style="color: #64748b;">{pattern['description']}</p>
                            <p style="color: #667eea; font-size: 0.9rem;">Confidence: {pattern['confidence']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No significant patterns discovered yet. Try different data or analysis methods.")
            
            with col2:
                st.markdown("### 💼 Business Insights")
                business_insights = st.session_state.insight_engine.generate_business_insights(df)
                
                for insight in business_insights:
                    st.markdown(f"""
                    <div style="
                        background: white;
                        padding: 1rem;
                        border-radius: 10px;
                        margin-bottom: 0.5rem;
                        border-left: 4px solid #10b981;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    ">
                        {insight}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Smart Recommendations
            st.markdown("### 🎯 Smart Recommendations")
            recommendations = st.session_state.insight_engine.smart_recommendations(df)
            
            if recommendations:
                cols = st.columns(len(recommendations))
                for i, rec in enumerate(recommendations):
                    priority_color = {
                        'High': '#ef4444',
                        'Medium': '#f59e0b',
                        'Low': '#10b981'
                    }.get(rec['priority'], '#64748b')
                    
                    with cols[i]:
                        st.markdown(f"""
                        <div style="
                            background: white;
                            padding: 1.5rem;
                            border-radius: 15px;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                            border-top: 4px solid {priority_color};
                            height: 100%;
                        ">
                            <h4 style="color: #2c3e50; margin-bottom: 0.5rem;">{rec['action']}</h4>
                            <p style="color: #64748b; font-size: 0.9rem;">{rec['reason']}</p>
                            <p style="color: {priority_color}; font-size: 0.8rem; font-weight: 600;">Priority: {rec['priority']}</p>
                            <p style="color: #10b981; font-size: 0.9rem;">Impact: {rec['impact']}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    with tab5:
        # Data Quality Tab
        st.subheader("📊 Data Quality Analysis")
        
        df = st.session_state.csv_processor.get_session_data(st.session_state.session_id)
        
        if df is not None:
            # Run quality analysis
            quality_report = st.session_state.data_quality.analyze_data_quality(df)
            
            # Overall score with gauge
            col1, col2 = st.columns([1, 2])
            
            with col1:
                score = quality_report['overall_score']
                score_color = '#10b981' if score >= 80 else '#f59e0b' if score >= 60 else '#ef4444'
                
                st.markdown(f"""
                <div style="
                    background: white;
                    padding: 2rem;
                    border-radius: 20px;
                    text-align: center;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                ">
                    <div style="
                        width: 150px;
                        height: 150px;
                        border-radius: 50%;
                        background: conic-gradient({score_color} {score * 3.6}deg, #f0f0f0 0deg);
                        margin: 0 auto 1rem auto;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">
                        <div style="
                            width: 120px;
                            height: 120px;
                            background: white;
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">
                            <span style="font-size: 2.5rem; font-weight: 700; color: {score_color};">{score}</span>
                        </div>
                    </div>
                    <h3 style="color: #2c3e50;">Data Quality Score</h3>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 📋 Detailed Analysis")
                st.json(quality_report['detailed_analysis'])
            
            # Issues and Recommendations
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ⚠️ Issues Found")
                if quality_report['issues']:
                    for issue in quality_report['issues']:
                        with st.expander(f"🔴 {issue['type'].title()}"):
                            st.write(issue['description'])
                            if 'details' in issue:
                                st.json(issue['details'])
                else:
                    st.success("✅ No issues found! Your data is clean.")
            
            with col2:
                st.markdown("### 💡 Recommendations")
                for rec in quality_report['recommendations']:
                    st.markdown(f"""
                    <div style="
                        background: #f0f9ff;
                        padding: 1rem;
                        border-radius: 10px;
                        margin-bottom: 0.5rem;
                        border-left: 4px solid #3b82f6;
                    ">
                        {rec}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Data Story
            st.markdown("### 📖 Data Story")
            story = st.session_state.data_storyteller.create_data_story(df)
            st.markdown(story)
    
    with tab6:
        # Smart Reports Tab
        st.subheader("⚡ Smart Reports & Export")
        
        df = st.session_state.csv_processor.get_session_data(st.session_state.session_id)
        
        if df is not None:
            # Report Types
            report_type = st.radio(
                "Select Report Type",
                ["Executive Summary", "Technical Analysis", "Business Insights", "Custom Report"],
                horizontal=True
            )
            
            if report_type == "Executive Summary":
                report = AutomatedReporting.generate_executive_summary(df)
                st.markdown(report)
                
                # Export options
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📥 Download as Markdown", use_container_width=True):
                        export_result = st.session_state.export_manager.export_data(
                            pd.DataFrame({'Report': [report]}), 'markdown', 'executive_summary'
                        )
                        if 'error' not in export_result:
                            b64 = base64.b64encode(export_result['data'].encode()).decode()
                            href = f'<a href="data:text/markdown;base64,{b64}" download="{export_result["filename"]}">Click to download</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            st.success("✅ Report ready for download!")
            
            elif report_type == "Technical Analysis":
                st.markdown("### 📊 Technical Metrics")
                
                numeric_df = df.select_dtypes(include=[np.number])
                if len(numeric_df.columns) > 0:
                    stats_data = []
                    for col in numeric_df.columns[:5]:  # Limit to 5 columns
                        stats_data.append({
                            'Metric': col,
                            'Count': len(numeric_df[col].dropna()),
                            'Mean': f"{numeric_df[col].mean():.2f}",
                            'Std': f"{numeric_df[col].std():.2f}",
                            'Min': f"{numeric_df[col].min():.2f}",
                            '25%': f"{numeric_df[col].quantile(0.25):.2f}",
                            '50%': f"{numeric_df[col].median():.2f}",
                            '75%': f"{numeric_df[col].quantile(0.75):.2f}",
                            'Max': f"{numeric_df[col].max():.2f}"
                        })
                    
                    st.dataframe(pd.DataFrame(stats_data), use_container_width=True)
            
            elif report_type == "Business Insights":
                st.markdown("### 💼 Business Intelligence Report")
                
                insights = st.session_state.insight_engine.generate_business_insights(df)
                for i, insight in enumerate(insights, 1):
                    st.markdown(f"{i}. {insight}")
            
            # Export Options
            st.markdown("---")
            st.markdown("### 📦 Export Data")
            
            export_format = st.selectbox(
                "Select Export Format",
                ["csv", "excel", "json", "html", "markdown"]
            )
            
            if st.button("🚀 Export Data", use_container_width=True):
                with st.spinner("Preparing export..."):
                    export_result = st.session_state.export_manager.export_data(
                        df, export_format, 'data_export'
                    )
                    
                    if 'error' not in export_result:
                        if export_format in ['csv', 'json', 'html', 'markdown']:
                            b64 = base64.b64encode(export_result['data'].encode()).decode()
                            href = f'<a href="data:{export_result["mime_type"]};base64,{b64}" download="{export_result["filename"]}">Click here to download your {export_format.upper()} file</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            st.success(f"✅ Export ready! Click the link above to download.")
                        elif export_format == 'excel':
                            st.success("Excel export ready! Check your downloads folder.")
                    else:
                        st.error(f"Export failed: {export_result['error']}")
            
            # Chart Export (if current chart exists)
            if st.session_state.current_chart and 'figure' in st.session_state.current_chart:
                st.markdown("### 📈 Export Current Chart")
                chart_format = st.selectbox("Chart Format", ["png", "svg", "pdf"], key="chart_format")
                
                if st.button("🎨 Export Chart", use_container_width=True):
                    with st.spinner("Exporting chart..."):
                        export_result = st.session_state.export_manager.export_chart(
                            st.session_state.current_chart['figure'], chart_format
                        )
                        
                        if 'error' not in export_result:
                            b64 = base64.b64encode(export_result['data']).decode()
                            href = f'<a href="data:{export_result["mime_type"]};base64,{b64}" download="{export_result["filename"]}">Click here to download your chart</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            st.success("✅ Chart export ready!")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; padding: 20px;">⚡ Powered by Advanced AI | Built with Streamlit | © 2026 AI BI Dashboard</div>',
    unsafe_allow_html=True
)
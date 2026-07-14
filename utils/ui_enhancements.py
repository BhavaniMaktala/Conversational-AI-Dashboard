# utils/ui_enhancements.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import base64
from typing import List, Dict, Any, Optional

class ModernUI:
    """Modern UI components for enhanced user experience"""
    
    @staticmethod
    def animated_metric_card(title: str, value: Any, icon: str, delta: Optional[float] = None,
                             color: str = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"):
        """Create an animated metric card"""
        
        card_html = f"""
        <div style="
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            animation: slideIn 0.5s ease-out;
            border: 1px solid rgba(102,126,234,0.2);
            margin: 10px 0;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: {color};
                animation: shimmer 2s infinite;
            "></div>
            
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem; background: {color}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {icon}
            </div>
            
            <div style="font-size: 2rem; font-weight: 700; color: #2c3e50; margin: 0.5rem 0;">
                {value:, if isinstance(value, (int, float)) else value}
            </div>
            
            <div style="font-size: 0.9rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">
                {title}
            </div>
            
            {f'<div style="margin-top: 0.5rem; color: {"#10b981" if delta > 0 else "#ef4444"}; font-size: 0.9rem;">{"▲" if delta > 0 else "▼"} {abs(delta)}%</div>' if delta else ''}
        </div>
        
        <style>
            @keyframes slideIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            @keyframes shimmer {{
                0% {{ transform: translateX(-100%); }}
                100% {{ transform: translateX(100%); }}
            }}
            
            div[class*="metric-card"]:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 15px rgba(102,126,234,0.3);
            }}
        </style>
        """
        
        return card_html
    
    @staticmethod
    def gradient_button(text: str, icon: str = "🚀", key: str = None):
        """Create a modern gradient button"""
        
        button_html = f"""
        <style>
            .gradient-btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                color: white;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 30px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102,126,234,0.4);
                width: 100%;
                font-weight: 500;
            }}
            
            .gradient-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(102,126,234,0.6);
            }}
            
            .gradient-btn:active {{
                transform: translateY(0);
            }}
        </style>
        
        <button class="gradient-btn" onclick="this.blur();">
            {icon} {text}
        </button>
        """
        
        return button_html
    
    @staticmethod
    def glassmorphism_card(content: str, title: str = None, width: str = "100%"):
        """Create a glassmorphism style card"""
        
        card_html = f"""
        <div style="
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.18);
            width: {width};
            margin: 10px 0;
            animation: fadeIn 0.5s ease-out;
        ">
            {f'<h3 style="color: #2c3e50; margin-bottom: 1rem; font-weight: 600;">{title}</h3>' if title else ''}
            {content}
        </div>
        
        <style>
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: scale(0.95); }}
                to {{ opacity: 1; transform: scale(1); }}
            }}
        </style>
        """
        
        return card_html
    
    @staticmethod
    def modern_tabs(tabs: List[str], icons: List[str] = None):
        """Create modern animated tabs"""
        
        if icons is None:
            icons = ["📊"] * len(tabs)
        
        tabs_html = ""
        for i, (tab, icon) in enumerate(zip(tabs, icons)):
            active_class = "active" if i == 0 else ""
            tabs_html += f"""
            <button class="modern-tab {active_class}" onclick="switchTab({i})">
                {icon} {tab}
            </button>
            """
        
        html = f"""
        <style>
            .modern-tabs-container {{
                background: white;
                padding: 0.5rem;
                border-radius: 15px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                display: flex;
                gap: 8px;
                margin-bottom: 20px;
                animation: slideDown 0.3s ease-out;
            }}
            
            .modern-tab {{
                flex: 1;
                padding: 10px 20px;
                border: none;
                background: transparent;
                border-radius: 10px;
                color: #64748b;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 1rem;
            }}
            
            .modern-tab:hover {{
                background: rgba(102,126,234,0.1);
                color: #667eea;
            }}
            
            .modern-tab.active {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 4px 10px rgba(102,126,234,0.3);
            }}
            
            @keyframes slideDown {{
                from {{ opacity: 0; transform: translateY(-10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
        
        <div class="modern-tabs-container">
            {tabs_html}
        </div>
        """
        
        return html
    
    @staticmethod
    def loading_animation():
        """Create a modern loading animation"""
        
        html = """
        <style>
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
            
            .loading-text {
                text-align: center;
                color: #667eea;
                font-weight: 500;
                margin-top: 10px;
                animation: pulse 1.5s ease-in-out infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
        </style>
        
        <div class="loader"></div>
        <div class="loading-text">Processing your request...</div>
        """
        
        return html

class DataStoryteller:
    """Create data stories and narratives"""
    
    @staticmethod
    def create_data_story(df: pd.DataFrame, title: str = "Your Data Story") -> str:
        """Generate a narrative from data"""
        
        story_parts = []
        
        # Opening
        story_parts.append(f"# 📊 {title}\n")
        story_parts.append(f"*Generated on {datetime.now().strftime('%B %d, %Y')}*\n")
        
        # Overview
        story_parts.append("## 📈 Overview")
        story_parts.append(f"This dataset contains **{len(df):,} rows** and **{len(df.columns)} columns**. ")
        
        # Key metrics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            story_parts.append("\n## 🔢 Key Metrics")
            for col in numeric_cols[:3]:  # Show top 3 numeric columns
                story_parts.append(f"- **{col}**: Average = {df[col].mean():.2f}, Range = {df[col].min():.2f} to {df[col].max():.2f}")
        
        # Insights
        story_parts.append("\n## 💡 Key Insights")
        
        # Find interesting patterns
        if len(numeric_cols) >= 2:
            corr = df[numeric_cols[0]].corr(df[numeric_cols[1]])
            if abs(corr) > 0.7:
                story_parts.append(f"- Strong {'positive' if corr > 0 else 'negative'} correlation ({corr:.2f}) between **{numeric_cols[0]}** and **{numeric_cols[1]}**")
        
        # Categorical insights
        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols[:2]:
            top_val = df[col].value_counts().index[0]
            top_pct = (df[col].value_counts().iloc[0] / len(df)) * 100
            story_parts.append(f"- Most common **{col}** is '{top_val}' ({top_pct:.1f}% of data)")
        
        # Recommendations
        story_parts.append("\n## 🎯 Recommendations")
        story_parts.append("- Consider creating visualizations to better understand patterns")
        story_parts.append("- Check for outliers that might affect your analysis")
        story_parts.append("- Use filters to focus on specific segments of your data")
        
        return "\n".join(story_parts)
    
    @staticmethod
    def generate_insight_cards(df: pd.DataFrame) -> List[Dict[str, str]]:
        """Generate insight cards for display"""
        
        insights = []
        
        # Data quality insight
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct == 0:
            insights.append({
                'icon': '✅',
                'title': 'Clean Data',
                'description': 'No missing values found! Your data is clean and ready for analysis.',
                'color': '#10b981'
            })
        else:
            insights.append({
                'icon': '⚠️',
                'title': 'Missing Values',
                'description': f'Found {missing_pct:.1f}% missing values. Consider cleaning your data.',
                'color': '#f59e0b'
            })
        
        # Numeric columns insight
        numeric_count = len(df.select_dtypes(include=[np.number]).columns)
        insights.append({
            'icon': '🔢',
            'title': 'Numeric Features',
            'description': f'Your data has {numeric_count} numeric columns for quantitative analysis.',
            'color': '#3b82f6'
        })
        
        # Categorical insight
        cat_count = len(df.select_dtypes(include=['object']).columns)
        if cat_count > 0:
            insights.append({
                'icon': '🏷️',
                'title': 'Categories',
                'description': f'Found {cat_count} categorical columns for grouping and segmentation.',
                'color': '#8b5cf6'
            })
        
        # Size insight
        size_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
        insights.append({
            'icon': '💾',
            'title': 'Data Size',
            'description': f'Dataset size: {size_mb:.2f} MB',
            'color': '#ec4899'
        })
        
        return insights
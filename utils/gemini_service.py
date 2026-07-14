import json
import pandas as pd
from typing import Dict, Any, List, Optional

class GeminiService:
    def __init__(self):
        pass
    
    def interpret_query(self, query: str, columns: List[str], data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Simple rule-based query interpretation"""
        query_lower = query.lower()
        
        result = {
            "intent": "general",
            "chart_type": None,
            "x_axis": None,
            "y_axis": None,
            "aggregation": "count",
            "filter_condition": None,
            "explanation": f"Processing: {query}"
        }
        
        # Check for visualization keywords
        if any(word in query_lower for word in ['pie', 'distribution', 'portion']):
            result['intent'] = 'visualize'
            result['chart_type'] = 'pie'
            if columns:
                result['x_axis'] = columns[0]
        
        elif any(word in query_lower for word in ['bar', 'bars', 'column']):
            result['intent'] = 'visualize'
            result['chart_type'] = 'bar'
            if columns:
                result['x_axis'] = columns[0]
                if len(columns) > 1:
                    result['y_axis'] = columns[1]
        
        elif any(word in query_lower for word in ['line', 'trend', 'over time', 'time series']):
            result['intent'] = 'visualize'
            result['chart_type'] = 'line'
            if columns:
                result['x_axis'] = columns[0]
                if len(columns) > 1:
                    result['y_axis'] = columns[1]
        
        elif any(word in query_lower for word in ['scatter', 'correlation', 'relationship']):
            result['intent'] = 'visualize'
            result['chart_type'] = 'scatter'
            if len(columns) >= 2:
                result['x_axis'] = columns[0]
                result['y_axis'] = columns[1]
        
        elif any(word in query_lower for word in ['histogram', 'distribution of']):
            result['intent'] = 'visualize'
            result['chart_type'] = 'histogram'
            if columns:
                result['x_axis'] = columns[0]
        
        elif any(word in query_lower for word in ['box', 'boxplot']):
            result['intent'] = 'visualize'
            result['chart_type'] = 'box'
            if columns:
                result['x_axis'] = columns[0]
        
        return result
    
    def generate_insights(self, df: pd.DataFrame, chart_data: Dict[str, Any]) -> List[str]:
        """Generate simple insights"""
        insights = []
        
        try:
            if not df.empty:
                # Basic stats
                insights.append(f"📊 Total records: {len(df):,}")
                
                # Numeric insights
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    col = numeric_cols[0]
                    insights.append(f"📈 {col}: Avg = {df[col].mean():.2f}, Min = {df[col].min():.2f}, Max = {df[col].max():.2f}")
                
                # Categorical insights
                cat_cols = df.select_dtypes(include=['object']).columns
                if len(cat_cols) > 0:
                    col = cat_cols[0]
                    top_val = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
                    insights.append(f"🏷️ Most common in {col}: {top_val}")
                
                # Chart-specific insights
                if chart_data and 'type' in chart_data:
                    chart_type = chart_data['type']
                    if chart_type == 'pie':
                        insights.append("🥧 Pie chart shows proportional distribution of categories")
                    elif chart_type == 'bar':
                        insights.append("📊 Bar chart compares values across different categories")
                    elif chart_type == 'line':
                        insights.append("📈 Line chart reveals trends and patterns over time")
                    elif chart_type == 'scatter':
                        insights.append("🔍 Scatter plot shows relationship between two variables")
                    elif chart_type == 'histogram':
                        insights.append("📊 Histogram shows the distribution of a single variable")
            
            # Ensure we have at least 3 insights
            while len(insights) < 3:
                insights.append(f"💡 Tip: Try asking for different chart types or filtering the data")
        
        except Exception as e:
            insights = ["📊 Analysis complete", "📈 Check the visualization above", "💡 Ask more questions"]
        
        return insights[:5]
    
    def generate_response(self, query: str, interpretation: Dict[str, Any], chart_data: Optional[Dict[str, Any]] = None) -> str:
        """Generate simple response"""
        if interpretation['intent'] == 'visualize':
            if chart_data and 'error' not in chart_data:
                return f"✅ I've created a {interpretation['chart_type']} chart showing {interpretation.get('x_axis', 'the data')}!"
            else:
                return f"📊 I'll help you visualize that. Please specify which columns to use."
        else:
            return f"💬 I understand you want to: {query}"
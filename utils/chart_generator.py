import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional, List
import numpy as np

class ChartGenerator:
    @staticmethod
    def generate_chart(df: pd.DataFrame, chart_type: str, x_col: str, y_col: Optional[str] = None, 
                      aggregation: str = "count", title: str = "") -> Dict[str, Any]:
        
        if df.empty:
            return {"error": "No data available"}
        
        # Clean column names for comparison
        x_col = str(x_col).strip() if x_col else ""
        if y_col:
            y_col = str(y_col).strip()
        
        # Validate columns
        if x_col and x_col not in df.columns:
            # Try to find matching column
            for col in df.columns:
                if col.strip() == x_col or col.lower() == x_col.lower():
                    x_col = col
                    break
            else:
                # Use first column as default
                x_col = df.columns[0]
        
        if y_col and y_col not in df.columns:
            for col in df.columns:
                if col.strip() == y_col or col.lower() == y_col.lower():
                    y_col = col
                    break
            else:
                y_col = None
        
        try:
            fig = None
            
            if chart_type == 'pie':
                # For pie chart
                value_counts = df[x_col].value_counts().reset_index()
                value_counts.columns = [x_col, 'count']
                
                fig = px.pie(
                    value_counts,
                    names=x_col,
                    values='count',
                    title=title or f"Distribution by {x_col}",
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                )
                
            elif chart_type == 'bar':
                if y_col and y_col in df.columns and aggregation != "count":
                    # Aggregate by x_col
                    agg_func = {
                        'sum': 'sum',
                        'average': 'mean',
                        'mean': 'mean',
                        'min': 'min',
                        'max': 'max',
                        'count': 'count'
                    }.get(aggregation.lower(), 'sum')
                    
                    aggregated = df.groupby(x_col)[y_col].agg(agg_func).reset_index()
                    fig = px.bar(
                        aggregated,
                        x=x_col,
                        y=y_col,
                        title=title or f"{aggregation.title()} of {y_col} by {x_col}",
                        color_discrete_sequence=['#6366f1'],
                        text=y_col
                    )
                else:
                    # Count occurrences
                    value_counts = df[x_col].value_counts().reset_index()
                    value_counts.columns = [x_col, 'count']
                    fig = px.bar(
                        value_counts,
                        x=x_col,
                        y='count',
                        title=title or f"Count by {x_col}",
                        color_discrete_sequence=['#6366f1'],
                        text='count'
                    )
                
                fig.update_traces(
                    texttemplate='%{text}',
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Value: %{y}<extra></extra>'
                )
                
            elif chart_type == 'line':
                if y_col and y_col in df.columns:
                    # Sort by x for line chart
                    try:
                        df_sorted = df.sort_values(x_col)
                    except:
                        df_sorted = df
                    
                    fig = px.line(
                        df_sorted,
                        x=x_col,
                        y=y_col,
                        title=title or f"Trend of {y_col} over {x_col}",
                        markers=True,
                        color_discrete_sequence=['#6366f1']
                    )
                else:
                    # Count over x
                    try:
                        time_counts = df[x_col].value_counts().sort_index().reset_index()
                    except:
                        time_counts = df[x_col].value_counts().reset_index()
                    time_counts.columns = [x_col, 'count']
                    fig = px.line(
                        time_counts,
                        x=x_col,
                        y='count',
                        title=title or f"Count over {x_col}",
                        markers=True,
                        color_discrete_sequence=['#6366f1']
                    )
                
            elif chart_type == 'scatter':
                if y_col and y_col in df.columns:
                    fig = px.scatter(
                        df,
                        x=x_col,
                        y=y_col,
                        title=title or f"Scatter plot: {y_col} vs {x_col}",
                        trendline="ols",
                        color_discrete_sequence=['#6366f1'],
                        opacity=0.7
                    )
                else:
                    return {"error": "Y-axis column required for scatter plot"}
                
            elif chart_type == 'histogram':
                fig = px.histogram(
                    df,
                    x=x_col,
                    title=title or f"Distribution of {x_col}",
                    nbins=20,
                    color_discrete_sequence=['#6366f1'],
                    marginal="box"
                )
                
            elif chart_type == 'box':
                if y_col and y_col in df.columns:
                    fig = px.box(
                        df,
                        x=x_col,
                        y=y_col,
                        title=title or f"Box plot of {y_col} by {x_col}",
                        color=x_col,
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                else:
                    fig = px.box(
                        df,
                        y=x_col,
                        title=title or f"Box plot of {x_col}",
                        color_discrete_sequence=['#6366f1']
                    )
            
            elif chart_type == 'area':
                if y_col and y_col in df.columns:
                    # Sort by x for area chart
                    try:
                        df_sorted = df.sort_values(x_col)
                    except:
                        df_sorted = df
                    
                    fig = px.area(
                        df_sorted,
                        x=x_col,
                        y=y_col,
                        title=title or f"Area chart of {y_col} over {x_col}",
                        color_discrete_sequence=['#6366f1']
                    )
                else:
                    return {"error": "Y-axis column required for area chart"}
            
            if fig:
                # Update layout
                fig.update_layout(
                    template='plotly_white',
                    hovermode='closest',
                    margin=dict(l=50, r=50, t=50, b=50),
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01,
                        bgcolor='rgba(255,255,255,0.8)'
                    ),
                    title={
                        'text': title or fig.layout.title.text,
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'family': 'Arial, sans-serif'}
                    },
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                return {
                    'type': chart_type,
                    'x_axis': x_col,
                    'y_axis': y_col,
                    'title': title,
                    'figure': fig.to_dict()
                }
            
        except Exception as e:
            return {"error": str(e)}
        
        return {"error": "Failed to generate chart"}
    
    @staticmethod
    def get_column_stats(df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Get statistical summary for a column"""
        if column not in df.columns:
            return {}
        
        try:
            if pd.api.types.is_numeric_dtype(df[column]):
                return {
                    'min': float(df[column].min()),
                    'max': float(df[column].max()),
                    'mean': float(df[column].mean()),
                    'median': float(df[column].median()),
                    'std': float(df[column].std()),
                    'sum': float(df[column].sum())
                }
            else:
                top_values = df[column].value_counts().head(5).to_dict()
                top_values = {str(k): int(v) for k, v in top_values.items()}
                return {
                    'unique_values': int(df[column].nunique()),
                    'most_common': str(df[column].mode().iloc[0]) if not df[column].mode().empty else None,
                    'top_values': top_values
                }
        except:
            return {}
    
    @staticmethod
    def suggest_chart_type(df: pd.DataFrame) -> List[Dict[str, str]]:
        """Suggest chart types based on data"""
        suggestions = []
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if categorical_cols:
            suggestions.append({
                'type': 'pie',
                'description': f'Distribution of {categorical_cols[0]}',
                'x': categorical_cols[0]
            })
            
            if numeric_cols:
                suggestions.append({
                    'type': 'bar',
                    'description': f'{numeric_cols[0]} by {categorical_cols[0]}',
                    'x': categorical_cols[0],
                    'y': numeric_cols[0]
                })
        
        if len(numeric_cols) >= 2:
            suggestions.append({
                'type': 'scatter',
                'description': f'{numeric_cols[1]} vs {numeric_cols[0]}',
                'x': numeric_cols[0],
                'y': numeric_cols[1]
            })
        
        if numeric_cols:
            suggestions.append({
                'type': 'histogram',
                'description': f'Distribution of {numeric_cols[0]}',
                'x': numeric_cols[0]
            })
        
        return suggestions[:4]
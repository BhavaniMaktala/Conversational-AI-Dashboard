# utils/advanced_features.py
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import json
from datetime import datetime, timedelta
import hashlib
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class AdvancedAnalytics:
    """Advanced analytics features for BI dashboard"""
    
    @staticmethod
    def correlation_analysis(df: pd.DataFrame) -> Dict[str, Any]:
        """Perform advanced correlation analysis"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            return {"error": "Need at least 2 numeric columns for correlation analysis"}
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Identify strong correlations
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': corr_value,
                        'strength': 'Very Strong' if abs(corr_value) > 0.9 else 'Strong'
                    })
        
        # Create correlation heatmap
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdBu_r',
            title="Correlation Matrix Heatmap"
        )
        
        fig.update_layout(
            width=600,
            height=500,
            xaxis_title="",
            yaxis_title=""
        )
        
        return {
            'matrix': corr_matrix.to_dict(),
            'strong_correlations': strong_correlations,
            'heatmap': fig.to_dict(),
            'summary': {
                'total_strong_correlations': len(strong_correlations),
                'max_correlation': float(corr_matrix.values.max()),
                'min_correlation': float(corr_matrix.values.min())
            }
        }
    
    @staticmethod
    def time_series_analysis(df: pd.DataFrame, date_col: str, value_col: str) -> Dict[str, Any]:
        """Perform time series analysis"""
        try:
            # Convert to datetime if not already
            df[date_col] = pd.to_datetime(df[date_col])
            df = df.sort_values(date_col)
            
            # Resample to different frequencies
            df.set_index(date_col, inplace=True)
            
            # Calculate moving averages
            df['MA_7'] = df[value_col].rolling(window=7, min_periods=1).mean()
            df['MA_30'] = df[value_col].rolling(window=30, min_periods=1).mean()
            
            # Detect trends
            from scipy import stats
            x = np.arange(len(df))
            y = df[value_col].values
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # Seasonality detection (if enough data)
            seasonality = None
            if len(df) > 30:
                # Simple seasonality check using autocorrelation
                try:
                    from statsmodels.tsa.stattools import acf
                    acf_values = acf(df[value_col].dropna(), nlags=20)
                    seasonality = {
                        'has_seasonality': bool(any(acf_values[1:] > 0.5)),
                        'acf_values': acf_values.tolist() if acf_values is not None else []
                    }
                except:
                    seasonality = {'has_seasonality': False, 'acf_values': []}
            
            # Create visualization
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Time Series with Moving Averages', 'Distribution'),
                vertical_spacing=0.15
            )
            
            # Original data
            fig.add_trace(
                go.Scatter(x=df.index, y=df[value_col], mode='lines', name='Original',
                          line=dict(color='blue', width=1)),
                row=1, col=1
            )
            
            # Moving averages
            fig.add_trace(
                go.Scatter(x=df.index, y=df['MA_7'], mode='lines', name='7-Day MA',
                          line=dict(color='red', width=2)),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=df.index, y=df['MA_30'], mode='lines', name='30-Day MA',
                          line=dict(color='green', width=2)),
                row=1, col=1
            )
            
            # Distribution
            fig.add_trace(
                go.Histogram(x=df[value_col], name='Distribution', nbinsx=30,
                            marker_color='purple'),
                row=2, col=1
            )
            
            fig.update_layout(height=700, showlegend=True, title_text="Time Series Analysis")
            
            return {
                'trend': {
                    'slope': float(slope),
                    'intercept': float(intercept),
                    'r_squared': float(r_value**2),
                    'p_value': float(p_value),
                    'direction': 'Upward' if slope > 0 else 'Downward' if slope < 0 else 'Stable'
                },
                'statistics': {
                    'mean': float(df[value_col].mean()),
                    'std': float(df[value_col].std()),
                    'min': float(df[value_col].min()),
                    'max': float(df[value_col].max()),
                    'volatility': float(df[value_col].std() / df[value_col].mean()) if df[value_col].mean() != 0 else 0
                },
                'seasonality': seasonality,
                'figure': fig.to_dict()
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def predictive_forecast(df: pd.DataFrame, value_col: str, periods: int = 10) -> Dict[str, Any]:
        """Simple predictive forecasting using ARIMA-like approach"""
        try:
            from statsmodels.tsa.holtwinters import ExponentialSmoothing
            from sklearn.metrics import mean_absolute_error, mean_squared_error
            
            # Prepare data
            series = df[value_col].dropna()
            
            if len(series) < 10:
                return {"error": "Need at least 10 data points for forecasting"}
            
            # Simple exponential smoothing
            model = ExponentialSmoothing(
                series,
                seasonal_periods=7 if len(series) > 30 else None,
                trend='add',
                seasonal='add' if len(series) > 30 else None
            )
            
            fitted_model = model.fit()
            
            # Make predictions
            forecast = fitted_model.forecast(periods)
            
            # Calculate confidence intervals (simplified)
            residuals = fitted_model.resid
            std_resid = np.std(residuals)
            confidence_interval = 1.96 * std_resid
            
            # Create visualization
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=series.index, y=series.values,
                mode='lines+markers', name='Historical',
                line=dict(color='blue', width=2)
            ))
            
            # Forecast
            forecast_index = pd.date_range(start=series.index[-1], periods=periods+1, freq='D')[1:]
            fig.add_trace(go.Scatter(
                x=forecast_index, y=forecast.values,
                mode='lines+markers', name='Forecast',
                line=dict(color='red', width=2, dash='dash')
            ))
            
            # Confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_index.tolist() + forecast_index.tolist()[::-1],
                y=(forecast + confidence_interval).tolist() + (forecast - confidence_interval).tolist()[::-1],
                fill='toself',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=True,
                name='95% Confidence Interval'
            ))
            
            fig.update_layout(
                title="Predictive Forecast",
                xaxis_title="Time",
                yaxis_title="Value",
                hovermode='x unified'
            )
            
            return {
                'forecast': forecast.to_dict(),
                'metrics': {
                    'mae': float(mean_absolute_error(series[-10:], fitted_model.fittedvalues[-10:])),
                    'rmse': float(np.sqrt(mean_squared_error(series[-10:], fitted_model.fittedvalues[-10:])))
                },
                'confidence_interval': float(confidence_interval),
                'figure': fig.to_dict()
            }
            
        except Exception as e:
            return {"error": str(e)}

class DataQualityAnalyzer:
    """Analyze data quality and provide recommendations"""
    
    @staticmethod
    def analyze_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive data quality analysis"""
        
        quality_report = {
            'overall_score': 100,
            'issues': [],
            'recommendations': [],
            'detailed_analysis': {}
        }
        
        # Check missing values
        missing_data = df.isnull().sum()
        missing_percentages = (missing_data / len(df)) * 100
        
        columns_with_missing = missing_percentages[missing_percentages > 0].to_dict()
        if columns_with_missing:
            quality_report['issues'].append({
                'type': 'missing_values',
                'description': f"Found missing values in {len(columns_with_missing)} columns",
                'details': columns_with_missing
            })
            quality_report['overall_score'] -= len(columns_with_missing) * 5
        
        # Check data types consistency
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if column should be numeric
                try:
                    pd.to_numeric(df[col], errors='coerce')
                    quality_report['issues'].append({
                        'type': 'data_type',
                        'description': f"Column '{col}' might be numeric but stored as object",
                        'suggestion': 'Convert to numeric type'
                    })
                    quality_report['overall_score'] -= 3
                except:
                    pass
        
        # Check for duplicates
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            quality_report['issues'].append({
                'type': 'duplicates',
                'description': f"Found {duplicate_count} duplicate rows",
                'percentage': (duplicate_count / len(df)) * 100
            })
            quality_report['overall_score'] -= min(duplicate_count * 2, 20)
        
        # Check outliers in numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        outliers = {}
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outlier_count = len(df[(df[col] < lower_bound) | (df[col] > upper_bound)])
            if outlier_count > 0:
                outliers[col] = {
                    'count': int(outlier_count),
                    'percentage': float((outlier_count / len(df)) * 100)
                }
        
        if outliers:
            quality_report['issues'].append({
                'type': 'outliers',
                'description': 'Found outliers in numeric columns',
                'details': outliers
            })
        
        # Generate recommendations
        quality_report['recommendations'] = DataQualityAnalyzer._generate_recommendations(quality_report['issues'])
        
        # Detailed analysis
        quality_report['detailed_analysis'] = {
            'row_count': len(df),
            'column_count': len(df.columns),
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
            'data_types': df.dtypes.astype(str).to_dict(),
            'numeric_columns': len(numeric_cols),
            'categorical_columns': len(df.select_dtypes(include=['object']).columns),
            'datetime_columns': len(df.select_dtypes(include=['datetime64']).columns)
        }
        
        return quality_report
    
    @staticmethod
    def _generate_recommendations(issues: List) -> List[str]:
        """Generate recommendations based on issues"""
        recommendations = []
        
        for issue in issues:
            if issue['type'] == 'missing_values':
                recommendations.append("📊 Consider imputing missing values using mean/median/mode")
                recommendations.append("🔄 Or drop columns with >50% missing values")
            
            elif issue['type'] == 'data_type':
                recommendations.append("🔧 Convert object columns to appropriate data types for better performance")
            
            elif issue['type'] == 'duplicates':
                recommendations.append("🗑️ Remove duplicate rows to avoid skewed analysis")
            
            elif issue['type'] == 'outliers':
                recommendations.append("📈 Review outliers - they might be errors or important anomalies")
        
        if not recommendations:
            recommendations.append("✅ Your data looks clean! Ready for analysis.")
        
        return recommendations[:5]

class ExportManager:
    """Handle data export in various formats"""
    
    @staticmethod
    def export_data(df: pd.DataFrame, format_type: str, filename: str = "export") -> Dict[str, Any]:
        """Export data in different formats"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{timestamp}"
            
            if format_type == 'csv':
                data = df.to_csv(index=False)
                mime_type = 'text/csv'
                extension = 'csv'
            
            elif format_type == 'excel':
                output = pd.ExcelWriter(f"{filename}.xlsx", engine='xlsxwriter')
                df.to_excel(output, index=False, sheet_name='Data')
                output.close()
                with open(f"{filename}.xlsx", 'rb') as f:
                    data = f.read()
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                extension = 'xlsx'
            
            elif format_type == 'json':
                data = df.to_json(orient='records', date_format='iso')
                mime_type = 'application/json'
                extension = 'json'
            
            elif format_type == 'html':
                data = df.to_html(classes='table table-striped', index=False)
                mime_type = 'text/html'
                extension = 'html'
            
            elif format_type == 'markdown':
                data = df.to_markdown(index=False)
                mime_type = 'text/markdown'
                extension = 'md'
            
            else:
                return {"error": f"Unsupported format: {format_type}"}
            
            return {
                'data': data,
                'filename': f"{filename}.{extension}",
                'mime_type': mime_type,
                'format': format_type
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def export_chart(figure: Dict, format_type: str = 'png') -> Dict[str, Any]:
        """Export chart as image"""
        try:
            import plotly.io as pio
            
            fig = go.Figure(figure)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chart_{timestamp}"
            
            if format_type == 'png':
                img_bytes = pio.to_image(fig, format='png')
                mime_type = 'image/png'
                extension = 'png'
            elif format_type == 'svg':
                img_bytes = pio.to_image(fig, format='svg')
                mime_type = 'image/svg+xml'
                extension = 'svg'
            elif format_type == 'pdf':
                img_bytes = pio.to_image(fig, format='pdf')
                mime_type = 'application/pdf'
                extension = 'pdf'
            else:
                return {"error": f"Unsupported format: {format_type}"}
            
            return {
                'data': img_bytes,
                'filename': f"{filename}.{extension}",
                'mime_type': mime_type,
                'format': format_type
            }
            
        except Exception as e:
            return {"error": str(e)}
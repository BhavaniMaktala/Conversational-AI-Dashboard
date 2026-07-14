# utils/insight_engine.py
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class InsightEngine:
    """Advanced insight generation engine"""
    
    @staticmethod
    def discover_patterns(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Discover hidden patterns in data"""
        
        patterns = []
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Pattern 1: Clustering tendency
        if len(numeric_df.columns) >= 2 and len(numeric_df) > 10:
            try:
                # Check if data forms natural clusters
                scaler = StandardScaler()
                scaled_data = scaler.fit_transform(numeric_df.dropna())
                
                # Use PCA to reduce dimensionality for visualization
                pca = PCA(n_components=2)
                pca_result = pca.fit_transform(scaled_data)
                
                # Simple clustering to check patterns
                kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
                clusters = kmeans.fit_predict(scaled_data)
                
                # Check cluster separation
                cluster_sizes = pd.Series(clusters).value_counts()
                if len(cluster_sizes) > 1 and cluster_sizes.min() > len(df) * 0.1:
                    patterns.append({
                        'type': 'clustering',
                        'title': 'Natural Clusters Detected',
                        'description': f'Data naturally forms {len(cluster_sizes)} distinct groups',
                        'confidence': 'High',
                        'details': {
                            'clusters': len(cluster_sizes),
                            'explained_variance': f"{pca.explained_variance_ratio_.sum() * 100:.1f}%"
                        }
                    })
            except:
                pass
        
        # Pattern 2: Outlier detection
        for col in numeric_df.columns[:3]:  # Check first 3 numeric columns
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
            
            if len(outliers) > 0 and len(outliers) < len(df) * 0.1:  # Less than 10% outliers
                patterns.append({
                    'type': 'outliers',
                    'title': f'Outliers in {col}',
                    'description': f'Found {len(outliers)} potential outliers ({len(outliers)/len(df)*100:.1f}% of data)',
                    'confidence': 'Medium',
                    'details': {
                        'column': col,
                        'outlier_count': len(outliers),
                        'typical_range': f"{Q1:.2f} - {Q3:.2f}"
                    }
                })
        
        # Pattern 3: Trend detection
        if len(df) > 10 and len(numeric_df.columns) > 0:
            col = numeric_df.columns[0]
            try:
                # Simple trend detection using linear regression
                from scipy import stats
                x = np.arange(len(df))
                y = df[col].values
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                
                if abs(r_value) > 0.5 and p_value < 0.05:
                    patterns.append({
                        'type': 'trend',
                        'title': f'Significant Trend in {col}',
                        'description': f"{'Increasing' if slope > 0 else 'Decreasing'} trend detected (R² = {r_value**2:.2f})",
                        'confidence': 'High' if r_value**2 > 0.7 else 'Medium',
                        'details': {
                            'column': col,
                            'slope': float(slope),
                            'r_squared': float(r_value**2),
                            'p_value': float(p_value)
                        }
                    })
            except:
                pass
        
        return patterns
    
    @staticmethod
    def generate_business_insights(df: pd.DataFrame) -> List[str]:
        """Generate business-focused insights"""
        
        insights = []
        
        # Performance insights
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            insights.append(f"📈 **Performance Metric**: {col} averages {df[col].mean():.2f}, with peak at {df[col].max():.2f}")
        
        # Distribution insights
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            col = cat_cols[0]
            top_cat = df[col].value_counts().index[0]
            top_pct = (df[col].value_counts().iloc[0] / len(df)) * 100
            insights.append(f"🎯 **Market Share**: '{top_cat}' dominates with {top_pct:.1f}% of the market")
        
        # Growth opportunities
        if len(numeric_cols) >= 2:
            col1, col2 = numeric_cols[0], numeric_cols[1]
            corr = df[col1].corr(df[col2])
            if corr > 0.7:
                insights.append(f"🚀 **Growth Opportunity**: Strong correlation between {col1} and {col2} suggests bundled opportunities")
            elif corr < -0.7:
                insights.append(f"⚖️ **Trade-off Alert**: {col1} and {col2} show strong negative correlation - balance needed")
        
        # Efficiency insights
        if len(df) > 100:
            insights.append(f"⚡ **Scale Efficiency**: Dataset contains {len(df)} records - sufficient for statistical significance")
        
        # Risk insights
        for col in numeric_cols[:2]:
            volatility = df[col].std() / df[col].mean() if df[col].mean() != 0 else 0
            if volatility > 1:
                insights.append(f"⚠️ **Risk Alert**: High volatility in {col} (CV = {volatility:.2f}) - monitor closely")
        
        return insights
    
    @staticmethod
    def smart_recommendations(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Provide smart recommendations based on data"""
        
        recommendations = []
        
        # Data quality recommendations
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct > 10:
            recommendations.append({
                'action': 'Clean Data',
                'reason': f'High missing values ({missing_pct:.1f}%)',
                'impact': 'Improve analysis accuracy',
                'priority': 'High'
            })
        
        # Feature engineering recommendations
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            recommendations.append({
                'action': 'Create Composite Metrics',
                'reason': 'Multiple numeric columns available',
                'impact': 'Discover hidden patterns',
                'priority': 'Medium'
            })
        
        # Visualization recommendations
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0 and len(numeric_cols) > 0:
            recommendations.append({
                'action': 'Build Interactive Dashboard',
                'reason': 'Mix of categorical and numeric data',
                'impact': 'Better decision making',
                'priority': 'High'
            })
        
        # Advanced analytics recommendations
        if len(df) > 1000:
            recommendations.append({
                'action': 'Apply Machine Learning',
                'reason': 'Sufficient data volume for training',
                'impact': 'Predictive capabilities',
                'priority': 'Medium'
            })
        
        return recommendations

class AutomatedReporting:
    """Automated report generation"""
    
    @staticmethod
    def generate_executive_summary(df: pd.DataFrame) -> str:
        """Generate executive summary"""
        
        summary = []
        
        # Header
        summary.append("# 📊 Executive Data Summary\n")
        
        # Key metrics
        summary.append("## Key Metrics")
        summary.append(f"- **Total Records**: {len(df):,}")
        summary.append(f"- **Total Features**: {len(df.columns)}")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        summary.append(f"- **Numeric Features**: {len(numeric_cols)}")
        
        cat_cols = df.select_dtypes(include=['object']).columns
        summary.append(f"- **Categorical Features**: {len(cat_cols)}\n")
        
        # Top findings
        summary.append("## Top Findings")
        
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            summary.append(f"1. **{col}** ranges from {df[col].min():.2f} to {df[col].max():.2f}, averaging {df[col].mean():.2f}")
        
        if len(cat_cols) > 0:
            col = cat_cols[0]
            top_val = df[col].value_counts().index[0]
            summary.append(f"2. **{col}** is predominantly '{top_val}'")
        
        # Recommendations
        summary.append("\n## Recommendations")
        insights = InsightEngine.smart_recommendations(df)
        for i, rec in enumerate(insights[:3], 1):
            summary.append(f"{i}. **{rec['action']}** - {rec['reason']} (Priority: {rec['priority']})")
        
        return "\n".join(summary)
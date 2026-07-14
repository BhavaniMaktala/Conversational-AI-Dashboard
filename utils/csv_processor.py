import pandas as pd
import numpy as np
import hashlib
from datetime import datetime
import os
from typing import Dict, Any, List, Optional

class CSVProcessor:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
        self.sessions = {}
    
    def process_upload(self, file) -> Dict[str, Any]:
        try:
            # Read the file with proper encoding
            content = file.getvalue()
            
            # Try different encodings
            encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    file.seek(0)
                    df = pd.read_csv(file, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
                except Exception:
                    continue
            
            if df is None:
                # Last resort: try with default
                file.seek(0)
                df = pd.read_csv(file)
            
            # Clean column names
            df.columns = [str(col).strip().replace('\x00', '').replace('\n', '').replace('\r', '') for col in df.columns]
            
            # Generate session ID
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_id = hashlib.md5(f"{file.name}{timestamp}".encode()).hexdigest()[:10]
            
            # Handle missing values
            for col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    df[col] = df[col].fillna(df[col].mean() if not df[col].isna().all() else 0)
                else:
                    df[col] = df[col].fillna('Unknown')
            
            # Store in session
            self.sessions[session_id] = {
                'df': df,
                'filename': file.name,
                'upload_time': datetime.now(),
                'history': []
            }
            
            # Prepare response
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            return {
                'session_id': session_id,
                'filename': file.name,
                'columns': df.columns.tolist(),
                'row_count': len(df),
                'col_count': len(df.columns),
                'numeric_cols': numeric_cols,
                'categorical_cols': categorical_cols,
                'summary': self.get_data_summary(df),
                'dtypes': df.dtypes.astype(str).to_dict(),
                'sample_data': df.head(5).to_dict('records')
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        summary = {}
        for col in df.columns:
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    summary[col] = {
                        'type': 'numeric',
                        'min': float(df[col].min()) if not pd.isna(df[col].min()) else 0,
                        'max': float(df[col].max()) if not pd.isna(df[col].max()) else 0,
                        'mean': float(df[col].mean()) if not pd.isna(df[col].mean()) else 0,
                        'median': float(df[col].median()) if not pd.isna(df[col].median()) else 0,
                        'std': float(df[col].std()) if not pd.isna(df[col].std()) else 0,
                        'sum': float(df[col].sum()) if not pd.isna(df[col].sum()) else 0
                    }
                else:
                    value_counts = df[col].value_counts().head(5).to_dict()
                    value_counts = {str(k): int(v) for k, v in value_counts.items()}
                    summary[col] = {
                        'type': 'categorical',
                        'unique_values': int(df[col].nunique()),
                        'top_values': value_counts,
                        'most_common': str(df[col].mode().iloc[0]) if not df[col].mode().empty else None
                    }
            except:
                summary[col] = {'type': 'unknown'}
        return summary
    
    def get_session_data(self, session_id: str) -> Optional[pd.DataFrame]:
        if session_id in self.sessions:
            return self.sessions[session_id]['df'].copy()
        return None

    def apply_filter(self, session_id: str, column: str, values: List) -> Optional[pd.DataFrame]:
        if session_id in self.sessions:
            df = self.sessions[session_id]['df']
            if column in df.columns:
                return df[df[column].isin(values)]
        return None
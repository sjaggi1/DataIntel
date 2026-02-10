import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta

class AnomalyDetector:
    """Detects anomalies and outliers in data"""
    
    def __init__(self):
        self.threshold_zscore = 3
        self.threshold_iqr = 1.5
    
    def detect_anomalies(self, df):
        """Comprehensive anomaly detection"""
        anomalies = []
        
        # Statistical outliers
        anomalies.extend(self._detect_statistical_outliers(df))
        
        # Impossible values
        anomalies.extend(self._detect_impossible_values(df))
        
        # Duplicate detection
        anomalies.extend(self._detect_duplicates(df))
        
        # Sudden spikes
        anomalies.extend(self._detect_spikes(df))
        
        # Data consistency issues
        anomalies.extend(self._detect_inconsistencies(df))
        
        return anomalies
    
    def _detect_statistical_outliers(self, df):
        """Detect statistical outliers using Z-score and IQR"""
        anomalies = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            # Skip if column has too many nulls
            if df[col].isnull().sum() / len(df) > 0.5:
                continue
            
            # Z-score method
            z_scores = np.abs(stats.zscore(df[col].dropna()))
            outliers_z = np.where(z_scores > self.threshold_zscore)[0]
            
            # IQR method
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers_iqr = df[(df[col] < (Q1 - self.threshold_iqr * IQR)) | 
                             (df[col] > (Q3 + self.threshold_iqr * IQR))].index.tolist()
            
            if len(outliers_z) > 0 or len(outliers_iqr) > 0:
                # Combine both methods
                outlier_indices = list(set(outliers_z.tolist() + outliers_iqr))
                
                if outlier_indices:
                    mean_val = df[col].mean()
                    outlier_vals = df.iloc[outlier_indices][col].values
                    
                    # Calculate severity
                    max_deviation = max(abs(outlier_vals - mean_val))
                    severity = 'High' if max_deviation > 3 * df[col].std() else 'Medium'
                    
                    anomalies.append({
                        'type': 'Statistical Outlier',
                        'column': col,
                        'severity': severity,
                        'message': f'Found {len(outlier_indices)} outliers in {col}',
                        'details': f'Values significantly differ from mean ({mean_val:.2f})',
                        'affected_rows': outlier_indices
                    })
        
        return anomalies
    
    def _detect_impossible_values(self, df):
        """Detect logically impossible values"""
        anomalies = []
        
        # Check for negative values in columns that shouldn't be negative
        possible_positive_cols = [col for col in df.columns if any(
            keyword in col.lower() for keyword in ['salary', 'age', 'price', 'count', 'amount']
        )]
        
        for col in possible_positive_cols:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                negative_count = (df[col] < 0).sum()
                
                if negative_count > 0:
                    anomalies.append({
                        'type': 'Impossible Value',
                        'column': col,
                        'severity': 'High',
                        'message': f'Found {negative_count} negative values in {col}',
                        'details': f'{col} should not contain negative values',
                        'affected_rows': df[df[col] < 0].index.tolist()
                    })
        
        # Check for future dates in joining/birth date columns
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        
        for col in date_cols:
            try:
                date_series = pd.to_datetime(df[col], errors='coerce')
                future_dates = date_series > pd.Timestamp.now()
                
                if future_dates.sum() > 0:
                    anomalies.append({
                        'type': 'Impossible Date',
                        'column': col,
                        'severity': 'High',
                        'message': f'Found {future_dates.sum()} future dates in {col}',
                        'details': 'Dates are in the future',
                        'affected_rows': df[future_dates].index.tolist()
                    })
            except:
                pass
        
        # Check for unrealistic age values
        age_cols = [col for col in df.columns if 'age' in col.lower()]
        
        for col in age_cols:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                unrealistic = (df[col] < 18) | (df[col] > 100)
                
                if unrealistic.sum() > 0:
                    anomalies.append({
                        'type': 'Unrealistic Value',
                        'column': col,
                        'severity': 'Medium',
                        'message': f'Found {unrealistic.sum()} unrealistic age values in {col}',
                        'details': 'Ages are outside typical working range (18-100)',
                        'affected_rows': df[unrealistic].index.tolist()
                    })
        
        return anomalies
    
    def _detect_duplicates(self, df):
        """Detect duplicate records"""
        anomalies = []
        
        # Full row duplicates
        duplicates = df.duplicated()
        dup_count = duplicates.sum()
        
        if dup_count > 0:
            anomalies.append({
                'type': 'Duplicate Records',
                'column': 'All columns',
                'severity': 'Medium',
                'message': f'Found {dup_count} duplicate records',
                'details': 'Complete row duplicates detected',
                'affected_rows': df[duplicates].index.tolist()
            })
        
        # Check for duplicate phone numbers
        phone_cols = [col for col in df.columns if 'phone' in col.lower()]
        
        for col in phone_cols:
            if col in df.columns:
                dups = df[col].duplicated(keep=False)
                dup_count = dups.sum()
                
                if dup_count > 0:
                    anomalies.append({
                        'type': 'Duplicate Values',
                        'column': col,
                        'severity': 'Low',
                        'message': f'Found {dup_count} duplicate phone numbers',
                        'details': 'Same phone number used by multiple records',
                        'affected_rows': df[dups].index.tolist()
                    })
        
        # Check for duplicate emails
        email_cols = [col for col in df.columns if 'email' in col.lower()]
        
        for col in email_cols:
            if col in df.columns:
                dups = df[col].duplicated(keep=False)
                dup_count = dups.sum()
                
                if dup_count > 0:
                    anomalies.append({
                        'type': 'Duplicate Values',
                        'column': col,
                        'severity': 'Medium',
                        'message': f'Found {dup_count} duplicate email addresses',
                        'details': 'Same email used by multiple records',
                        'affected_rows': df[dups].index.tolist()
                    })
        
        return anomalies
    
    def _detect_spikes(self, df):
        """Detect sudden spikes in numeric columns"""
        anomalies = []
        
        # Look for date columns to detect time-based spikes
        date_cols = df.select_dtypes(include=['datetime64']).columns
        
        if len(date_cols) > 0:
            date_col = date_cols[0]
            
            # Group by date and count
            daily_counts = df.groupby(pd.Grouper(key=date_col, freq='D')).size()
            
            if len(daily_counts) > 3:
                # Calculate rolling average
                rolling_avg = daily_counts.rolling(window=3, center=True).mean()
                
                # Detect spikes (more than 2x rolling average)
                spikes = daily_counts > (2 * rolling_avg)
                
                if spikes.sum() > 0:
                    spike_dates = daily_counts[spikes].index.tolist()
                    
                    anomalies.append({
                        'type': 'Activity Spike',
                        'column': date_col,
                        'severity': 'Medium',
                        'message': f'Detected {spikes.sum()} unusual activity spikes',
                        'details': f'Activity levels more than 2x normal on certain dates',
                        'affected_rows': []
                    })
        
        return anomalies
    
    def _detect_inconsistencies(self, df):
        """Detect data inconsistencies"""
        anomalies = []
        
        # Check for inconsistent formatting in text columns
        text_cols = df.select_dtypes(include=['object']).columns
        
        for col in text_cols:
            if df[col].dtype == 'object':
                # Check case inconsistency
                values = df[col].dropna().astype(str)
                
                if len(values) > 0:
                    # Count different case versions of same value
                    lower_values = values.str.lower()
                    original_unique = values.nunique()
                    lower_unique = lower_values.nunique()
                    
                    if original_unique > lower_unique:
                        diff = original_unique - lower_unique
                        
                        anomalies.append({
                            'type': 'Inconsistent Formatting',
                            'column': col,
                            'severity': 'Low',
                            'message': f'Found {diff} case inconsistencies in {col}',
                            'details': 'Same values with different capitalization',
                            'affected_rows': []
                        })
        
        # Check for salary jumps (if salary column exists)
        salary_cols = [col for col in df.columns if 'salary' in col.lower()]
        
        for col in salary_cols:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                mean_salary = df[col].mean()
                high_salaries = df[df[col] > 10 * mean_salary]
                
                if len(high_salaries) > 0:
                    anomalies.append({
                        'type': 'Extreme Value',
                        'column': col,
                        'severity': 'High',
                        'message': f'{len(high_salaries)} employees have salary 10x higher than average',
                        'details': f'Average salary: ${mean_salary:,.2f}',
                        'affected_rows': high_salaries.index.tolist()
                    })
        
        return anomalies
    
    def get_anomaly_summary(self, anomalies):
        """Summarize detected anomalies"""
        if not anomalies:
            return "No anomalies detected"
        
        summary = {
            'total': len(anomalies),
            'by_severity': {},
            'by_type': {}
        }
        
        for anomaly in anomalies:
            severity = anomaly['severity']
            atype = anomaly['type']
            
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            summary['by_type'][atype] = summary['by_type'].get(atype, 0) + 1
        
        return summary


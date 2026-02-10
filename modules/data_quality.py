import pandas as pd
import numpy as np

class DataQualityChecker:
    """Calculates comprehensive data quality scores"""
    
    def calculate_scores(self, df):
        """Calculate all quality metrics"""
        return {
            'completeness': self._calculate_completeness(df),
            'consistency': self._calculate_consistency(df),
            'duplicate_risk': self._calculate_duplicate_risk(df),
            'anomaly_risk': self._calculate_anomaly_risk(df),
            'validity': self._calculate_validity(df),
            'accuracy_estimate': self._estimate_accuracy(df)
        }
    
    def _calculate_completeness(self, df):
        """Calculate completeness score (percentage of non-null values)"""
        total_cells = df.size
        non_null_cells = df.count().sum()
        
        completeness = (non_null_cells / total_cells) * 100
        return round(completeness, 2)
    
    def _calculate_consistency(self, df):
        """Calculate consistency score"""
        score = 100
        
        # Check for consistent data types
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if numeric values are mixed with text
                try:
                    numeric_count = pd.to_numeric(df[col], errors='coerce').notna().sum()
                    total_count = df[col].notna().sum()
                    
                    if 0 < numeric_count < total_count:
                        # Mixed types detected
                        penalty = (numeric_count / total_count) * 10
                        score -= penalty
                except:
                    pass
        
        # Check for consistent formatting in text columns
        text_cols = df.select_dtypes(include=['object']).columns
        
        for col in text_cols:
            values = df[col].dropna().astype(str)
            
            if len(values) > 0:
                # Check case consistency
                lower_unique = values.str.lower().nunique()
                original_unique = values.nunique()
                
                if original_unique > lower_unique:
                    # Case inconsistency
                    inconsistency_ratio = (original_unique - lower_unique) / original_unique
                    score -= inconsistency_ratio * 5
        
        return max(0, round(score, 2))
    
    def _calculate_duplicate_risk(self, df):
        """Calculate duplicate risk level"""
        duplicate_count = df.duplicated().sum()
        total_rows = len(df)
        
        if total_rows == 0:
            return "N/A"
        
        duplicate_ratio = duplicate_count / total_rows
        
        if duplicate_ratio == 0:
            return "Low"
        elif duplicate_ratio < 0.05:
            return "Medium"
        else:
            return "High"
    
    def _calculate_anomaly_risk(self, df):
        """Calculate anomaly risk level"""
        risk_score = 0
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            # Calculate z-scores
            try:
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers = (z_scores > 3).sum()
                
                if outliers > 0:
                    risk_score += outliers / len(df)
            except:
                pass
        
        # Normalize risk score
        if risk_score == 0:
            return "Low"
        elif risk_score < 0.05:
            return "Medium"
        else:
            return "High"
    
    def _calculate_validity(self, df):
        """Calculate validity score (percentage of valid values)"""
        score = 100
        
        # Check for invalid email addresses
        email_cols = [col for col in df.columns if 'email' in col.lower()]
        
        for col in email_cols:
            if col in df.columns:
                valid_emails = df[col].astype(str).str.match(
                    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                ).sum()
                total = df[col].notna().sum()
                
                if total > 0:
                    validity_ratio = valid_emails / total
                    score -= (1 - validity_ratio) * 10
        
        # Check for invalid phone numbers
        phone_cols = [col for col in df.columns if 'phone' in col.lower()]
        
        for col in phone_cols:
            if col in df.columns:
                valid_phones = df[col].astype(str).str.match(
                    r'^[\d\s\-\+\(\)]{10,}$'
                ).sum()
                total = df[col].notna().sum()
                
                if total > 0:
                    validity_ratio = valid_phones / total
                    score -= (1 - validity_ratio) * 10
        
        return max(0, round(score, 2))
    
    def _estimate_accuracy(self, df):
        """Estimate data accuracy"""
        # This is a rough estimate based on various factors
        score = 100
        
        # Penalize for missing values
        completeness = self._calculate_completeness(df)
        score = score * (completeness / 100)
        
        # Penalize for duplicates
        duplicate_ratio = df.duplicated().sum() / len(df) if len(df) > 0 else 0
        score -= duplicate_ratio * 20
        
        # Penalize for outliers
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        outlier_ratio = 0
        for col in numeric_cols:
            try:
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers = (z_scores > 3).sum()
                outlier_ratio += outliers / len(df)
            except:
                pass
        
        if len(numeric_cols) > 0:
            outlier_ratio /= len(numeric_cols)
        
        score -= outlier_ratio * 15
        
        return max(0, round(score, 2))
    
    def generate_report(self, df):
        """Generate comprehensive quality report"""
        scores = self.calculate_scores(df)
        
        report = {
            'overall_score': round(np.mean([
                scores['completeness'],
                scores['consistency'],
                scores['validity'],
                scores['accuracy_estimate']
            ]), 2),
            'scores': scores,
            'recommendations': self._generate_recommendations(df, scores)
        }
        
        return report
    
    def _generate_recommendations(self, df, scores):
        """Generate recommendations for improving data quality"""
        recommendations = []
        
        if scores['completeness'] < 90:
            missing_cols = df.columns[df.isnull().any()].tolist()
            recommendations.append({
                'priority': 'High',
                'issue': 'Low completeness',
                'recommendation': f'Fill missing values in columns: {", ".join(missing_cols[:5])}'
            })
        
        if scores['consistency'] < 85:
            recommendations.append({
                'priority': 'Medium',
                'issue': 'Inconsistent formatting',
                'recommendation': 'Standardize text formatting and data types'
            })
        
        if scores['duplicate_risk'] in ['Medium', 'High']:
            recommendations.append({
                'priority': 'High',
                'issue': 'Duplicate records detected',
                'recommendation': 'Review and remove duplicate entries'
            })
        
        if scores['anomaly_risk'] in ['Medium', 'High']:
            recommendations.append({
                'priority': 'Medium',
                'issue': 'Anomalies detected',
                'recommendation': 'Investigate and validate outlier values'
            })
        
        if scores['validity'] < 90:
            recommendations.append({
                'priority': 'High',
                'issue': 'Invalid data values',
                'recommendation': 'Validate email addresses and phone numbers'
            })
        
        return recommendations
    
    def get_column_quality(self, df, column):
        """Get quality metrics for a specific column"""
        col_data = df[column]
        
        metrics = {
            'completeness': round((col_data.notna().sum() / len(df)) * 100, 2),
            'uniqueness': round((col_data.nunique() / len(df)) * 100, 2),
            'data_type': str(col_data.dtype)
        }
        
        if pd.api.types.is_numeric_dtype(col_data):
            metrics['mean'] = round(col_data.mean(), 2)
            metrics['median'] = round(col_data.median(), 2)
            metrics['std'] = round(col_data.std(), 2)
            metrics['outliers'] = self._count_outliers(col_data)
        
        return metrics
    
    def _count_outliers(self, series):
        """Count outliers in a numeric series"""
        try:
            z_scores = np.abs((series - series.mean()) / series.std())
            return (z_scores > 3).sum()
        except:
            return 0

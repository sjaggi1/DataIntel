import pandas as pd
import hashlib
import re
import random
import string

class DataMasker:
    """Handles sensitive data masking and protection"""
    
    def __init__(self):
        self.sensitive_patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
            'ssn': r'^\d{3}-\d{2}-\d{4}$',
            'credit_card': r'^\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}$',
            'aadhaar': r'^\d{4}\s\d{4}\s\d{4}$',
            'pan': r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        }
    
    def detect_sensitive_columns(self, df):
        """Automatically detect potentially sensitive columns"""
        sensitive_cols = []
        
        for col in df.columns:
            col_lower = col.lower()
            
            # Check column name patterns
            sensitivity_keywords = {
                'email': ['email', 'e-mail', 'mail'],
                'phone': ['phone', 'mobile', 'contact', 'cell'],
                'ssn': ['ssn', 'social security'],
                'aadhaar': ['aadhaar', 'aadhar'],
                'pan': ['pan'],
                'salary': ['salary', 'compensation', 'pay'],
                'address': ['address', 'location', 'residence'],
                'dob': ['dob', 'birth', 'birthday']
            }
            
            for stype, keywords in sensitivity_keywords.items():
                if any(keyword in col_lower for keyword in keywords):
                    # Sample data to verify
                    confidence = self._verify_sensitivity(df[col], stype)
                    
                    if confidence > 50:
                        sensitive_cols.append({
                            'column': col,
                            'type': stype,
                            'confidence': confidence
                        })
                    break
        
        return sensitive_cols
    
    def _verify_sensitivity(self, series, data_type):
        """Verify if column contains sensitive data by sampling"""
        sample = series.dropna().head(10).astype(str)
        
        if len(sample) == 0:
            return 0
        
        matches = 0
        
        if data_type in self.sensitive_patterns:
            pattern = self.sensitive_patterns[data_type]
            
            for value in sample:
                if re.match(pattern, value):
                    matches += 1
        else:
            # For other types, just check keywords
            return 70
        
        confidence = (matches / len(sample)) * 100
        return round(confidence, 2)
    
    def apply_masking(self, series, method='Partial Mask'):
        """Apply masking to a series"""
        if method == 'Partial Mask':
            return series.apply(self._partial_mask)
        elif method == 'Full Mask':
            return series.apply(self._full_mask)
        elif method == 'Hash':
            return series.apply(self._hash_value)
        elif method == 'Tokenize':
            return series.apply(self._tokenize)
        else:
            return series
    
    def _partial_mask(self, value):
        """Partially mask a value"""
        if pd.isna(value):
            return value
        
        value_str = str(value)
        
        # Email masking: keep first 2 chars and domain
        if '@' in value_str:
            local, domain = value_str.split('@')
            if len(local) > 2:
                masked_local = local[:2] + '*' * (len(local) - 2)
                return f"{masked_local}@{domain}"
            return value_str
        
        # Phone number masking: show last 4 digits
        if value_str.replace('-', '').replace(' ', '').replace('+', '').isdigit():
            clean_num = value_str.replace('-', '').replace(' ', '').replace('+', '')
            if len(clean_num) >= 4:
                return '*' * (len(clean_num) - 4) + clean_num[-4:]
            return value_str
        
        # General masking: show first and last 2 chars
        if len(value_str) > 4:
            return value_str[:2] + '*' * (len(value_str) - 4) + value_str[-2:]
        
        return '*' * len(value_str)
    
    def _full_mask(self, value):
        """Fully mask a value"""
        if pd.isna(value):
            return value
        
        return '*' * len(str(value))
    
    def _hash_value(self, value):
        """Hash a value using SHA-256"""
        if pd.isna(value):
            return value
        
        return hashlib.sha256(str(value).encode()).hexdigest()[:16]
    
    def _tokenize(self, value):
        """Replace value with random token"""
        if pd.isna(value):
            return value
        
        # Generate consistent token based on hash
        hash_val = hashlib.md5(str(value).encode()).hexdigest()[:8]
        return f"TOKEN_{hash_val}"
    
    def mask_dataframe(self, df, column_methods):
        """Mask multiple columns in dataframe
        
        Args:
            df: DataFrame to mask
            column_methods: Dict mapping column names to masking methods
        """
        masked_df = df.copy()
        
        for col, method in column_methods.items():
            if col in masked_df.columns:
                masked_df[col] = self.apply_masking(masked_df[col], method)
        
        return masked_df
    
    def create_synthetic_data(self, series, count=None):
        """Generate synthetic data that preserves statistical properties"""
        if count is None:
            count = len(series)
        
        series_clean = series.dropna()
        
        if len(series_clean) == 0:
            return pd.Series([None] * count)
        
        if pd.api.types.is_numeric_dtype(series_clean):
            # Generate numeric synthetic data
            mean = series_clean.mean()
            std = series_clean.std()
            
            synthetic = np.random.normal(mean, std, count)
            
            # Ensure same data type
            if series_clean.dtype == 'int64':
                synthetic = synthetic.astype(int)
            
            return pd.Series(synthetic)
        
        else:
            # For categorical, sample with replacement
            return pd.Series(random.choices(series_clean.tolist(), k=count))
    
    def anonymize_personally_identifiable_info(self, df):
        """Automatically detect and anonymize PII"""
        pii_columns = self.detect_sensitive_columns(df)
        
        masked_df = df.copy()
        masking_applied = []
        
        for col_info in pii_columns:
            col = col_info['column']
            
            # Determine appropriate masking method based on type
            if col_info['type'] == 'email':
                method = 'Partial Mask'
            elif col_info['type'] in ['ssn', 'aadhaar', 'pan', 'credit_card']:
                method = 'Hash'
            elif col_info['type'] == 'phone':
                method = 'Partial Mask'
            else:
                method = 'Partial Mask'
            
            masked_df[col] = self.apply_masking(masked_df[col], method)
            masking_applied.append({
                'column': col,
                'type': col_info['type'],
                'method': method
            })
        
        return masked_df, masking_applied
    
    def create_data_subset_for_testing(self, df, sample_size=100, mask_pii=True):
        """Create a safe subset of data for testing"""
        # Sample data
        if len(df) > sample_size:
            subset = df.sample(n=sample_size, random_state=42)
        else:
            subset = df.copy()
        
        # Mask PII if requested
        if mask_pii:
            subset, _ = self.anonymize_personally_identifiable_info(subset)
        
        return subset

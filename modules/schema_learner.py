import pandas as pd
import re
from collections import Counter

class SchemaLearner:
    """Automatically learns data schema from raw data"""
    
    def learn_schema(self, text):
        """Detect and learn schema from text data"""
        schema = {
            'detected_fields': [],
            'field_types': {},
            'delimiters': [],
            'structure': 'unknown',
            'confidence': 0.0
        }
        
        lines = text.strip().split('\n')[:10]  # Analyze first 10 lines
        
        if not lines:
            return schema
        
        # Detect delimiters
        delimiter_counts = {
            ',': sum(line.count(',') for line in lines),
            ';': sum(line.count(';') for line in lines),
            ':': sum(line.count(':') for line in lines),
            '\t': sum(line.count('\t') for line in lines),
            '|': sum(line.count('|') for line in lines)
        }
        
        schema['delimiters'] = [k for k, v in delimiter_counts.items() if v > 0]
        
        # Detect structure
        if '|' in schema['delimiters']:
            schema['structure'] = 'table'
        elif ':' in lines[0] and ':' in lines[1]:
            schema['structure'] = 'key-value'
        else:
            schema['structure'] = 'tabular'
        
        # Detect fields (from first line)
        primary_delimiter = max(delimiter_counts, key=delimiter_counts.get)
        
        if delimiter_counts[primary_delimiter] > 0:
            fields = lines[0].split(primary_delimiter)
            schema['detected_fields'] = [f.strip() for f in fields]
            
            # Detect field types from second line
            if len(lines) > 1:
                values = lines[1].split(primary_delimiter)
                
                for i, (field, value) in enumerate(zip(schema['detected_fields'], values)):
                    schema['field_types'][field] = self._detect_type(value.strip())
        
        # Calculate confidence
        if schema['detected_fields']:
            schema['confidence'] = min(100, len(schema['detected_fields']) * 10)
        
        return schema
    
    def _detect_type(self, value):
        """Detect data type of a value"""
        value = value.strip()
        
        # Check for empty
        if not value:
            return 'string'
        
        # Check for date patterns
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY or MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value):
                return 'date'
        
        # Check for number
        try:
            float(value.replace(',', ''))
            return 'number'
        except ValueError:
            pass
        
        # Check for email
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            return 'email'
        
        # Check for phone
        if re.match(r'^[\d\s\-\+\(\)]+$', value) and len(value) >= 10:
            return 'phone'
        
        # Check for boolean
        if value.lower() in ['true', 'false', 'yes', 'no', '1', '0']:
            return 'boolean'
        
        # Default to string
        return 'string'
    
    def suggest_column_names(self, detected_fields):
        """Suggest clean column names"""
        suggestions = []
        
        for field in detected_fields:
            # Clean and normalize
            clean = field.strip().lower()
            
            # Remove special characters
            clean = re.sub(r'[^\w\s]', '', clean)
            
            # Replace spaces with underscores
            clean = clean.replace(' ', '_')
            
            # Capitalize first letter
            clean = clean.title().replace('_', ' ')
            
            suggestions.append(clean)
        
        return suggestions
    
    def detect_relationships(self, df):
        """Detect potential relationships between columns"""
        relationships = []
        
        columns = df.columns.tolist()
        
        # Check for potential foreign keys
        for i, col1 in enumerate(columns):
            for col2 in columns[i+1:]:
                # Check if one column's values are subset of another
                if df[col1].dtype == df[col2].dtype:
                    unique1 = set(df[col1].dropna().unique())
                    unique2 = set(df[col2].dropna().unique())
                    
                    if unique1.issubset(unique2) and len(unique1) < len(unique2):
                        relationships.append({
                            'type': 'subset',
                            'child': col1,
                            'parent': col2,
                            'confidence': len(unique1) / len(unique2)
                        })
        
        return relationships
    
    def infer_primary_key(self, df):
        """Infer which column might be a primary key"""
        candidates = []
        
        for col in df.columns:
            # Check uniqueness
            if df[col].nunique() == len(df):
                # Check if it looks like an ID
                is_numeric = pd.api.types.is_numeric_dtype(df[col])
                has_id_name = 'id' in col.lower() or 'key' in col.lower()
                
                score = 0
                if is_numeric:
                    score += 50
                if has_id_name:
                    score += 50
                
                candidates.append({
                    'column': col,
                    'score': score
                })
        
        if candidates:
            # Return highest scoring candidate
            return max(candidates, key=lambda x: x['score'])['column']
        
        return None

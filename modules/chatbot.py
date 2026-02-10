import pandas as pd
import numpy as np
from datetime import datetime

class ChatbotAssistant:
    """AI chatbot for data queries and insights"""
    
    def __init__(self):
        self.context = []
    
    def generate_response(self, query, df, intent_info):
        """Generate response based on user query and detected intent"""
        if df is None:
            return "Please upload data first before I can help you analyze it."
        
        intent = intent_info.get('primary_intent', 'general_query')
        
        # Route to appropriate handler
        if intent == 'summary':
            return self._handle_summary(df)
        elif intent == 'aggregate':
            return self._handle_aggregate(query, df, intent_info)
        elif intent == 'filter':
            return self._handle_filter(query, df)
        elif intent == 'trend':
            return self._handle_trend(df)
        elif intent == 'anomaly':
            return self._handle_anomaly_query(df)
        elif intent == 'quality':
            return self._handle_quality_query(df)
        else:
            return self._handle_general_query(query, df)
    
    def _handle_summary(self, df):
        """Generate data summary"""
        summary_parts = []
        
        summary_parts.append(f"📊 **Dataset Summary**\n")
        summary_parts.append(f"- Total Records: {len(df):,}")
        summary_parts.append(f"- Total Columns: {len(df.columns)}")
        
        # Numeric columns summary
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            summary_parts.append(f"\n**Numeric Columns:** {len(numeric_cols)}")
            
            for col in numeric_cols[:3]:  # Show first 3
                summary_parts.append(f"  - {col}: Mean = {df[col].mean():.2f}, Range = [{df[col].min():.2f}, {df[col].max():.2f}]")
        
        # Categorical columns
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            summary_parts.append(f"\n**Text Columns:** {len(cat_cols)}")
            
            for col in cat_cols[:3]:
                summary_parts.append(f"  - {col}: {df[col].nunique()} unique values")
        
        # Data quality quick check
        missing_count = df.isnull().sum().sum()
        if missing_count > 0:
            summary_parts.append(f"\n⚠️ Missing values detected: {missing_count}")
        
        return "\n".join(summary_parts)
    
    def _handle_aggregate(self, query, df, intent_info):
        """Handle aggregation queries"""
        query_lower = query.lower()
        
        # Detect aggregation function
        if 'sum' in query_lower or 'total' in query_lower:
            func = 'sum'
            func_name = 'Sum'
        elif 'average' in query_lower or 'mean' in query_lower:
            func = 'mean'
            func_name = 'Average'
        elif 'count' in query_lower or 'how many' in query_lower:
            func = 'count'
            func_name = 'Count'
        elif 'max' in query_lower or 'maximum' in query_lower or 'highest' in query_lower:
            func = 'max'
            func_name = 'Maximum'
        elif 'min' in query_lower or 'minimum' in query_lower or 'lowest' in query_lower:
            func = 'min'
            func_name = 'Minimum'
        else:
            func = 'count'
            func_name = 'Count'
        
        # Try to find column name in query
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        target_col = None
        for col in numeric_cols:
            if col.lower() in query_lower:
                target_col = col
                break
        
        if target_col is None and len(numeric_cols) > 0:
            target_col = numeric_cols[0]
        
        if target_col is None:
            return f"I couldn't find a numeric column to calculate {func_name}. Available numeric columns: {', '.join(numeric_cols) if len(numeric_cols) > 0 else 'None'}"
        
        # Calculate aggregation
        if func == 'sum':
            result = df[target_col].sum()
        elif func == 'mean':
            result = df[target_col].mean()
        elif func == 'count':
            result = df[target_col].count()
        elif func == 'max':
            result = df[target_col].max()
        elif func == 'min':
            result = df[target_col].min()
        
        return f"📊 {func_name} of **{target_col}**: {result:,.2f}"
    
    def _handle_filter(self, query, df):
        """Handle filter queries"""
        return "I can help you filter the data. Please use the Data Processing page to apply filters, or ask me a more specific question about what you'd like to see."
    
    def _handle_trend(self, df):
        """Handle trend queries"""
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        if not date_cols:
            # Try to find potential date columns
            potential_date_cols = [col for col in df.columns if 'date' in col.lower()]
            
            if potential_date_cols:
                return f"I found potential date columns: {', '.join(potential_date_cols)}. Please convert them to date format first in the Data Processing page."
            else:
                return "I couldn't find any date columns to analyze trends. Please ensure your data has date information."
        
        date_col = date_cols[0]
        
        # Find numeric column
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return "No numeric columns found to analyze trends."
        
        metric_col = numeric_cols[0]
        
        # Calculate trend
        df_sorted = df.sort_values(date_col)
        
        first_value = df_sorted[metric_col].iloc[0]
        last_value = df_sorted[metric_col].iloc[-1]
        
        change = last_value - first_value
        change_pct = (change / first_value * 100) if first_value != 0 else 0
        
        direction = "increased" if change > 0 else "decreased"
        
        return f"📈 Trend Analysis:\n\n**{metric_col}** has {direction} by {abs(change_pct):.1f}% over the time period.\n\n- Start: {first_value:,.2f}\n- End: {last_value:,.2f}\n- Change: {change:+,.2f}"
    
    def _handle_anomaly_query(self, df):
        """Handle anomaly detection queries"""
        from modules.anomaly_detector import AnomalyDetector
        
        detector = AnomalyDetector()
        anomalies = detector.detect_anomalies(df)
        
        if not anomalies:
            return "✅ Good news! I didn't find any significant anomalies in your data."
        
        response = f"🚨 I found {len(anomalies)} potential issues:\n\n"
        
        for i, anomaly in enumerate(anomalies[:5], 1):  # Show first 5
            response += f"{i}. **{anomaly['type']}** in {anomaly.get('column', 'data')}\n"
            response += f"   - {anomaly['message']}\n"
            response += f"   - Severity: {anomaly['severity']}\n\n"
        
        if len(anomalies) > 5:
            response += f"...and {len(anomalies) - 5} more. Check the Anomaly Detection tab for full details."
        
        return response
    
    def _handle_quality_query(self, df):
        """Handle data quality queries"""
        from modules.data_quality import DataQualityChecker
        
        checker = DataQualityChecker()
        scores = checker.calculate_scores(df)
        
        response = "📊 **Data Quality Report**\n\n"
        
        response += f"- **Completeness**: {scores['completeness']}% "
        response += "✅" if scores['completeness'] > 90 else "⚠️"
        response += "\n"
        
        response += f"- **Consistency**: {scores['consistency']}% "
        response += "✅" if scores['consistency'] > 85 else "⚠️"
        response += "\n"
        
        response += f"- **Duplicate Risk**: {scores['duplicate_risk']}\n"
        response += f"- **Anomaly Risk**: {scores['anomaly_risk']}\n"
        
        # Missing values
        missing_cols = df.columns[df.isnull().any()].tolist()
        
        if missing_cols:
            response += f"\n⚠️ Columns with missing data: {', '.join(missing_cols[:5])}"
        
        # Duplicates
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            response += f"\n⚠️ Found {dup_count} duplicate rows"
        
        return response
    
    def _handle_general_query(self, query, df):
        """Handle general queries"""
        query_lower = query.lower()
        
        # Try to identify what user wants
        if 'column' in query_lower:
            cols = ', '.join(df.columns[:10])
            extra = f" (and {len(df.columns) - 10} more)" if len(df.columns) > 10 else ""
            return f"Your dataset has {len(df.columns)} columns: {cols}{extra}"
        
        elif 'row' in query_lower:
            return f"Your dataset has {len(df):,} rows."
        
        elif 'help' in query_lower:
            return self._get_help_message()
        
        elif 'insight' in query_lower or 'tell me' in query_lower:
            return self._generate_insights(df)
        
        else:
            return "I'm not sure I understand. You can ask me about:\n- Data summary\n- Aggregations (sum, average, count, etc.)\n- Trends over time\n- Data quality issues\n- Anomalies\n\nOr simply ask 'help' for more options."
    
    def _get_help_message(self):
        """Return help message"""
        return """
🤖 **I can help you with:**

📊 **Data Analysis**
- "Give me a summary of the data"
- "What's the total/average/count of [column]?"
- "Show me trends"

🔍 **Data Quality**
- "Are there any data quality issues?"
- "Find anomalies"
- "Check for duplicates"

📈 **Insights**
- "What are the key insights?"
- "Tell me something interesting about this data"

Just ask in natural language and I'll do my best to help!
        """
    
    def _generate_insights(self, df):
        """Generate automatic insights"""
        insights = []
        
        # Insight 1: Record count
        insights.append(f"📊 Your dataset contains {len(df):,} records across {len(df.columns)} columns.")
        
        # Insight 2: Data completeness
        completeness = (1 - df.isnull().sum().sum() / df.size) * 100
        
        if completeness > 95:
            insights.append(f"✅ Data is {completeness:.1f}% complete - excellent!")
        elif completeness > 80:
            insights.append(f"⚠️ Data is {completeness:.1f}% complete - some missing values detected.")
        else:
            insights.append(f"🚨 Data is only {completeness:.1f}% complete - significant gaps found.")
        
        # Insight 3: Numeric columns analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            # Find column with highest variation
            variations = {col: df[col].std() / df[col].mean() for col in numeric_cols if df[col].mean() != 0}
            
            if variations:
                most_varied = max(variations, key=variations.get)
                insights.append(f"📊 '{most_varied}' shows the highest variation in your data.")
        
        # Insight 4: Duplicate check
        dup_count = df.duplicated().sum()
        
        if dup_count > 0:
            insights.append(f"⚠️ Found {dup_count} duplicate records that may need review.")
        else:
            insights.append(f"✅ No duplicate records found.")
        
        return "\n\n".join(insights)
    
    def get_suggested_questions(self, df):
        """Get suggested questions based on data"""
        suggestions = [
            "What's the summary of this data?",
            "Are there any data quality issues?",
            "Show me key insights"
        ]
        
        # Add column-specific suggestions
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            suggestions.append(f"What's the total {col}?")
        
        # Add date-specific suggestions
        date_cols = df.select_dtypes(include=['datetime64']).columns
        
        if len(date_cols) > 0:
            suggestions.append("Show me trends over time")
        
        return suggestions

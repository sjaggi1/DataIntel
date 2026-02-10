import re
from typing import Dict, List

class IntentDetector:
    """Detects user intent from natural language queries"""
    
    def __init__(self):
        self.intent_patterns = {
            'summary': [
                r'summar',
                r'overview',
                r'what.*data',
                r'tell me about',
                r'describe'
            ],
            'aggregate': [
                r'total',
                r'sum',
                r'average',
                r'mean',
                r'count',
                r'how many',
                r'number of'
            ],
            'filter': [
                r'show.*where',
                r'filter',
                r'only',
                r'with',
                r'having'
            ],
            'trend': [
                r'trend',
                r'over time',
                r'change',
                r'growth',
                r'increase',
                r'decrease'
            ],
            'comparison': [
                r'compare',
                r'versus',
                r'vs',
                r'difference',
                r'between'
            ],
            'anomaly': [
                r'anomal',
                r'outlier',
                r'unusual',
                r'strange',
                r'weird',
                r'wrong'
            ],
            'export': [
                r'export',
                r'download',
                r'save',
                r'generate.*file'
            ],
            'visualization': [
                r'chart',
                r'graph',
                r'plot',
                r'visuali[sz]e',
                r'show.*graph'
            ],
            'prediction': [
                r'predict',
                r'forecast',
                r'future',
                r'what will',
                r'expect'
            ],
            'quality': [
                r'quality',
                r'missing',
                r'duplicate',
                r'clean',
                r'valid'
            ]
        }
    
    def detect_intent(self, query: str) -> Dict[str, any]:
        """Detect the primary intent from a user query"""
        query_lower = query.lower()
        
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            matched_patterns = []
            
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    score += 1
                    matched_patterns.append(pattern)
            
            if score > 0:
                intent_scores[intent] = {
                    'score': score,
                    'patterns': matched_patterns
                }
        
        if not intent_scores:
            return {
                'primary_intent': 'general_query',
                'confidence': 0.5,
                'entities': self._extract_entities(query)
            }
        
        # Get primary intent (highest score)
        primary = max(intent_scores.items(), key=lambda x: x[1]['score'])
        
        return {
            'primary_intent': primary[0],
            'confidence': min(1.0, primary[1]['score'] / 3),
            'secondary_intents': [k for k, v in intent_scores.items() if k != primary[0]],
            'entities': self._extract_entities(query),
            'matched_patterns': primary[1]['patterns']
        }
    
    def _extract_entities(self, query: str) -> Dict[str, List[str]]:
        """Extract entities from query"""
        entities = {
            'columns': [],
            'values': [],
            'dates': [],
            'numbers': []
        }
        
        # Extract potential column names (capitalized words)
        entities['columns'] = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', query)
        
        # Extract dates
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}/\d{2}/\d{4}',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}'
        ]
        
        for pattern in date_patterns:
            entities['dates'].extend(re.findall(pattern, query))
        
        # Extract numbers
        entities['numbers'] = re.findall(r'\b\d+(?:\.\d+)?\b', query)
        
        # Extract quoted values
        entities['values'] = re.findall(r'["\']([^"\']+)["\']', query)
        
        return entities
    
    def suggest_query(self, intent: str) -> str:
        """Suggest a follow-up query based on intent"""
        suggestions = {
            'summary': "Would you like to see specific statistics or a detailed breakdown?",
            'aggregate': "Would you like to see this aggregation by specific groups?",
            'filter': "Would you like to apply additional filters?",
            'trend': "Would you like to see trends for a specific time period?",
            'comparison': "Would you like to compare additional categories?",
            'anomaly': "Would you like to investigate the anomalies further?",
            'export': "What format would you prefer for the export?",
            'visualization': "What type of chart would you prefer?",
            'prediction': "What time horizon would you like for the prediction?",
            'quality': "Would you like recommendations for fixing data quality issues?"
        }
        
        return suggestions.get(intent, "How else can I help you with this data?")
    
    def parse_aggregation_query(self, query: str) -> Dict:
        """Parse aggregation-specific queries"""
        agg_functions = {
            'sum': ['sum', 'total'],
            'mean': ['average', 'mean'],
            'count': ['count', 'number of', 'how many'],
            'min': ['minimum', 'min', 'lowest'],
            'max': ['maximum', 'max', 'highest']
        }
        
        query_lower = query.lower()
        
        detected_function = None
        for func, keywords in agg_functions.items():
            if any(kw in query_lower for kw in keywords):
                detected_function = func
                break
        
        return {
            'function': detected_function or 'count',
            'group_by': self._detect_group_by(query)
        }
    
    def _detect_group_by(self, query: str) -> List[str]:
        """Detect grouping fields from query"""
        patterns = [
            r'by\s+(\w+)',
            r'for each\s+(\w+)',
            r'per\s+(\w+)',
            r'grouped by\s+(\w+)'
        ]
        
        groups = []
        for pattern in patterns:
            matches = re.findall(pattern, query.lower())
            groups.extend(matches)
        
        return list(set(groups))

import pandas as pd
from datetime import datetime
import json

class AuditLogger:
    """Comprehensive audit logging system"""
    
    def __init__(self):
        self.logs = []
    
    def log_action(self, action, user, details=""):
        """Log a user action"""
        log_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'action': action,
            'user': user,
            'details': details,
            'session_id': self._get_session_id()
        }
        
        self.logs.append(log_entry)
        
        return log_entry
    
    def log_data_access(self, user, resource, operation):
        """Log data access events"""
        return self.log_action(
            action=f"Data Access: {operation}",
            user=user,
            details=f"Resource: {resource}"
        )
    
    def log_data_modification(self, user, table, operation, row_count=0):
        """Log data modification events"""
        return self.log_action(
            action=f"Data Modification: {operation}",
            user=user,
            details=f"Table: {table}, Rows affected: {row_count}"
        )
    
    def log_export(self, user, format, row_count):
        """Log data export events"""
        return self.log_action(
            action="Data Export",
            user=user,
            details=f"Format: {format}, Rows: {row_count}"
        )
    
    def log_error(self, user, error_type, error_message):
        """Log error events"""
        return self.log_action(
            action=f"Error: {error_type}",
            user=user,
            details=error_message
        )
    
    def log_security_event(self, user, event_type, details):
        """Log security-related events"""
        return self.log_action(
            action=f"Security: {event_type}",
            user=user,
            details=details
        )
    
    def get_all_logs(self):
        """Retrieve all logs"""
        return self.logs
    
    def get_recent_logs(self, count=10):
        """Get most recent logs"""
        return self.logs[-count:] if len(self.logs) >= count else self.logs
    
    def get_logs_by_user(self, user):
        """Get logs for specific user"""
        return [log for log in self.logs if log['user'] == user]
    
    def get_logs_by_action(self, action):
        """Get logs for specific action"""
        return [log for log in self.logs if action.lower() in log['action'].lower()]
    
    def get_logs_by_date_range(self, start_date, end_date):
        """Get logs within date range"""
        filtered_logs = []
        
        for log in self.logs:
            log_date = datetime.strptime(log['timestamp'], "%Y-%m-%d %H:%M:%S")
            
            if start_date <= log_date <= end_date:
                filtered_logs.append(log)
        
        return filtered_logs
    
    def export_logs_to_csv(self, filename="audit_log.csv"):
        """Export logs to CSV file"""
        if self.logs:
            df = pd.DataFrame(self.logs)
            df.to_csv(filename, index=False)
            return filename
        return None
    
    def export_logs_to_json(self, filename="audit_log.json"):
        """Export logs to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.logs, f, indent=2)
        return filename
    
    def get_audit_summary(self):
        """Generate audit summary statistics"""
        if not self.logs:
            return {
                'total_events': 0,
                'unique_users': 0,
                'event_types': {}
            }
        
        df = pd.DataFrame(self.logs)
        
        summary = {
            'total_events': len(self.logs),
            'unique_users': df['user'].nunique(),
            'event_types': df['action'].value_counts().to_dict(),
            'events_by_user': df.groupby('user').size().to_dict(),
            'recent_activity': self.get_recent_logs(5)
        }
        
        return summary
    
    def clear_logs(self):
        """Clear all logs (use with caution!)"""
        self.logs = []
    
    def _get_session_id(self):
        """Generate or retrieve session ID"""
        # In a real application, this would be tied to user session
        return "session_" + datetime.now().strftime("%Y%m%d")
    
    def generate_compliance_report(self, start_date=None, end_date=None):
        """Generate compliance audit report"""
        logs = self.logs
        
        if start_date or end_date:
            if start_date and not end_date:
                end_date = datetime.now()
            elif end_date and not start_date:
                start_date = datetime.min
            
            logs = self.get_logs_by_date_range(start_date, end_date)
        
        if not logs:
            return {
                'status': 'No logs found',
                'period': 'N/A'
            }
        
        df = pd.DataFrame(logs)
        
        report = {
            'period': {
                'start': logs[0]['timestamp'],
                'end': logs[-1]['timestamp']
            },
            'total_events': len(logs),
            'unique_users': df['user'].nunique(),
            'actions_summary': df['action'].value_counts().to_dict(),
            'user_activity': df.groupby('user').size().to_dict(),
            'security_events': len([l for l in logs if 'Security' in l['action']]),
            'data_exports': len([l for l in logs if 'Export' in l['action']]),
            'data_modifications': len([l for l in logs if 'Modification' in l['action']]),
            'errors': len([l for l in logs if 'Error' in l['action']])
        }
        
        return report
    
    def check_suspicious_activity(self):
        """Detect suspicious activity patterns"""
        if len(self.logs) < 5:
            return []
        
        suspicious = []
        
        df = pd.DataFrame(self.logs)
        
        # Check for rapid consecutive actions
        df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp_dt')
        df['time_diff'] = df['timestamp_dt'].diff().dt.total_seconds()
        
        rapid_actions = df[df['time_diff'] < 1]  # Less than 1 second apart
        
        if len(rapid_actions) > 0:
            suspicious.append({
                'type': 'Rapid Actions',
                'severity': 'Medium',
                'details': f'{len(rapid_actions)} actions performed in quick succession',
                'users': rapid_actions['user'].unique().tolist()
            })
        
        # Check for unusual export volume
        export_logs = df[df['action'].str.contains('Export', case=False)]
        
        if len(export_logs) > 10:
            suspicious.append({
                'type': 'High Export Volume',
                'severity': 'High',
                'details': f'{len(export_logs)} export operations detected',
                'users': export_logs['user'].unique().tolist()
            })
        
        # Check for failed access attempts
        error_logs = df[df['action'].str.contains('Error', case=False)]
        
        if len(error_logs) > 5:
            suspicious.append({
                'type': 'Multiple Errors',
                'severity': 'Low',
                'details': f'{len(error_logs)} errors occurred',
                'users': error_logs['user'].unique().tolist()
            })
        
        return suspicious

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

class PredictiveAnalytics:
    """Handles predictive analytics and forecasting"""
    
    def forecast_timeseries(self, df, date_col, metric_col, periods=3):
        """Forecast future values using simple trend analysis"""
        try:
            # Sort by date
            df_sorted = df.sort_values(date_col).copy()
            
            # Create numeric representation of dates
            df_sorted['date_numeric'] = (df_sorted[date_col] - df_sorted[date_col].min()).dt.days
            
            # Prepare data for model
            X = df_sorted[['date_numeric']].values
            y = df_sorted[metric_col].values
            
            # Train model
            model = LinearRegression()
            model.fit(X, y)
            
            # Generate future dates
            last_date = df_sorted[date_col].max()
            freq = self._infer_frequency(df_sorted[date_col])
            
            future_dates = pd.date_range(
                start=last_date + freq,
                periods=periods,
                freq=freq
            )
            
            # Generate predictions
            last_numeric = df_sorted['date_numeric'].max()
            future_numeric = np.array([
                last_numeric + i * freq.n
                for i in range(1, periods + 1)
            ]).reshape(-1, 1)
            
            predictions = model.predict(future_numeric)
            
            # Create forecast DataFrame
            forecast_df = pd.DataFrame({
                'date': future_dates,
                'forecast': predictions
            })
            
            return forecast_df
            
        except Exception as e:
            # Fallback to simple average
            avg = df[metric_col].mean()
            future_dates = pd.date_range(
                start=df[date_col].max() + timedelta(days=1),
                periods=periods,
                freq='D'
            )
            
            return pd.DataFrame({
                'date': future_dates,
                'forecast': [avg] * periods
            })
    
    def _infer_frequency(self, date_series):
        """Infer the frequency of a date series"""
        if len(date_series) < 2:
            return pd.DateOffset(days=1)
        
        # Calculate mode of differences
        diffs = date_series.diff().dropna()
        
        avg_diff = diffs.mean().days
        
        if avg_diff <= 1:
            return pd.DateOffset(days=1)
        elif avg_diff <= 7:
            return pd.DateOffset(weeks=1)
        elif avg_diff <= 31:
            return pd.DateOffset(months=1)
        else:
            return pd.DateOffset(years=1)
    
    def predict_attrition_risk(self, df):
        """Predict employee attrition risk"""
        risk_factors = []
        
        # Check tenure
        if 'joining_date' in df.columns or 'hire_date' in df.columns:
            date_col = 'joining_date' if 'joining_date' in df.columns else 'hire_date'
            
            try:
                df[date_col] = pd.to_datetime(df[date_col])
                df['tenure_days'] = (datetime.now() - df[date_col]).dt.days
                
                # High risk: < 1 year
                short_tenure = df[df['tenure_days'] < 365]
                
                if len(short_tenure) > 0:
                    risk_factors.append({
                        'factor': 'Short Tenure (< 1 year)',
                        'count': len(short_tenure),
                        'risk_score': 0.35
                    })
            except:
                pass
        
        # Check salary
        salary_cols = [col for col in df.columns if 'salary' in col.lower()]
        
        if salary_cols:
            sal_col = salary_cols[0]
            
            if pd.api.types.is_numeric_dtype(df[sal_col]):
                median_salary = df[sal_col].median()
                
                # Below market (< 75% of median)
                below_market = df[df[sal_col] < median_salary * 0.75]
                
                if len(below_market) > 0:
                    risk_factors.append({
                        'factor': 'Salary Below Market',
                        'count': len(below_market),
                        'risk_score': 0.42
                    })
        
        # Overall attrition rate estimate
        total_employees = len(df)
        total_risk_score = sum([f['risk_score'] * f['count'] for f in risk_factors])
        
        if total_employees > 0:
            estimated_attrition = (total_risk_score / total_employees) * 100
        else:
            estimated_attrition = 0
        
        return {
            'risk_factors': risk_factors,
            'estimated_attrition_rate': round(estimated_attrition, 2),
            'high_risk_employees': sum([f['count'] for f in risk_factors])
        }
    
    def forecast_hiring_needs(self, df, months_ahead=3):
        """Forecast future hiring needs"""
        # Check for joining date column
        date_cols = [col for col in df.columns if 'join' in col.lower() or 'hire' in col.lower()]
        
        if not date_cols:
            return {
                'forecast': [{'month': i+1, 'predicted_hires': 0} for i in range(months_ahead)],
                'confidence': 'Low'
            }
        
        date_col = date_cols[0]
        
        try:
            df[date_col] = pd.to_datetime(df[date_col])
            
            # Group by month
            monthly_hires = df.groupby(pd.Grouper(key=date_col, freq='M')).size()
            
            if len(monthly_hires) < 3:
                # Not enough data
                avg_hires = monthly_hires.mean() if len(monthly_hires) > 0 else 5
                
                forecast = [
                    {
                        'month': i+1,
                        'predicted_hires': int(avg_hires)
                    }
                    for i in range(months_ahead)
                ]
                
                return {
                    'forecast': forecast,
                    'confidence': 'Low'
                }
            
            # Simple trend-based forecast
            X = np.arange(len(monthly_hires)).reshape(-1, 1)
            y = monthly_hires.values
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict future months
            future_X = np.arange(len(monthly_hires), len(monthly_hires) + months_ahead).reshape(-1, 1)
            predictions = model.predict(future_X)
            
            # Ensure non-negative
            predictions = np.maximum(predictions, 0)
            
            forecast = [
                {
                    'month': i+1,
                    'predicted_hires': int(round(pred))
                }
                for i, pred in enumerate(predictions)
            ]
            
            # Calculate confidence based on R²
            from sklearn.metrics import r2_score
            train_pred = model.predict(X)
            r2 = r2_score(y, train_pred)
            
            confidence = 'High' if r2 > 0.7 else 'Medium' if r2 > 0.4 else 'Low'
            
            return {
                'forecast': forecast,
                'confidence': confidence,
                'trend': 'Increasing' if model.coef_[0] > 0 else 'Decreasing'
            }
            
        except Exception as e:
            return {
                'forecast': [{'month': i+1, 'predicted_hires': 5} for i in range(months_ahead)],
                'confidence': 'Low',
                'error': str(e)
            }
    
    def forecast_salary_budget(self, df, months_ahead=12):
        """Forecast salary budget for future months"""
        salary_cols = [col for col in df.columns if 'salary' in col.lower()]
        
        if not salary_cols:
            return {
                'monthly_budget': [],
                'total_annual': 0
            }
        
        sal_col = salary_cols[0]
        
        if not pd.api.types.is_numeric_dtype(df[sal_col]):
            return {
                'monthly_budget': [],
                'total_annual': 0
            }
        
        # Current total monthly salary
        current_monthly = df[sal_col].sum()
        
        # Assume 3% annual growth and factor in predicted hires
        hiring_forecast = self.forecast_hiring_needs(df, months_ahead)
        
        monthly_budget = []
        cumulative = current_monthly
        
        for i in range(months_ahead):
            # Add predicted new hires
            new_hires = 0
            for forecast_item in hiring_forecast['forecast']:
                if forecast_item['month'] == i + 1:
                    new_hires = forecast_item['predicted_hires']
                    break
            
            # Estimate average salary for new hires
            avg_salary = df[sal_col].median()
            
            # Add new hire costs
            cumulative += new_hires * avg_salary
            
            # Add annual growth (prorated monthly)
            cumulative *= (1 + 0.03/12)
            
            monthly_budget.append({
                'month': i + 1,
                'budget': round(cumulative, 2)
            })
        
        return {
            'monthly_budget': monthly_budget,
            'total_annual': round(sum([m['budget'] for m in monthly_budget]), 2),
            'current_monthly': round(current_monthly, 2)
        }
    
    def detect_trends(self, df):
        """Detect various trends in the data"""
        trends = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            # Calculate trend using linear regression
            X = np.arange(len(df)).reshape(-1, 1)
            y = df[col].values
            
            # Remove NaN
            mask = ~np.isnan(y)
            if mask.sum() < 2:
                continue
            
            X_clean = X[mask]
            y_clean = y[mask]
            
            model = LinearRegression()
            model.fit(X_clean, y_clean)
            
            slope = model.coef_[0]
            
            if abs(slope) > 0.01:  # Significant trend
                direction = 'Increasing' if slope > 0 else 'Decreasing'
                strength = 'Strong' if abs(slope) > 0.1 else 'Moderate'
                
                trends.append({
                    'column': col,
                    'direction': direction,
                    'strength': strength,
                    'slope': round(slope, 4)
                })
        
        return trends
    
    def simulate_what_if(self, df, column, change_percent):
        """Simulate what-if scenario"""
        if column not in df.columns:
            return None
        
        if not pd.api.types.is_numeric_dtype(df[column]):
            return None
        
        original_sum = df[column].sum()
        original_mean = df[column].mean()
        
        # Apply change
        new_values = df[column] * (1 + change_percent / 100)
        
        new_sum = new_values.sum()
        new_mean = new_values.mean()
        
        return {
            'original': {
                'sum': original_sum,
                'mean': original_mean
            },
            'modified': {
                'sum': new_sum,
                'mean': new_mean
            },
            'change': {
                'sum': new_sum - original_sum,
                'mean': new_mean - original_mean,
                'percent': change_percent
            }
        }

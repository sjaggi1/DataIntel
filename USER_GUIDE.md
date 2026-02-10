# Enterprise Data Intelligence Platform - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Data Upload](#data-upload)
3. [Data Processing](#data-processing)
4. [Analytics Dashboard](#analytics-dashboard)
5. [AI Assistant](#ai-assistant)
6. [Data Governance](#data-governance)
7. [Alerts & Automation](#alerts--automation)
8. [Collaboration](#collaboration)
9. [Predictive Analytics](#predictive-analytics)
10. [Advanced Features](#advanced-features)

---

## Getting Started

### First Time Setup

1. **Launch the Application**
   ```bash
   streamlit run app.py
   ```
   Or use the startup script:
   ```bash
   ./start.sh
   ```

2. **Select Your Role**
   - In the sidebar, choose your user role
   - Roles: Admin, HR, Manager, Analyst
   - Different roles have different permissions

3. **Navigate the Interface**
   - Use the sidebar for navigation
   - Each page has specific functionality
   - Quick stats shown in sidebar

---

## Data Upload

### Uploading PDF Files

1. **Navigate to Data Upload Page**
   - Click "📤 Data Upload" in sidebar

2. **Upload Files**
   - Click "Choose PDF file(s)"
   - Select one or multiple PDF files
   - Supported formats: .pdf

3. **Configure Parsing Settings**
   - **Auto-detect**: Let system detect delimiter
   - **Comma (,)**: For CSV-like data
   - **Semicolon (;)**: For semicolon-separated data
   - **Colon (:)**: For key-value pairs
   - **Tab**: For tab-separated data
   - **Mixed**: For complex formats (use regex)

4. **Analyze Structure**
   - Click "Analyze PDF Structure"
   - System will:
     - Extract text from PDF
     - Detect data structure
     - Identify column names
     - Infer data types
     - Show preview

### OCR for Scanned PDFs

1. **Navigate to Image/Scanned PDF Tab**
2. **Upload scanned file or image**
3. **Select OCR language**
   - English
   - Hindi
   - Multi-language
4. **Click "Process with OCR"**
5. **Review extracted text**
6. **Parse to data table**

### Upload Settings

Configure default settings:
- Auto-process on upload
- Enable duplicate detection
- Auto-mask sensitive data
- Max file size limit
- Default encoding
- Date format preference

---

## Data Processing

### Column Mapping

**Purpose**: Reorganize and combine columns for your Excel output

1. **Navigate to Column Mapping Tab**
2. **View Current Columns**
   - See all detected columns
3. **Create Custom Mappings**
   - Set number of output columns
   - For each output column:
     - Name the column
     - Select source columns to combine
     - Choose separator (space, comma, etc.)
     - Apply transformation:
       - None
       - Uppercase
       - Lowercase
       - Title Case
       - Trim whitespace
       - Remove special characters
4. **Apply Mapping**
   - Click "Apply Mapping"
   - Review preview
   - Data is now reorganized

**Example Use Case**:
```
Input: FirstName, MiddleName, LastName
Output: FullName (FirstName + " " + MiddleName + " " + LastName)
```

### Data Cleaning

**Missing Values**
- View missing value count per column
- Choose handling method:
  - Keep as is
  - Remove rows
  - Fill with mean (numeric)
  - Fill with median (numeric)
  - Fill with mode
  - Fill with custom value

**Duplicate Detection**
- Automatically counts duplicates
- One-click removal
- Preview affected rows

**Data Type Validation**
- Review data types
- Identify type mismatches
- Convert as needed

### Transformations

**Date Parsing**
- Select date column
- Specify date format
- Convert to datetime
- Example: "2024-01-15" → datetime

**Text Extraction**
- Use regex patterns
- Extract specific parts
- Create new columns
- Example: Extract phone from "Call: 1234567890"

**Numeric Conversion**
- Convert text to numbers
- Handle currency symbols
- Parse percentages

### Export Options

**Excel Export**
- ✅ Include dashboard charts
- ✅ Include summary sheet
- ✅ Apply professional formatting
- Enter filename
- Click "Generate Excel"
- Download file

**Dashboard Report (PDF/Word)**
- Select format (PDF or DOCX)
- Click "Generate Dashboard Report"
- Includes:
  - Executive summary
  - Data quality analysis
  - Statistical summaries
  - Charts and visualizations
  - Recommendations

---

## Analytics Dashboard

### Data Quality Score

**Metrics Displayed**:
- **Completeness**: % of non-null values
  - Target: >90%
- **Consistency**: Data format uniformity
  - Target: >85%
- **Duplicate Risk**: Low/Medium/High
- **Anomaly Risk**: Low/Medium/High

### Overview Analytics

**Dataset Summary**
- Total records
- Total columns
- Memory usage
- Quick statistics

**Column Analysis**
- Select any column
- View:
  - Sum (numeric)
  - Mean (numeric)
  - Median (numeric)
  - Std deviation (numeric)
  - Unique values (text)
  - Most common value (text)
- Distribution chart

### Trend Analysis

**Prerequisites**: Date column required

**Features**:
- Select date column
- Select metric
- Choose aggregation period:
  - Daily
  - Weekly
  - Monthly
  - Quarterly
  - Yearly
- View:
  - Trend line
  - Count overlay
  - Growth rate

### Anomaly Analysis

**Automated Detection**:
- Statistical outliers
- Impossible values
- Future dates
- Negative values (where inappropriate)
- Duplicate entries
- Sudden spikes

**Review Anomalies**:
- Severity levels (High/Medium/Low)
- Affected rows
- Details and recommendations

**Manual Outlier Detection**:
- Select column
- Choose method:
  - IQR (Interquartile Range)
  - Z-Score
- View box plot
- Review outlier data

### What-If Analysis

**Simulate Changes**:
1. Select column to modify
2. Choose modification type:
   - Percentage increase
   - Percentage decrease
   - Add fixed amount
   - Multiply by factor
3. Set change value
4. View impact:
   - Current vs new totals
   - Current vs new averages
   - Delta calculations
5. Compare scenarios visually

**Use Cases**:
- "What if salaries increase by 10%?"
- "What if we hire 5 more employees?"
- "What if costs reduce by 15%?"

### Deep Dive Analytics

**Correlation Analysis**
- View correlation matrix
- Identify strong correlations (>0.7)
- Understand relationships

**Group-by Analysis**
- Group by any column
- Aggregate with:
  - Sum
  - Mean
  - Median
  - Count
  - Min
  - Max
- Top 20 results
- Interactive charts

---

## AI Assistant

### Using the Chatbot

**Ask Natural Language Questions**:
- "Give me a summary of the data"
- "What's the total salary?"
- "Show me trends over time"
- "Are there any data quality issues?"
- "Find anomalies"
- "What are the key insights?"

**Intent Detection**:
System automatically detects:
- Summary requests
- Aggregations
- Filtering
- Trend analysis
- Comparisons
- Anomaly detection
- Export needs
- Visualization requests
- Predictions
- Quality checks

**Quick Actions**:
- Data Summary
- Find Insights
- Show Trends
- Detect Issues

**Tips for Best Results**:
- Be specific: "total salary" vs "salary info"
- Mention column names when possible
- Ask one question at a time
- Use follow-up questions

---

## Data Governance

### Data Masking

**Automatic Detection**:
System detects:
- Email addresses
- Phone numbers
- SSN
- Aadhaar numbers
- PAN numbers
- Credit card numbers

**Masking Methods**:

1. **Partial Mask**
   - Email: jo**@example.com
   - Phone: ******7890
   - General: ab****yz

2. **Full Mask**
   - Everything replaced with *
   - Length preserved

3. **Hash**
   - SHA-256 hash (16 chars)
   - One-way encryption
   - Consistent for same value

4. **Tokenize**
   - Replace with TOKEN_xxx
   - Unique identifier
   - Reversible with key

**Apply Masking**:
1. Review detected sensitive columns
2. Choose masking method per column
3. Click "Apply Masking"
4. Preview masked data
5. Export if needed

### Audit Log

**What's Logged**:
- Data uploads
- Data modifications
- Exports
- User actions
- Security events
- Errors

**Filter Logs**:
- By action type
- By user
- By date range

**Export Logs**:
- CSV format
- For compliance
- For analysis

**Compliance Reporting**:
- Generate periodic reports
- Review security events
- Monitor access patterns
- Detect suspicious activity

### Access Control

**Role Permissions**:

**Admin**
- View all data
- Edit data
- Delete data
- Export data
- Manage users
- View salary
- Mask data

**HR**
- View all data
- Edit data
- Export data
- View salary
- Mask data

**Manager**
- View all data
- View headcount
- Basic analytics

**Analyst**
- View all data
- Basic analytics
- Export data

**Column-Level Restrictions**:
- Some columns restricted by role
- Example: Managers can't view salary details
- Automatic enforcement

---

## Alerts & Automation

### Email Alerts

**Configure Notifications**:
1. Enable email notifications
2. Enter recipient email
3. Select triggers:
   - New PDF uploaded
   - Data processing completed
   - Anomalies detected
   - Quality score below threshold
4. Set threshold (if applicable)
5. Save settings

**Email Content**:
- Action summary
- Data statistics
- Links to reports
- Anomaly details (if any)

### Slack/Teams Integration

**Setup**:
1. Choose platform (Slack or Teams)
2. Generate webhook URL in Slack/Teams
3. Enter webhook URL in application
4. Test integration
5. Configure triggers

**Notifications Sent**:
- "New employee data processed"
- "Dashboard updated"
- "Data quality alert"
- "Anomalies detected"

### Automation Rules

**Create Rule**:
1. Name the rule
2. Select trigger:
   - New PDF uploaded
   - Schedule (daily/weekly)
   - Quality score change
   - Anomaly detected
3. Choose actions:
   - Convert to Excel
   - Generate dashboard
   - Send email
   - Mask sensitive data
   - Run quality check
   - Create backup
4. Create rule

**Manage Rules**:
- View active rules
- See last run time
- Enable/disable rules
- Edit configurations

---

## Collaboration

### Comments

**Add Row Comments**:
1. Navigate to Comments tab
2. View data table
3. Select row number
4. Add comment text
5. Click "Add Comment"

**View Comments**:
- See all comments for selected row
- Shows user and timestamp
- Organized by row

**Use Cases**:
- "Verify this salary amount"
- "Check employee ID"
- "Confirm hire date"

### Task Management

**Create Task**:
1. Enter task title
2. Assign to role (HR, Manager, Admin, Analyst)
3. Set priority (Low/Medium/High/Critical)
4. Set due date
5. Add description
6. Click "Create Task"

**Manage Tasks**:
- View all active tasks
- See assignee
- Check priority
- Review due dates
- Mark as complete

**Priority Indicators**:
- 🔴 Critical
- 🟡 High
- 🟢 Medium/Low

---

## Predictive Analytics

### Forecasting

**Time Series Forecast**:
1. Select date column
2. Select metric to forecast
3. Set forecast periods (1-12 months)
4. Click "Generate Forecast"
5. View:
   - Historical data
   - Forecast line
   - Forecast table
   - Confidence level

**Models Used**:
- Linear regression
- Trend analysis
- Seasonal adjustment

### Predictions

**Hiring Trend Forecast**:
- Predicts future hires
- Based on historical data
- Shows trend direction
- Confidence level

**Attrition Risk**:
- Analyzes risk factors
- Identifies high-risk employees
- Estimates attrition rate
- Shows risk score

**Salary Budget Projection**:
- 12-month forecast
- Includes new hires
- Accounts for growth (3% annual)
- Total annual budget

### Trend Projections

**Attrition Prediction**:
- Risk factors identified:
  - Tenure < 1 year
  - No promotion in 2 years
  - Salary below market
  - Low engagement
  - Manager change
- Impact score per factor
- Employees affected
- Recommended actions

---

## Advanced Features

### Data Quality Scoring

**Methodology**:
- Completeness: Non-null ratio
- Consistency: Format uniformity
- Validity: Format validation
- Accuracy: Estimated from patterns

**Interpretation**:
- 90-100%: Excellent
- 80-89%: Good
- 70-79%: Fair
- <70%: Needs improvement

### Schema Learning

**Automatic Detection**:
- Field names from headers
- Data types (number, date, text, etc.)
- Delimiters
- Structure (table, key-value, etc.)
- Relationships between columns

**Benefits**:
- Faster setup
- Fewer errors
- Better parsing
- Smart defaults

### Intent Detection

**How It Works**:
1. Analyzes user query
2. Identifies keywords and patterns
3. Classifies intent
4. Extracts entities
5. Generates appropriate response

**Intents Supported**:
- Summary
- Aggregation
- Filtering
- Trends
- Comparisons
- Anomalies
- Exports
- Visualizations
- Predictions
- Quality checks

### Anomaly Detection Algorithms

**Statistical Methods**:
1. **Z-Score**: Identifies values >3 standard deviations from mean
2. **IQR**: Detects values outside 1.5×IQR from Q1/Q3
3. **Business Rules**: Checks for impossible values

**What's Detected**:
- Outliers in numeric data
- Future dates
- Negative values (where inappropriate)
- Unrealistic ages
- Salary jumps
- Duplicate entries
- Activity spikes

---

## Tips & Best Practices

### For Best Results

1. **Data Preparation**
   - Ensure PDFs have clear structure
   - Use consistent formatting
   - Check for encryption

2. **Column Mapping**
   - Plan your output structure
   - Test with small samples
   - Document complex mappings

3. **Data Quality**
   - Run quality checks early
   - Address issues before export
   - Monitor trends over time

4. **Security**
   - Always mask sensitive data
   - Review audit logs regularly
   - Use appropriate role permissions

5. **Analytics**
   - Start with overview
   - Drill down into specifics
   - Use what-if for planning

6. **Collaboration**
   - Use comments for questions
   - Assign tasks for follow-up
   - Set realistic due dates

### Common Workflows

**Workflow 1: Basic PDF to Excel**
1. Upload PDF → Data Upload
2. Analyze structure
3. Apply mapping → Data Processing
4. Export to Excel

**Workflow 2: Quality Analysis & Cleanup**
1. Upload data
2. Check quality score → Analytics
3. Review anomalies
4. Clean data → Data Processing
5. Export cleaned version

**Workflow 3: Full Analytics Report**
1. Upload data
2. Process and clean
3. Generate insights → Analytics
4. Create dashboard report → Export
5. Share with stakeholders

**Workflow 4: Predictive Planning**
1. Upload historical data
2. Run forecasts → Predictive Analytics
3. Perform what-if analysis
4. Generate recommendations
5. Export forecast report

---

## Troubleshooting

### Common Issues

**PDF Not Parsing Correctly**
- Check if PDF is encrypted
- Try different delimiter
- Use OCR for scanned PDFs
- Verify PDF has extractable text

**Charts Not Showing**
- Ensure data has numeric columns
- Check if date column exists for trends
- Verify data has enough records

**Masking Not Applied**
- Check if sensitive data detected
- Verify column format
- Try manual masking selection

**Forecast Not Accurate**
- Need more historical data (minimum 3 periods)
- Check for data quality issues
- Verify date column format
- Review for outliers

**Export Failed**
- Check file permissions
- Verify data isn't too large
- Try exporting smaller subsets
- Check disk space

### Getting Help

1. **Use AI Assistant**
   - Ask your question in chat
   - Get instant guidance

2. **Check Audit Logs**
   - Review error messages
   - Identify failed operations

3. **Review Data Quality**
   - Run quality check
   - Fix identified issues

4. **Consult Documentation**
   - This user guide
   - README file
   - Code comments

---

## Keyboard Shortcuts

- **Navigate pages**: Use sidebar
- **Chat with AI**: Type in chat input
- **Download files**: Click download buttons
- **Refresh data**: Re-run analysis

---

## Version History

**v1.0.0** - February 2026
- Initial release
- All 21 features implemented
- Full documentation

---

**Questions? Use the AI Assistant or consult the README.md file!**

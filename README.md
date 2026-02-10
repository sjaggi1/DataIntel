# Enterprise Data Intelligence Platform

A comprehensive Streamlit-based web application for PDF to Excel conversion with advanced analytics, AI assistance, and enterprise-grade data governance.

## 🌟 Features

### 1. **Data Upload & Parsing** (Features 1-2, 15)
- Multiple PDF file upload support
- Automatic delimiter detection (comma, semicolon, colon, mixed)
- Custom column mapping and field reorganization
- OCR support for scanned PDFs and images
- Image intelligence for processing visual data

### 2. **Data Processing** (Features 3-4)
- Custom column mapping with field combination
- Data transformations (uppercase, lowercase, trim, etc.)
- Missing value handling
- Duplicate detection and removal
- Date parsing and regex extraction
- Quick analytics (sum, count, average, etc.)

### 3. **Schema Learning** (Feature 7)
- Automatic schema detection from raw data
- Field type inference (date, number, email, phone, etc.)
- Data structure recognition
- Relationship detection between columns

### 4. **Intent Detection** (Feature 5)
- Natural language query understanding
- Automatic intent classification
- Entity extraction from queries
- Smart query suggestions

### 5. **Anomaly Detection** (Feature 6)
- Statistical outlier detection (Z-score, IQR)
- Impossible value detection
- Duplicate identification
- Sudden spike detection
- Data inconsistency checking

### 6. **Data Quality Metrics** (Feature 8)
- Completeness score
- Consistency score
- Duplicate risk assessment
- Anomaly risk evaluation
- Validity checking
- Column-level quality metrics

### 7. **Data Masking & Privacy** (Feature 9)
- Automatic PII detection
- Multiple masking methods:
  - Partial masking
  - Full masking
  - Hashing
  - Tokenization
- Sensitive field protection (email, phone, SSN, Aadhaar, PAN, etc.)

### 8. **Audit Logging** (Feature 10)
- Comprehensive action logging
- User activity tracking
- Data access logging
- Export tracking
- Security event monitoring
- Compliance reporting
- Suspicious activity detection

### 9. **Excel Generation** (Feature 11)
- Professional formatting
- Automatic chart generation
- Summary statistics sheet
- Dashboard with visualizations
- Zebra striping for readability
- Formula support

### 10. **Dashboard Reports** (Feature 12)
- PDF report generation
- Word (DOCX) report generation
- Executive summaries
- Data quality analysis
- Statistical summaries
- Visual analytics
- Recommendations

### 11. **AI Chatbot Assistant** (Feature 13)
- Natural language queries
- Intent-based responses
- Data insights generation
- Automatic recommendations
- Contextual help

### 12. **Predictive Analytics** (Feature 14)
- Time series forecasting
- Attrition risk prediction
- Hiring needs forecasting
- Salary budget projection
- Trend detection
- What-if analysis

### 13. **Alerts & Automation** (Feature 16)
- Email notifications
- Slack/Teams integration
- Automated workflows
- Rule-based triggers
- Schedule-based actions

### 14. **Multi-User Collaboration** (Feature 17)
- Row-level comments
- Task assignment
- Priority management
- Due date tracking
- User mentions

### 15. **Compliance & Privacy** (Feature 18)
- Role-based access control (RBAC)
- Data masking engine
- Audit trails
- Compliance reporting
- Column-level access control

### 16. **What-If Simulator** (Feature 19)
- Percentage change simulation
- Fixed amount adjustments
- Impact analysis
- Scenario comparison
- Real-time calculations

### 17. **Predictive Insights** (Feature 20)
- Hiring trend forecasts
- Attrition predictions
- Budget projections
- Risk factor analysis

### 18. **Anomaly & Outlier Detection** (Feature 21)
- Real-time anomaly alerts
- Statistical outlier identification
- Business rule violations
- Data quality alerts

## 📁 Project Structure

```
.
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── modules/
│   ├── pdf_parser.py              # PDF parsing and text extraction
│   ├── schema_learner.py          # Automatic schema detection
│   ├── intent_detector.py         # Natural language intent detection
│   ├── anomaly_detector.py        # Anomaly and outlier detection
│   ├── data_quality.py            # Data quality metrics
│   ├── masking.py                 # Data masking and privacy
│   ├── audit_log.py               # Comprehensive audit logging
│   ├── predictive_analytics.py    # Forecasting and predictions
│   ├── chatbot.py                 # AI chatbot assistant
│   ├── excel_generator.py         # Excel file generation
│   └── dashboard_generator.py     # PDF/Word report generation
└── README.md                       # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Tesseract OCR (for scanned PDF processing)

### Steps

1. **Clone or download the project**

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Tesseract OCR** (Optional, for scanned PDF support)

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**
Navigate to: http://localhost:8501

## 💡 Usage Guide

### 1. Upload Data
- Go to **Data Upload** page
- Upload PDF file(s)
- Select delimiter type or use auto-detect
- Click "Analyze PDF Structure"

### 2. Process Data
- Navigate to **Data Processing**
- Configure column mappings
- Apply data cleaning
- Perform transformations
- Export to Excel or dashboard format

### 3. View Analytics
- Go to **Analytics Dashboard**
- Review data quality scores
- Explore visualizations
- Check anomalies
- Run what-if scenarios

### 4. Use AI Assistant
- Open **AI Assistant** page
- Ask questions in natural language
- Get instant insights
- View suggested queries

### 5. Configure Governance
- Visit **Data Governance** page
- Apply data masking
- Review audit logs
- Set access controls

### 6. Set Up Alerts
- Go to **Alerts & Automation**
- Configure email notifications
- Set up Slack/Teams webhooks
- Create automation rules

### 7. Collaborate
- Use **Collaboration** page
- Add comments to rows
- Create and assign tasks
- Track progress

### 8. View Predictions
- Navigate to **Predictive Analytics**
- Generate forecasts
- View trend projections
- Analyze risk factors

## 🔧 Configuration

### User Roles
The application supports 4 user roles:
- **Admin**: Full access to all features
- **HR**: Data management and employee information
- **Manager**: View access and analytics
- **Analyst**: Data analysis and export

### Data Masking
Automatically detects and masks:
- Email addresses
- Phone numbers
- SSN
- Aadhaar numbers
- PAN numbers
- Credit card numbers

### Supported File Formats

**Input:**
- PDF (text-based and scanned)
- PNG, JPG, JPEG (via OCR)
- TIFF images

**Output:**
- Excel (.xlsx)
- PDF reports
- Word (.docx) reports
- CSV (via audit logs)

## 📊 Analytics Features

### Data Quality Metrics
- **Completeness**: Percentage of non-null values
- **Consistency**: Data type and format consistency
- **Duplicate Risk**: Low/Medium/High
- **Anomaly Risk**: Statistical outlier risk
- **Validity**: Format validation (emails, phones, etc.)

### Visualizations
- Bar charts for distributions
- Line charts for trends
- Pie charts for categorical data
- Correlation heatmaps
- Box plots for outliers

### Predictive Models
- Linear regression for forecasting
- Trend analysis
- Risk scoring
- Budget projections

## 🔒 Security Features

### Data Protection
- Role-based access control
- Automatic PII masking
- Secure data handling
- Audit trail logging

### Compliance
- GDPR-ready features
- Data lineage tracking
- Access logs
- Export controls

## 🎨 Customization

### Themes
The application uses a professional blue theme. You can customize colors in the CSS section of `app.py`.

### Charts
Chart styles can be modified in the `excel_generator.py` and `dashboard_generator.py` modules.

### Masking Rules
Custom masking rules can be added in `modules/masking.py`.

## 🐛 Troubleshooting

### Common Issues

**Issue**: OCR not working
**Solution**: Install Tesseract OCR and ensure it's in your PATH

**Issue**: Charts not displaying in Excel
**Solution**: Ensure openpyxl is installed correctly

**Issue**: PDF parsing fails
**Solution**: Check if PDF is encrypted or corrupted

**Issue**: Memory errors with large files
**Solution**: Process files in batches or increase available RAM

## 📝 Best Practices

1. **Data Quality**: Always run quality checks before analysis
2. **Masking**: Enable automatic masking for sensitive data
3. **Backups**: Export audit logs regularly
4. **Testing**: Use sample data before production
5. **Documentation**: Comment complex mappings and transformations

## 🔄 Updates & Maintenance

### Regular Tasks
- Review audit logs weekly
- Update masking rules as needed
- Monitor data quality trends
- Archive old data periodically

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review audit logs for errors
3. Use the AI Assistant for quick help

## 📜 License

This is a demonstration application. Modify as needed for your organization.

## 🙏 Acknowledgments

Built with:
- Streamlit for the web framework
- Pandas for data manipulation
- Plotly for interactive charts
- OpenPyXL for Excel generation
- ReportLab for PDF generation
- scikit-learn for machine learning

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Status**: Production Ready ✅

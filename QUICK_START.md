# Quick Start Guide

## Installation (5 Minutes)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: (Optional) Install Tesseract OCR

**For scanned PDF support only**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### Step 3: Run the Application

**Option A - Quick Start:**
```bash
streamlit run app.py
```

**Option B - Using Start Script:**
```bash
chmod +x start.sh
./start.sh
```

### Step 4: Open in Browser

Navigate to: **http://localhost:8501**

---

## First Use

1. **Select Your Role** (sidebar)
   - Admin, HR, Manager, or Analyst

2. **Upload PDF** (Data Upload page)
   - Choose your PDF file
   - Click "Analyze PDF Structure"

3. **Process Data** (Data Processing page)
   - Configure column mappings
   - Apply transformations
   - Export to Excel

4. **View Analytics** (Analytics Dashboard)
   - Check data quality
   - View visualizations
   - Detect anomalies

5. **Ask Questions** (AI Assistant)
   - Type natural language queries
   - Get instant insights

---

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB
- **Browser**: Chrome, Firefox, Safari, or Edge

---

## File Structure After Installation

```
your-folder/
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── start.sh                 # Startup script
├── README.md                # Full documentation
├── USER_GUIDE.md            # Detailed user guide
└── modules/                 # Core modules
    ├── pdf_parser.py
    ├── schema_learner.py
    ├── intent_detector.py
    ├── anomaly_detector.py
    ├── data_quality.py
    ├── masking.py
    ├── audit_log.py
    ├── predictive_analytics.py
    ├── chatbot.py
    ├── excel_generator.py
    └── dashboard_generator.py
```

---

## Troubleshooting Quick Fixes

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### "Port already in use"
```bash
streamlit run app.py --server.port 8502
```

### "Permission denied" on start.sh
```bash
chmod +x start.sh
```

---

## Quick Feature Overview

✅ **PDF to Excel conversion** - Automatic parsing  
✅ **Custom column mapping** - Reorganize your data  
✅ **OCR support** - Scanned PDFs & images  
✅ **Data quality metrics** - Completeness, consistency  
✅ **Anomaly detection** - Automatic issue identification  
✅ **Data masking** - PII protection  
✅ **Audit logging** - Complete activity tracking  
✅ **AI chatbot** - Natural language queries  
✅ **Predictive analytics** - Forecasting & trends  
✅ **Interactive dashboards** - Charts & visualizations  
✅ **Excel export** - Professional formatting  
✅ **PDF/Word reports** - Dashboard export  
✅ **What-if analysis** - Scenario simulation  
✅ **Collaboration** - Comments & tasks  
✅ **Alerts** - Email & Slack/Teams  
✅ **Role-based access** - Security & compliance  

---

## Next Steps

1. Read the **USER_GUIDE.md** for detailed instructions
2. Check **README.md** for feature descriptions
3. Start with sample data to test features
4. Configure your role and preferences
5. Set up alerts and automation rules

---

## Support

- **AI Assistant**: Built-in help in the app
- **Documentation**: USER_GUIDE.md
- **README**: Full feature list

---

**Ready to go! 🚀**

Open your browser to **http://localhost:8501** and start analyzing!

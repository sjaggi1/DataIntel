import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import re
import json
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Import custom modules
from modules.pdf_parser import PDFParser
from modules.schema_learner import SchemaLearner
from modules.intent_detector import IntentDetector
from modules.anomaly_detector import AnomalyDetector
from modules.data_quality import DataQualityChecker
from modules.masking import DataMasker
from modules.audit_log import AuditLogger
from modules.predictive_analytics import PredictiveAnalytics
from modules.chatbot import ChatbotAssistant
from modules.excel_generator import ExcelGenerator
from modules.dashboard_generator import DashboardGenerator
from pathlib import Path

LOGO_PATH = Path("assets/logo.png")

# Page configuration
st.set_page_config(
    page_title="Enterprise Data Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0052a3;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    .alert-success {
        background-color: #d4edda;
        border-color: #28a745;
        color: #155724;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0066cc;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = AuditLogger()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'schema' not in st.session_state:
    st.session_state.schema = None
if 'masked_columns' not in st.session_state:
    st.session_state.masked_columns = []
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'Manager'
if 'comments' not in st.session_state:
    st.session_state.comments = {}
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

def main():
    # Sidebar navigation
    with st.sidebar:
        st.image(str(LOGO_PATH), width=200)
        st.markdown("---")
        
        # User role selection
        st.session_state.user_role = st.selectbox(
            "👤 User Role",
            ["Admin", "HR", "Manager", "Analyst"],
            index=2
        )
        
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "📤 Data Upload",
                "🔧 Data Processing",
                "📊 Analytics Dashboard",
                "🤖 AI Assistant",
                "🔒 Data Governance",
                "🔔 Alerts & Automation",
                "👥 Collaboration",
                "📈 Predictive Analytics",
                "⚙️ Settings"
            ]
        )
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        if st.session_state.df is not None:
            st.metric("Total Records", len(st.session_state.df))
            st.metric("Columns", len(st.session_state.df.columns))
        else:
            st.info("Upload data to see statistics")
    
    # Main content area
    if page == "🏠 Home":
        show_home_page()
    elif page == "📤 Data Upload":
        show_upload_page()
    elif page == "🔧 Data Processing":
        show_processing_page()
    elif page == "📊 Analytics Dashboard":
        show_analytics_page()
    elif page == "🤖 AI Assistant":
        show_chatbot_page()
    elif page == "🔒 Data Governance":
        show_governance_page()
    elif page == "🔔 Alerts & Automation":
        show_alerts_page()
    elif page == "👥 Collaboration":
        show_collaboration_page()
    elif page == "📈 Predictive Analytics":
        show_predictive_page()
    elif page == "⚙️ Settings":
        show_settings_page()

def show_home_page():
    st.title("📊 DataIntel")
    st.markdown("### Enterprise Data Intelligence Platform")
    st.markdown("### Transform PDF data into actionable insights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <h3>🚀 Quick Start</h3>
                <p>Upload your PDF files and let AI handle the rest</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <h3>🎯 AutoParse</h3>
                <p>Automatic schema detection and data parsing</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <h3>📈 Analytics</h3>
                <p>Real-time dashboards and predictive insights</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="metric-card">
                <h3>🔒 Secure</h3>
                <p>Enterprise-grade security and compliance</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature highlights
    st.markdown("### 🎯 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📄 Data Processing**
        - PDF to Excel conversion
        - Smart field detection
        - Custom column mapping
        - OCR for scanned documents
        - Image intelligence
        
        **🔍 Data Quality**
        - Anomaly detection
        - Duplicate identification
        - Data completeness check
        - Consistency validation
        """)
    
    with col2:
        st.markdown("""
        **🤖 AI-Powered**
        - Intent detection
        - Predictive analytics
        - Natural language chatbot
        - Automated insights
        
        **🔐 Governance**
        - Data masking
        - Role-based access
        - Audit logging
        - Compliance tracking
        """)
    
    st.markdown("---")
    
    # Recent activity
    if st.session_state.audit_log.logs:
        st.markdown("### 📋 Recent Activity")
        recent_logs = st.session_state.audit_log.get_recent_logs(5)
        for log in recent_logs:
            st.text(f"{log['timestamp']} - {log['action']} by {log['user']}")

def show_upload_page():
    st.title("📤 Data Upload & Import")
    
    tab1, tab2, tab3 = st.tabs(["📄 PDF Upload", "🖼️ Image/Scanned PDF", "⚙️ Upload Settings"])
    
    with tab1:
        st.markdown("### Upload PDF Files")
        
        uploaded_files = st.file_uploader(
            "Choose PDF file(s)",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF files containing structured data"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")
            
            # Delimiter detection
            st.markdown("#### Data Format Detection")
            delimiter_option = st.radio(
                "Select delimiter type:",
                ["Auto-detect", "Comma (,)", "Semicolon (;)", "Colon (:)", "Tab", "Mixed"],
                horizontal=True
            )
            
            custom_delimiter = None
            if delimiter_option == "Mixed":
                custom_delimiter = st.text_input("Enter custom delimiter pattern (regex):", value=r"[,;:]")
            
            if st.button("🔍 Analyze PDF Structure", type="primary"):
                with st.spinner("Analyzing PDF structure..."):
                    parser = PDFParser()
                    
                    for file in uploaded_files:
                        # Parse PDF
                        raw_data = parser.extract_text(file)
                        
                        # Detect schema
                        schema_learner = SchemaLearner()
                        detected_schema = schema_learner.learn_schema(raw_data)
                        st.session_state.schema = detected_schema
                        
                        # Preview
                        st.markdown("#### 📋 Detected Structure")
                        st.json(detected_schema)
                        
                        # Show sample data
                        st.markdown("#### 📊 Sample Data Preview")
                        sample_df = parser.parse_to_dataframe(
                            raw_data,
                            delimiter=custom_delimiter if delimiter_option == "Mixed" else delimiter_option
                        )
                        st.dataframe(sample_df.head(10), use_container_width=True)
                        
                        st.session_state.df = sample_df
                        st.session_state.audit_log.log_action("Data Upload", st.session_state.user_role, f"Uploaded {len(uploaded_files)} PDF file(s)")
    
    with tab2:
        st.markdown("### 🖼️ Image & Scanned PDF Intelligence")
        st.info("Upload scanned PDFs or images for OCR processing")
        
        image_files = st.file_uploader(
            "Choose image or scanned PDF",
            type=['pdf', 'png', 'jpg', 'jpeg', 'tiff'],
            accept_multiple_files=True
        )
        
        if st.button("🔍 Process with OCR", type="primary"):
            with st.spinner("Performing OCR..."):
                parser = PDFParser()

                for file in image_files:
                    file.seek(0)  # ✅ VERY IMPORTANT

                    st.subheader(f"📄 {file.name}")

                    # ✅ OCR extraction
                    ocr_text = parser.ocr_extract(
                        file,
                        language=ocr_language
                    )

                    st.text_area(
                        "Extracted Text",
                        ocr_text,
                        height=250
                    )

                    # ✅ Convert text → structured table
                    df = parser.parse_to_dataframe(ocr_text)

                    if not df.empty:
                        st.dataframe(df, use_container_width=True)
                        st.session_state.df = df
                    else:
                        st.warning("⚠️ No structured data detected")
    
    with tab3:
        st.markdown("### ⚙️ Upload Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Auto-process on upload", value=True)
            st.checkbox("Enable duplicate detection", value=True)
            st.checkbox("Auto-mask sensitive data", value=True)
        
        with col2:
            st.number_input("Max file size (MB)", value=50, min_value=1, max_value=500)
            st.selectbox("Default encoding", ["UTF-8", "Latin-1", "ASCII"])
            st.selectbox("Date format", ["Auto-detect", "DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])

def show_processing_page():
    st.title("🔧 Data Processing & Transformation")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload data first from the Data Upload page")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎨 Column Mapping",
        "🧹 Data Cleaning",
        "✨ Transformations",
        "💾 Export"
    ])
    
    with tab1:
        st.markdown("### 🎨 Custom Column Mapping")
        
        st.info("Define how you want to organize your Excel output")
        
        df = st.session_state.df
        available_columns = list(df.columns)
        
        st.markdown("#### Current Columns")
        st.write(available_columns)
        
        st.markdown("#### Create Custom Mappings")
        
        num_mappings = st.number_input("Number of output columns", min_value=1, max_value=20, value=len(available_columns))
        
        mappings = []
        for i in range(num_mappings):
            with st.expander(f"Column {i+1} Configuration"):
                col_name = st.text_input(f"Output column name", value=f"Column_{i+1}", key=f"name_{i}")
                
                selected_cols = st.multiselect(
                    "Source columns to combine",
                    available_columns,
                    key=f"cols_{i}"
                )
                
                separator = st.text_input("Separator (if combining)", value=" ", key=f"sep_{i}")
                
                transform = st.selectbox(
                    "Transformation",
                    ["None", "Uppercase", "Lowercase", "Title Case", "Trim", "Remove Special Chars"],
                    key=f"trans_{i}"
                )
                
                mappings.append({
                    'name': col_name,
                    'sources': selected_cols,
                    'separator': separator,
                    'transform': transform
                })
        
        if st.button("🎯 Apply Mapping", type="primary"):
            with st.spinner("Applying mappings..."):
                new_df = pd.DataFrame()
                
                for mapping in mappings:
                    if not mapping['sources']:
                        continue
                    
                    # Combine columns
                    if len(mapping['sources']) == 1:
                        new_df[mapping['name']] = df[mapping['sources'][0]]
                    else:
                        new_df[mapping['name']] = df[mapping['sources']].astype(str).agg(mapping['separator'].join, axis=1)
                    
                    # Apply transformation
                    if mapping['transform'] == 'Uppercase':
                        new_df[mapping['name']] = new_df[mapping['name']].str.upper()
                    elif mapping['transform'] == 'Lowercase':
                        new_df[mapping['name']] = new_df[mapping['name']].str.lower()
                    elif mapping['transform'] == 'Title Case':
                        new_df[mapping['name']] = new_df[mapping['name']].str.title()
                    elif mapping['transform'] == 'Trim':
                        new_df[mapping['name']] = new_df[mapping['name']].str.strip()
                    elif mapping['transform'] == 'Remove Special Chars':
                        new_df[mapping['name']] = new_df[mapping['name']].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
                
                st.session_state.processed_data = new_df
                st.success("✅ Mapping applied successfully!")
                st.dataframe(new_df.head(10), use_container_width=True)
    
    with tab2:
        st.markdown("### 🧹 Data Cleaning")
        
        df = st.session_state.processed_data if st.session_state.processed_data is not None else st.session_state.df
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Missing Values")
            missing = df.isnull().sum()
            missing_pct = (missing / len(df) * 100).round(2)
            missing_df = pd.DataFrame({
                'Column': missing.index,
                'Missing': missing.values,
                'Percentage': missing_pct.values
            })
            st.dataframe(missing_df, use_container_width=True)
            
            handle_missing = st.selectbox(
                "Handle missing values",
                ["Keep as is", "Remove rows", "Fill with mean", "Fill with median", "Fill with mode", "Fill with custom value"]
            )
            
            if handle_missing != "Keep as is" and st.button("Apply"):
                if handle_missing == "Remove rows":
                    df = df.dropna()
                elif handle_missing == "Fill with mean":
                    df = df.fillna(df.mean(numeric_only=True))
                elif handle_missing == "Fill with median":
                    df = df.fillna(df.median(numeric_only=True))
                elif handle_missing == "Fill with mode":
                    df = df.fillna(df.mode().iloc[0])
                
                st.session_state.processed_data = df
                st.success("✅ Missing values handled")
        
        with col2:
            st.markdown("#### Duplicate Detection")
            
            duplicates = df.duplicated().sum()
            st.metric("Duplicate Rows", duplicates)
            
            if duplicates > 0:
                if st.button("Remove Duplicates"):
                    df = df.drop_duplicates()
                    st.session_state.processed_data = df
                    st.success(f"✅ Removed {duplicates} duplicate rows")
            
            st.markdown("#### Data Types")
            dtypes_df = pd.DataFrame({
                'Column': df.dtypes.index,
                'Type': df.dtypes.values
            })
            st.dataframe(dtypes_df, use_container_width=True)
    
    with tab3:
        st.markdown("### ✨ Advanced Transformations")
        
        df = st.session_state.processed_data if st.session_state.processed_data is not None else st.session_state.df
        
        transformation_type = st.selectbox(
            "Select transformation",
            [
                "Date Parsing",
                "Text Extraction (Regex)",
                "Numeric Conversion",
                "Categorical Encoding",
                "Custom Function"
            ]
        )
        
        if transformation_type == "Date Parsing":
            date_col = st.selectbox("Select date column", df.columns)
            date_format = st.text_input("Date format (e.g., %Y-%m-%d)", value="%Y-%m-%d")
            
            if st.button("Parse Dates"):
                df[date_col] = pd.to_datetime(df[date_col], format=date_format, errors='coerce')
                st.session_state.processed_data = df
                st.success("✅ Dates parsed successfully")
        
        elif transformation_type == "Text Extraction (Regex)":
            text_col = st.selectbox("Select text column", df.columns)
            regex_pattern = st.text_input("Regex pattern", value=r"(\d+)")
            new_col_name = st.text_input("New column name", value="Extracted")
            
            if st.button("Extract"):
                df[new_col_name] = df[text_col].astype(str).str.extract(regex_pattern, expand=False)
                st.session_state.processed_data = df
                st.success("✅ Text extracted successfully")
    
    with tab4:
        st.markdown("### 💾 Export Data")
        
        df = st.session_state.processed_data if st.session_state.processed_data is not None else st.session_state.df
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Excel Export Options")
            
            include_charts = st.checkbox("Include dashboard charts", value=True)
            include_summary = st.checkbox("Include summary sheet", value=True)
            apply_formatting = st.checkbox("Apply professional formatting", value=True)
            
            excel_filename = st.text_input("Excel filename", value="employee_data.xlsx")
            
            if st.button("📊 Generate Excel", type="primary"):
                with st.spinner("Generating Excel file..."):
                    excel_gen = ExcelGenerator()
                    excel_file = excel_gen.create_excel(
                        df,
                        filename=excel_filename,
                        include_charts=include_charts,
                        include_summary=include_summary,
                        apply_formatting=apply_formatting
                    )
                    
                    st.success("✅ Excel file generated successfully!")
                    
                    # Download button
                    with open(excel_file, 'rb') as f:
                        st.download_button(
                            label="⬇️ Download Excel",
                            data=f,
                            file_name=excel_filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    st.session_state.audit_log.log_action("Excel Export", st.session_state.user_role, f"Generated {excel_filename}")
        
        with col2:
            st.markdown("#### Dashboard Export (PDF/Word)")
            
            dashboard_format = st.radio("Select format", ["PDF", "Word (DOCX)"])
            
            if st.button("📄 Generate Dashboard Report"):
                with st.spinner("Generating dashboard report..."):
                    dashboard_gen = DashboardGenerator()
                    report_file = dashboard_gen.create_report(
                        df,
                        format=dashboard_format.lower()
                    )
                    
                    st.success(f"✅ {dashboard_format} report generated!")
                    
                    with open(report_file, 'rb') as f:
                        st.download_button(
                            label=f"⬇️ Download {dashboard_format}",
                            data=f,
                            file_name=f"dashboard_report.{dashboard_format.lower()}",
                            mime=f"application/{dashboard_format.lower()}"
                        )

def show_analytics_page():
    st.title("📊 Analytics Dashboard")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload data first")
        return
    
    df = st.session_state.processed_data if st.session_state.processed_data is not None else st.session_state.df
    
    # Data Quality Score
    st.markdown("### 📈 Data Quality Score")
    
    quality_checker = DataQualityChecker()
    quality_scores = quality_checker.calculate_scores(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completeness = quality_scores['completeness']
        st.metric("Completeness", f"{completeness}%", delta=f"{completeness-90}%")
    
    with col2:
        consistency = quality_scores['consistency']
        st.metric("Consistency", f"{consistency}%", delta=f"{consistency-90}%")
    
    with col3:
        duplicate_risk = quality_scores['duplicate_risk']
        st.metric("Duplicate Risk", duplicate_risk)
    
    with col4:
        anomaly_risk = quality_scores['anomaly_risk']
        st.metric("Anomaly Risk", anomaly_risk)
    
    st.markdown("---")
    
    # Tabs for different analytics
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "📈 Trends",
        "🚨 Anomalies",
        "🎯 What-If Analysis",
        "🔍 Deep Dive"
    ])
    
    with tab1:
        show_overview_analytics(df)
    
    with tab2:
        show_trend_analytics(df)
    
    with tab3:
        show_anomaly_analytics(df)
    
    with tab4:
        show_whatif_analytics(df)
    
    with tab5:
        show_deep_dive_analytics(df)

def show_overview_analytics(df):
    st.markdown("### 📊 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(df))
    
    with col2:
        st.metric("Total Columns", len(df.columns))
    
    with col3:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        st.metric("Numeric Columns", len(numeric_cols))
    
    with col4:
        memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
        st.metric("Memory Usage", f"{memory_mb:.2f} MB")
    
    # Quick analytics
    st.markdown("#### Quick Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Select column for analysis
        selected_col = st.selectbox("Select column for analysis", df.columns)
        
        if df[selected_col].dtype in [np.int64, np.float64]:
            st.metric("Sum", f"{df[selected_col].sum():,.2f}")
            st.metric("Mean", f"{df[selected_col].mean():,.2f}")
            st.metric("Median", f"{df[selected_col].median():,.2f}")
            st.metric("Std Dev", f"{df[selected_col].std():,.2f}")
        else:
            st.metric("Unique Values", df[selected_col].nunique())
            st.metric("Most Common", df[selected_col].mode().values[0] if len(df[selected_col].mode()) > 0 else "N/A")
    
    with col2:
        # Distribution chart
        if df[selected_col].dtype in [np.int64, np.float64]:
            fig = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            value_counts = df[selected_col].value_counts().head(10)
            fig = px.bar(x=value_counts.index, y=value_counts.values, title=f"Top 10 {selected_col}")
            st.plotly_chart(fig, use_container_width=True)

def show_trend_analytics(df):
    st.markdown("### 📈 Trend Analysis")
    
    # Check for date columns
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    if not date_cols:
        # Try to find potential date columns
        potential_date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        
        if potential_date_cols:
            st.info("Found potential date columns. Converting...")
            for col in potential_date_cols:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    date_cols.append(col)
                except:
                    pass
    
    if date_cols:
        date_col = st.selectbox("Select date column", date_cols)
        metric_col = st.selectbox("Select metric to analyze", df.select_dtypes(include=[np.number]).columns)
        
        # Time-based aggregation
        freq = st.radio("Aggregation period", ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"], horizontal=True)
        
        freq_map = {
            "Daily": "D",
            "Weekly": "W",
            "Monthly": "M",
            "Quarterly": "Q",
            "Yearly": "Y"
        }
        
        trend_df = df.groupby(pd.Grouper(key=date_col, freq=freq_map[freq]))[metric_col].agg(['sum', 'mean', 'count']).reset_index()
        
        # Trend chart
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=trend_df[date_col], y=trend_df['sum'], name="Total", line=dict(color='#0066cc', width=3)),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=trend_df[date_col], y=trend_df['count'], name="Count", line=dict(color='#ff6b6b', width=2, dash='dash')),
            secondary_y=True
        )
        
        fig.update_layout(title=f"{metric_col} Trend Over Time", hovermode='x unified', height=400)
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text=f"Total {metric_col}", secondary_y=False)
        fig.update_yaxes(title_text="Count", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Growth rate
        if len(trend_df) > 1:
            growth_rate = ((trend_df['sum'].iloc[-1] - trend_df['sum'].iloc[0]) / trend_df['sum'].iloc[0] * 100)
            st.metric("Overall Growth Rate", f"{growth_rate:.2f}%")
    else:
        st.warning("No date columns found for trend analysis")

def show_anomaly_analytics(df):
    st.markdown("### 🚨 Anomaly Detection")
    
    detector = AnomalyDetector()
    anomalies = detector.detect_anomalies(df)
    
    if anomalies:
        # Summary
        st.markdown(f"""
            <div class="alert-box alert-warning">
                <strong>⚠️ {len(anomalies)} anomalies detected</strong>
            </div>
        """, unsafe_allow_html=True)
        
        # Display anomalies
        for anomaly in anomalies:
            with st.expander(f"⚠️ {anomaly['type']}: {anomaly['message']}"):
                st.write(f"**Severity:** {anomaly['severity']}")
                st.write(f"**Details:** {anomaly['details']}")
                
                if 'affected_rows' in anomaly:
                    st.write(f"**Affected rows:** {len(anomaly['affected_rows'])}")
                    st.dataframe(df.iloc[anomaly['affected_rows']].head(10))
    else:
        st.markdown("""
            <div class="alert-box alert-success">
                <strong>✅ No anomalies detected - Data looks good!</strong>
            </div>
        """, unsafe_allow_html=True)
    
    # Statistical outliers
    st.markdown("#### Statistical Outliers")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        outlier_col = st.selectbox("Select column for outlier detection", numeric_cols)
        
        method = st.radio("Detection method", ["IQR", "Z-Score"], horizontal=True)
        
        if method == "IQR":
            Q1 = df[outlier_col].quantile(0.25)
            Q3 = df[outlier_col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[outlier_col] < (Q1 - 1.5 * IQR)) | (df[outlier_col] > (Q3 + 1.5 * IQR))]
        else:
            z_scores = np.abs((df[outlier_col] - df[outlier_col].mean()) / df[outlier_col].std())
            outliers = df[z_scores > 3]
        
        st.metric("Outliers Found", len(outliers))
        
        if len(outliers) > 0:
            # Box plot
            fig = go.Figure()
            fig.add_trace(go.Box(y=df[outlier_col], name=outlier_col, marker_color='#0066cc'))
            fig.update_layout(title=f"Box Plot - {outlier_col}", height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(outliers, use_container_width=True)

def show_whatif_analytics(df):
    st.markdown("### 🧮 What-If Simulator")
    
    st.info("💡 Simulate changes and see their impact on your data")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            target_col = st.selectbox("Select column to modify", numeric_cols)
            
            modification_type = st.radio(
                "Modification type",
                ["Percentage Increase", "Percentage Decrease", "Add Fixed Amount", "Multiply by Factor"],
                horizontal=False
            )
            
            if "Percentage" in modification_type:
                change_value = st.slider("Change (%)", 0, 100, 10)
            else:
                change_value = st.number_input("Change value", value=1.0)
        
        with col2:
            st.markdown("#### Impact Analysis")
            
            # Calculate current metrics
            current_sum = df[target_col].sum()
            current_mean = df[target_col].mean()
            
            # Calculate what-if scenario
            if modification_type == "Percentage Increase":
                new_values = df[target_col] * (1 + change_value / 100)
            elif modification_type == "Percentage Decrease":
                new_values = df[target_col] * (1 - change_value / 100)
            elif modification_type == "Add Fixed Amount":
                new_values = df[target_col] + change_value
            else:  # Multiply
                new_values = df[target_col] * change_value
            
            new_sum = new_values.sum()
            new_mean = new_values.mean()
            
            # Display impact
            st.metric("Current Total", f"{current_sum:,.2f}")
            st.metric("New Total", f"{new_sum:,.2f}", delta=f"{new_sum - current_sum:,.2f}")
            
            st.metric("Current Average", f"{current_mean:,.2f}")
            st.metric("New Average", f"{new_mean:,.2f}", delta=f"{new_mean - current_mean:,.2f}")
        
        # Visualization
        comparison_df = pd.DataFrame({
            'Scenario': ['Current', 'What-If'],
            'Total': [current_sum, new_sum],
            'Average': [current_mean, new_mean]
        })
        
        fig = px.bar(comparison_df, x='Scenario', y=['Total', 'Average'], barmode='group',
                     title="Current vs What-If Scenario")
        st.plotly_chart(fig, use_container_width=True)

def show_deep_dive_analytics(df):
    st.markdown("### 🔍 Deep Dive Analytics")
    
    analysis_type = st.selectbox(
        "Select analysis type",
        [
            "Correlation Analysis",
            "Distribution Analysis",
            "Group-by Analysis",
            "Pivot Table",
            "Cross-tabulation"
        ]
    )
    
    if analysis_type == "Correlation Analysis":
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            
            fig = px.imshow(corr_matrix, 
                           text_auto='.2f',
                           aspect='auto',
                           color_continuous_scale='RdBu_r',
                           title="Correlation Matrix")
            st.plotly_chart(fig, use_container_width=True)
            
            # Find strong correlations
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.7:
                        strong_corr.append({
                            'Column 1': corr_matrix.columns[i],
                            'Column 2': corr_matrix.columns[j],
                            'Correlation': corr_matrix.iloc[i, j]
                        })
            
            if strong_corr:
                st.markdown("#### Strong Correlations (>0.7)")
                st.dataframe(pd.DataFrame(strong_corr), use_container_width=True)
    
    elif analysis_type == "Group-by Analysis":
        group_col = st.selectbox("Group by", df.columns)
        agg_col = st.selectbox("Aggregate column", df.select_dtypes(include=[np.number]).columns)
        agg_func = st.selectbox("Aggregation function", ["sum", "mean", "median", "count", "min", "max"])
        
        grouped = df.groupby(group_col)[agg_col].agg(agg_func).reset_index()
        grouped = grouped.sort_values(agg_col, ascending=False).head(20)
        
        fig = px.bar(grouped, x=group_col, y=agg_col, title=f"{agg_func.title()} of {agg_col} by {group_col}")
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(grouped, use_container_width=True)

def show_chatbot_page():
    st.title("🤖 AI Assistant")
    
    st.markdown("""
        <div class="alert-box alert-success">
            <strong>💬 Ask me anything about your data!</strong><br>
            I can help with analysis, insights, and data queries.
        </div>
    """, unsafe_allow_html=True)
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type the quick actions here.../Ask a question about your data..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chatbot = ChatbotAssistant()
                
                # Detect intent
                intent_detector = IntentDetector()
                intent = intent_detector.detect_intent(prompt)
                
                response = chatbot.generate_response(
                    prompt,
                    st.session_state.df,
                    intent
                )
                
                st.markdown(response)
                
                # Add assistant message
                st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Quick actions
    st.markdown("### 🎯 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Data Summary"):
            st.session_state.chat_history.append({"role": "user", "content": "Give me a summary of the data"})
    
    with col2:
        if st.button("🔍 Find Insights"):
            st.session_state.chat_history.append({"role": "user", "content": "What are the key insights from this data?"})
    
    with col3:
        if st.button("📈 Show Trends"):
            st.session_state.chat_history.append({"role": "user", "content": "Show me trends in the data"})
    
    with col4:
        if st.button("🚨 Detect Issues"):
            st.session_state.chat_history.append({"role": "user", "content": "Are there any data quality issues?"})

def show_governance_page():
    st.title("🔒 Data Governance & Compliance")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload data first")
        return
    
    tab1, tab2, tab3 = st.tabs(["🔐 Data Masking", "📋 Audit Log", "🎯 Access Control"])
    
    with tab1:
        st.markdown("### 🔐 Sensitive Data Masking")
        
        df = st.session_state.processed_data if st.session_state.processed_data is not None else st.session_state.df
        
        masker = DataMasker()
        
        # Auto-detect sensitive columns
        sensitive_cols = masker.detect_sensitive_columns(df)
        
        if sensitive_cols:
            st.markdown("""
                <div class="alert-box alert-warning">
                    <strong>⚠️ Detected potentially sensitive columns</strong>
                </div>
            """, unsafe_allow_html=True)
            
            for col_info in sensitive_cols:
                with st.expander(f"🔒 {col_info['column']} - {col_info['type']}"):
                    st.write(f"**Confidence:** {col_info['confidence']}%")
                    
                    mask_type = st.selectbox(
                        f"Masking method for {col_info['column']}",
                        ["Partial Mask", "Full Mask", "Hash", "Tokenize", "None"],
                        key=f"mask_{col_info['column']}"
                    )
                    
                    if mask_type != "None":
                        if st.button(f"Apply Masking", key=f"apply_{col_info['column']}"):
                            df[col_info['column']] = masker.apply_masking(
                                df[col_info['column']],
                                method=mask_type
                            )
                            st.session_state.masked_columns.append(col_info['column'])
                            st.success(f"✅ Masking applied to {col_info['column']}")
        
        # Preview masked data
        if st.session_state.masked_columns:
            st.markdown("#### Masked Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
    
    with tab2:
        st.markdown("### 📋 Audit Log")
        
        logs = st.session_state.audit_log.get_all_logs()
        
        if logs:
            # Filter options
            col1, col2 = st.columns(2)
            
            with col1:
                action_filter = st.multiselect(
                    "Filter by action",
                    options=list(set([log['action'] for log in logs])),
                    default=list(set([log['action'] for log in logs]))
                )
            
            with col2:
                user_filter = st.multiselect(
                    "Filter by user",
                    options=list(set([log['user'] for log in logs])),
                    default=list(set([log['user'] for log in logs]))
                )
            
            # Filter logs
            filtered_logs = [
                log for log in logs
                if log['action'] in action_filter and log['user'] in user_filter
            ]
            
            # Display logs
            log_df = pd.DataFrame(filtered_logs)
            st.dataframe(log_df, use_container_width=True)
            
            # Export audit log
            if st.button("📥 Export Audit Log"):
                csv = log_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="audit_log.csv",
                    mime="text/csv"
                )
        else:
            st.info("No audit logs yet")
    
    with tab3:
        st.markdown("### 🎯 Role-Based Access Control")
        
        st.info(f"Current Role: **{st.session_state.user_role}**")
        
        # Define permissions
        permissions = {
            'Admin': ['View All Data', 'Edit Data', 'Delete Data', 'Export Data', 'Manage Users', 'View Salary', 'Mask Data'],
            'HR': ['View All Data', 'Edit Data', 'Export Data', 'View Salary'],
            'Manager': ['View All Data', 'View Headcount', 'Basic Analytics','Edit Data', 'Delete Data', 'Export Data', 'Manage Users', 'View Salary', 'Mask Data'],
            'Analyst': ['View All Data', 'Basic Analytics', 'Export Data']
        }
        
        user_permissions = permissions.get(st.session_state.user_role, [])
        
        st.markdown("#### Your Permissions")
        for perm in user_permissions:
            st.markdown(f"✅ {perm}")
        
        st.markdown("---")
        
        # Column-level access
        st.markdown("#### Column-Level Access")
        
        df = st.session_state.df
        
        restricted_cols = []
        if st.session_state.user_role == 'Manager':
            restricted_cols = [col for col in df.columns if 'salary' in col.lower() or 'compensation' in col.lower()]
        
        if restricted_cols:
            st.warning(f"⚠️ Restricted columns for your role: {', '.join(restricted_cols)}")
        else:
            st.success("✅ You have access to all columns")

def show_alerts_page():
    st.title("🔔 Alerts & Automation")
    
    tab1, tab2 = st.tabs(["📧 Email Alerts", "🔄 Automation Rules"])
    
    with tab1:
        st.markdown("### 📧 Configure Email Alerts")
        
        st.checkbox("Enable email notifications", value=True)
        
        recipient_email = st.text_input("Recipient email", value="hr@company.com")
        
        st.markdown("#### Alert Triggers")
        
        st.checkbox("New PDF uploaded", value=True)
        st.checkbox("Data processing completed", value=True)
        st.checkbox("Anomalies detected", value=False)
        st.checkbox("Data quality score below threshold", value=False)
        
        threshold = st.slider("Quality score threshold (%)", 0, 100, 80)
        
        if st.button("💾 Save Alert Settings"):
            st.success("✅ Alert settings saved!")
        
        st.markdown("---")
        
        st.markdown("### 🔗 Slack/Teams Integration")
        
        platform = st.radio("Select platform", ["Slack", "Microsoft Teams"], horizontal=True)
        
        webhook_url = st.text_input(f"{platform} Webhook URL", type="password")
        
        if st.button(f"Test {platform} Integration"):
            st.info(f"📤 Sending test message to {platform}...")
            # In real implementation, this would send a message
            st.success(f"✅ Test message sent to {platform}!")
    
    with tab2:
        st.markdown("### 🔄 Automation Rules")
        
        st.markdown("#### Create New Rule")
        
        rule_name = st.text_input("Rule name", value="Auto-process employee data")
        
        trigger = st.selectbox(
            "Trigger",
            [
                "When new PDF is uploaded",
                "On schedule (daily/weekly)",
                "When data quality score changes",
                "When anomaly is detected"
            ]
        )
        
        st.markdown("#### Actions")
        
        actions = st.multiselect(
            "Select actions to perform",
            [
                "Convert to Excel",
                "Generate dashboard",
                "Send email notification",
                "Mask sensitive data",
                "Run data quality check",
                "Create backup"
            ]
        )
        
        if st.button("✅ Create Rule"):
            st.success(f"✅ Rule '{rule_name}' created successfully!")
        
        st.markdown("---")
        
        st.markdown("#### Existing Rules")
        
        # Sample rules
        rules_df = pd.DataFrame({
            'Rule': ['Auto-process uploads', 'Daily quality check', 'Anomaly alert'],
            'Trigger': ['New upload', 'Schedule: Daily 9 AM', 'Anomaly detected'],
            'Status': ['Active', 'Active', 'Active'],
            'Last Run': ['2 hours ago', '3 hours ago', 'Never']
        })
        
        st.dataframe(rules_df, use_container_width=True)

def show_collaboration_page():
    st.title("👥 Collaboration & Task Management")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload data first")
        return
    
    tab1, tab2 = st.tabs(["💬 Comments", "✅ Tasks"])
    
    with tab1:
        st.markdown("### 💬 Row Comments")
        
        df = st.session_state.processed_data if st.session_state.processed_data is not None else st.session_state.df
        
        st.dataframe(df.head(10), use_container_width=True)
        
        row_num = st.number_input("Select row to comment on", min_value=0, max_value=len(df)-1, value=0)
        
        comment_text = st.text_area("Add comment", placeholder="E.g., Verify this salary amount")
        
        if st.button("💬 Add Comment"):
            if row_num not in st.session_state.comments:
                st.session_state.comments[row_num] = []
            
            st.session_state.comments[row_num].append({
                'user': st.session_state.user_role,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'text': comment_text
            })
            
            st.success("✅ Comment added!")
        
        # Display comments for selected row
        if row_num in st.session_state.comments:
            st.markdown(f"#### Comments for Row {row_num}")
            
            for comment in st.session_state.comments[row_num]:
                st.markdown(f"""
                    <div class="alert-box alert-success">
                        <strong>{comment['user']}</strong> - {comment['timestamp']}<br>
                        {comment['text']}
                    </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### ✅ Task Management")
        
        st.markdown("#### Create New Task")
        
        col1, col2 = st.columns(2)
        
        with col1:
            task_title = st.text_input("Task title", placeholder="E.g., Confirm employee ID")
            task_assignee = st.selectbox("Assign to", ["HR", "Manager", "Admin", "Analyst"])
        
        with col2:
            task_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            task_due_date = st.date_input("Due date")
        
        task_description = st.text_area("Description")
        
        if st.button("➕ Create Task"):
            st.session_state.tasks.append({
                'title': task_title,
                'assignee': task_assignee,
                'priority': task_priority,
                'due_date': task_due_date,
                'description': task_description,
                'status': 'Open',
                'created_by': st.session_state.user_role,
                'created_at': datetime.now()
            })
            
            st.success("✅ Task created!")
        
        st.markdown("---")
        
        st.markdown("#### Active Tasks")
        
        if st.session_state.tasks:
            for idx, task in enumerate(st.session_state.tasks):
                with st.expander(f"{'🔴' if task['priority'] == 'Critical' else '🟡' if task['priority'] == 'High' else '🟢'} {task['title']}"):
                    st.write(f"**Assignee:** {task['assignee']}")
                    st.write(f"**Priority:** {task['priority']}")
                    st.write(f"**Due Date:** {task['due_date']}")
                    st.write(f"**Status:** {task['status']}")
                    st.write(f"**Description:** {task['description']}")
                    
                    if st.button(f"Mark as Complete", key=f"complete_{idx}"):
                        st.session_state.tasks[idx]['status'] = 'Completed'
                        st.success("✅ Task marked as complete!")
        else:
            st.info("No tasks yet")

def show_predictive_page():
    st.title("📈 Predictive Analytics")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload data first")
        return
    
    df = st.session_state.processed_data if st.session_state.processed_data is not None else st.session_state.df
    
    tab1, tab2, tab3 = st.tabs(["📊 Forecasting", "🎯 Predictions", "📉 Trend Projections"])
    
    with tab1:
        st.markdown("### 📊 Time Series Forecasting")
        
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        if date_cols:
            date_col = st.selectbox("Select date column", date_cols)
            metric_col = st.selectbox("Select metric to forecast", df.select_dtypes(include=[np.number]).columns)
            
            forecast_periods = st.slider("Forecast periods ahead", 1, 12, 3)
            
            if st.button("🔮 Generate Forecast"):
                with st.spinner("Generating forecast..."):
                    predictor = PredictiveAnalytics()
                    forecast = predictor.forecast_timeseries(
                        df,
                        date_col,
                        metric_col,
                        periods=forecast_periods
                    )
                    
                    # Plot forecast
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=df[date_col],
                        y=df[metric_col],
                        mode='lines+markers',
                        name='Actual',
                        line=dict(color='#0066cc', width=2)
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=forecast['date'],
                        y=forecast['forecast'],
                        mode='lines+markers',
                        name='Forecast',
                        line=dict(color='#ff6b6b', width=2, dash='dash')
                    ))
                    
                    fig.update_layout(
                        title=f"{metric_col} Forecast",
                        xaxis_title="Date",
                        yaxis_title=metric_col,
                        hovermode='x unified',
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Forecast table
                    st.markdown("#### Forecast Values")
                    st.dataframe(forecast, use_container_width=True)
    
    with tab2:
        st.markdown("### 🎯 Predictive Insights")
        
        st.markdown("#### Hiring Trend Forecast")
        st.info("Based on historical data, predict future hiring needs")
        
        # Sample prediction
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Predicted Hires (Next Quarter)", "15-18", delta="+3")
        
        with col2:
            st.metric("Attrition Risk", "5.2%", delta="-1.1%")
        
        with col3:
            st.metric("Headcount Growth", "+12%", delta="+2%")
        
        st.markdown("#### Salary Budget Projection")
        
        # Sample projection chart
        months = pd.date_range(start='2026-01-01', periods=12, freq='M')
        projected_budget = [1000000 + i*50000 + np.random.randint(-20000, 20000) for i in range(12)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=projected_budget,
            mode='lines+markers',
            name='Projected Budget',
            fill='tozeroy',
            line=dict(color='#0066cc', width=3)
        ))
        
        fig.update_layout(
            title="Salary Budget Projection - Next 12 Months",
            xaxis_title="Month",
            yaxis_title="Budget ($)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 📉 Advanced Trend Analysis")
        
        st.markdown("#### Attrition Prediction Model")
        
        st.info("📊 ML model predicts employee attrition risk")
        
        # Sample risk factors
        risk_factors = pd.DataFrame({
            'Factor': ['Tenure < 1 year', 'No promotion in 2 years', 'Salary below market', 'Low engagement score', 'Manager change'],
            'Impact': [0.35, 0.28, 0.42, 0.38, 0.22],
            'Employees Affected': [12, 8, 15, 10, 5]
        })
        
        fig = px.bar(risk_factors, x='Factor', y='Impact', color='Employees Affected',
                     title="Attrition Risk Factors",
                     color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Recommended Actions")
        
        st.markdown("""
        - 🎯 **Review compensation** for 15 employees below market rate
        - 📈 **Career development** discussions for 8 employees without recent promotion
        - 💬 **Engagement survey** for low-scoring team members
        - 🤝 **Mentorship program** for employees with new managers
        """)

def show_settings_page():
    st.title("⚙️ Settings & Preferences")
    
    tab1, tab2, tab3 = st.tabs(["👤 User Preferences", "🎨 Display", "🔧 Advanced"])
    
    with tab1:
        st.markdown("### 👤 User Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Name", value="John Doe")
            st.text_input("Email", value="john.doe@company.com")
            st.selectbox("Department", ["HR", "Finance", "IT", "Operations"])
        
        with col2:
            st.selectbox("Timezone", ["UTC", "EST", "PST", "IST"])
            st.selectbox("Date Format", ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"])
            st.selectbox("Number Format", ["1,234.56", "1.234,56"])
        
        if st.button("💾 Save Preferences"):
            st.success("✅ Preferences saved!")
    
    with tab2:
        st.markdown("### 🎨 Display Settings")
        
        theme = st.radio("Theme", ["Light", "Dark", "Auto"], horizontal=True)
        
        st.slider("Chart animation speed", 0, 100, 50)
        
        st.checkbox("Show data tooltips", value=True)
        st.checkbox("Enable animations", value=True)
        st.checkbox("Compact view", value=False)
        
        if st.button("💾 Save Display Settings"):
            st.success("✅ Display settings saved!")
    
    with tab3:
        st.markdown("### 🔧 Advanced Settings")
        
        st.number_input("Max rows to display", value=1000, min_value=100, max_value=100000)
        
        st.number_input("Cache duration (hours)", value=24, min_value=1, max_value=168)
        
        st.checkbox("Enable debug mode", value=False)
        st.checkbox("Enable performance logging", value=False)
        
        st.markdown("#### Data Export Defaults")
        
        st.selectbox("Default Excel format", [".xlsx", ".xls"])
        st.selectbox("Default CSV encoding", ["UTF-8", "Latin-1", "ASCII"])
        
        if st.button("💾 Save Advanced Settings"):
            st.success("✅ Advanced settings saved!")
        
        st.markdown("---")
        
        st.markdown("### 🗑️ Data Management")
        
        if st.button("🔄 Clear Cache", type="secondary"):
            st.cache_data.clear()
            st.success("✅ Cache cleared!")
        
        if st.button("📥 Export All Settings", type="secondary"):
            settings = {
                'user_role': st.session_state.user_role,
                'masked_columns': st.session_state.masked_columns
            }
            st.download_button(
                label="Download Settings",
                data=json.dumps(settings, indent=2),
                file_name="settings.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()

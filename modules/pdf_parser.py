import PyPDF2
import pandas as pd
import re
from io import BytesIO
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

class PDFParser:
    """Handles PDF text extraction and parsing"""
    def remove_repeated_header_rows(self, df):
        """
        Remove rows where values exactly match column names
        (common in PDFs where headers repeat on each page)
        """
        if df.empty:
            return df

        col_names = list(df.columns)

        df_clean = df[
            ~df.apply(
                lambda row: all(
                    str(row[i]).strip() == str(col_names[i]).strip()
                    for i in range(len(col_names))
                ),
                axis=1
            )
        ]

        df_clean = df_clean.reset_index(drop=True)
        return df_clean

    
    # def extract_text(self, pdf_file):
    #     """Extract text from PDF file"""
    #     try:
    #         pdf_reader = PyPDF2.PdfReader(pdf_file)
    #         text = ""
            
    #         for page in pdf_reader.pages:
    #             text += page.extract_text()
            
    #         return text
    #     except Exception as e:
    #         return f"Error extracting text: {str(e)}"
    def extract_text(self, pdf_file):
        """Extract text from ALL pages of a PDF (safe for multipage)"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_pages = []

            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text)

            return "\n".join(text_pages)

        except Exception as e:
            return f"Error extracting text: {str(e)}"

    
    # def ocr_extract(self, file, language="English"):
    #     """Extract text from scanned PDF or image using OCR"""
    #     try:
    #         if file.type == 'application/pdf':
    #             # Convert PDF to images
    #             images = convert_from_bytes(file.read())
    #             text = ""
                
    #             for image in images:
    #                 text += pytesseract.image_to_string(image, lang='eng')
                
    #             return text
    #         else:
    #             # Direct image OCR
    #             image = Image.open(file)
    #             text = pytesseract.image_to_string(image, lang='eng')
    #             return text
    #     except Exception as e:
    #         return f"OCR Error: {str(e)}\nNote: Tesseract OCR may not be installed. Using basic extraction."
    
    def ocr_extract(self, file, language="English"):
        """Extract text from scanned PDF or image using OCR (multi-page safe)"""
        try:
            if file.type == 'application/pdf':
                file_bytes = file.read()  # 🔥 read ONCE
                images = convert_from_bytes(file_bytes)

                text_pages = []
                for image in images:
                    text_pages.append(
                        pytesseract.image_to_string(image, lang='eng')
                    )

                return "\n".join(text_pages)

            else:
                image = Image.open(file)
                return pytesseract.image_to_string(image, lang='eng')

        except Exception as e:
            return f"OCR Error: {str(e)}"

    
    def parse_to_dataframe(self, text, delimiter="Auto-detect"):
        """Parse text to pandas DataFrame"""
        try:
            # Split into lines
            # lines = text.strip().split('\n')
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            
            if not lines:
                return pd.DataFrame()
            
            # Determine delimiter
            if delimiter == "Auto-detect":
                # Count occurrences of common delimiters
                delimiters = {',': 0, ';': 0, ':': 0, '\t': 0}
                for line in lines[:5]:  # Check first 5 lines
                    for delim in delimiters:
                        delimiters[delim] += line.count(delim)
                
                # Use most common delimiter
                delimiter = max(delimiters, key=delimiters.get)
            elif delimiter == "Comma (,)":
                delimiter = ','
            elif delimiter == "Semicolon (;)":
                delimiter = ';'
            elif delimiter == "Colon (:)":
                delimiter = ':'
            elif delimiter == "Tab":
                delimiter = '\t'
            
            # Parse lines
            data = []
            headers = None
            
            for line in lines:
                if not line.strip():
                    continue
                
                # Split by delimiter
                if isinstance(delimiter, str) and delimiter in [',', ';', ':', '\t']:
                    parts = line.split(delimiter)
                else:
                    # Use regex for mixed delimiters
                    parts = re.split(r'[,;:\t]+', line)
                
                parts = [p.strip() for p in parts if p.strip()]
                
                if parts:
                    if headers is None:
                        headers = parts
                    else:
                        data.append(parts)
            
            # Create DataFrame
            if headers and data:
                # Ensure all rows have same length as headers
                max_len = len(headers)
                data_clean = []
                
                for row in data:
                    if len(row) < max_len:
                        row.extend([''] * (max_len - len(row)))
                    elif len(row) > max_len:
                        row = row[:max_len]
                    data_clean.append(row)
                
                df = pd.DataFrame(data_clean, columns=headers)

                # 🔥 REMOVE REPEATED HEADER ROWS
                df = self.remove_repeated_header_rows(df)
                if 'Salary' in df.columns:
                    df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')
                return df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Parsing error: {str(e)}")
            return pd.DataFrame()
    
    def smart_parse(self, text):
        """Intelligently parse semi-structured text"""
        # Try to detect patterns
        patterns = {
            'key_value': re.compile(r'([A-Za-z\s]+):\s*([^:\n]+)'),
            'table': re.compile(r'\|(.+)\|'),
            'csv': re.compile(r'[,;]\s*')
        }
        
        # Detect format
        if patterns['table'].search(text):
            # Markdown table format
            return self._parse_markdown_table(text)
        elif patterns['key_value'].findall(text):
            # Key-value pairs
            return self._parse_key_value(text)
        else:
            # Default CSV-like parsing
            return self.parse_to_dataframe(text)
    
    def _parse_markdown_table(self, text):
        """Parse markdown-style table"""
        lines = text.strip().split('\n')
        table_lines = [l for l in lines if '|' in l]
        
        if len(table_lines) < 2:
            return pd.DataFrame()
        
        # Extract headers
        headers = [h.strip() for h in table_lines[0].split('|')[1:-1]]
        
        # Extract data (skip separator line)
        data = []
        for line in table_lines[2:]:
            row = [c.strip() for c in line.split('|')[1:-1]]
            data.append(row)
        
        return pd.DataFrame(data, columns=headers)
    
    def _parse_key_value(self, text):
        """Parse key-value pair format"""
        pattern = re.compile(r'([A-Za-z\s]+):\s*([^:\n]+)')
        matches = pattern.findall(text)
        
        if matches:
            df = pd.DataFrame(matches, columns=['Key', 'Value'])
            return df
        
        return pd.DataFrame()

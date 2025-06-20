# AI Contract Clause Risk Analyzer (MVP)

This is a rapid prototype for an AI-powered tool that analyzes legal contracts for risky clauses using keyword-based detection.

## Features
- Upload contracts in PDF, DOCX, or TXT format
- Extracts text (with OCR for scanned PDFs)
- Identifies and highlights risky clauses (High, Medium, Low risk)
- Simple, interactive dashboard (Streamlit UI)

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) For OCR, install Tesseract:
   - Windows: Download from https://github.com/tesseract-ocr/tesseract
   - Linux: `sudo apt-get install tesseract-ocr`
3. Start the app:
   ```bash
   streamlit run app/main.py
   ```

## Project Structure

- `app/main.py` - Streamlit UI
- `app/analyzer.py` - Clause extraction & risk analysis
- `app/file_utils.py` - File upload & text extraction
- `app/risk_keywords.py` - Risk keyword lists 
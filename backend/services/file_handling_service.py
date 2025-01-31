import pdfminer.high_level
import pandas as pd
from docx import Document
import csv

def pdf_to_text(pdf_path):
    try:
        text = pdfminer.high_level.extract_text(pdf_path)
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def csv_to_text(csv_path):
    try:
        df = pd.read_csv(csv_path)
        return df.to_string(index=False)
    except Exception as e:
        return f"Error reading CSV: {str(e)}"


def doc_to_text(doc_path):
    try:
        doc = Document(doc_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
    except Exception as e:
        return f"Error reading DOC/DOCX: {str(e)}"

import os
import re
import csv
from pathlib import Path
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """Extract text from a given PDF file."""
    reader = PdfReader(pdf_path)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def extract_invoice_data(text):
    """Extract invoice number, total amount, due date, and vendor name from text."""
    data = {
        "Invoice Number": None,
        "Total Amount": None,
        "Due Date": None,
        "Vendor Name": None
    }

    # Regex patterns (adjust as needed)
    invoice_pattern = re.search(r"Invoice\s*No[:#]?\s*(\S+)", text, re.IGNORECASE)
    amount_pattern = re.search(r"Total\s*Amount[:#]?\s*[$]?([0-9,]+\.\d{2})", text, re.IGNORECASE)
    due_date_pattern = re.search(r"Due\s*Date[:#]?\s*(\d{2}/\d{2}/\d{4})", text, re.IGNORECASE)
    vendor_pattern = re.search(r"Vendor[:#]?\s*(.+)\n", text, re.IGNORECASE)

    # Assign extracted values
    if invoice_pattern:
        data["Invoice Number"] = invoice_pattern.group(1)
    if amount_pattern:
        data["Total Amount"] = amount_pattern.group(1)
    if due_date_pattern:
        data["Due Date"] = due_date_pattern.group(1)
    if vendor_pattern:
        data["Vendor Name"] = vendor_pattern.group(1).strip()

    return data

def process_bills(directory):
    """Process all PDFs in the given directory and extract structured invoice data."""
    extracted_data = []

    pdf_files = Path(directory).glob("*.pdf")
    for pdf in pdf_files:
        print(f"Processing: {pdf.name}")
        text = extract_text_from_pdf(pdf)
        data = extract_invoice_data(text)
        extracted_data.append(data)

    return extracted_data

def save_to_csv(data, output_file):
    """Save extracted data to a CSV file."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Invoice Number", "Total Amount", "Due Date", "Vendor Name"])
        writer.writeheader()
        writer.writerows(data)

def main():
    bills_directory = os.path.expanduser("~/Documents/Downloaded Bills")
    output_csv = os.path.expanduser("~/Documents/Extracted_Bills_Data.csv")

    print("Starting extraction...")
    extracted_data = process_bills(bills_directory)
    save_to_csv(extracted_data, output_csv)
    print(f"Extraction complete! Data saved to: {output_csv}")

if __name__ == "__main__":
    main()

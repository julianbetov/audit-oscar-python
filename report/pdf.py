from pathlib import Path

import pdfkit


def save_html(html_page: str, html_path: str = "audit_results.html") -> str:
    Path(html_path).write_text(html_page, encoding="utf-8")
    return html_path

def render_pdf_bytes(html_page: str) -> bytes:
    config = pdfkit.configuration(wkhtmltopdf=r"c:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf_bytes: bytes = pdfkit.from_string(html_page, output_path=False, configuration=config)
    return pdf_bytes

# def save_html_as_pdf(html_page: str, pdf_filename: str = "complete_audit.pdf") -> str:
#     config = pdfkit.configuration(wkhtmltopdf=r"c:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
#     pdfkit.from_string(html_page, pdf_filename, configuration=config)
#     return pdf_filename

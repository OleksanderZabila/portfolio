"""Convert the generated CV.docx to PDF using docx2pdf (Word COM)."""
from pathlib import Path
from docx2pdf import convert

src = Path(r"C:\Users\ukzab\Desktop\CV_Junior_Python_Developer_Aleksandr_Zabila_May2026_Eng.docx")
dst = src.with_suffix(".pdf")
print(f"Converting:\n  {src}\n  -> {dst}")
convert(str(src), str(dst))
print("PDF created" if dst.exists() else "Failed")

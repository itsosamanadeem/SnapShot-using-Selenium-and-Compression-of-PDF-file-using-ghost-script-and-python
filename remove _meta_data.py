from pypdf import PdfReader , PdfWriter

reader= PdfReader("sample.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)
writer.add_metadata(reader.metadata)

with open("Removed_metadata.pdf", "wb") as f:
    writer.write(f)
    
from pypdf import PdfReader, PdfWriter

def compress_pdf(input_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    for page in writer.pages:
        for img in page.images:
            img.replace(img.image, quality=0)
        page.compress_content_streams(level=9)

    writer.add_metadata(reader.metadata)
    with open("out.pdf", "wb") as f:
        writer.write(f)

input_file = "sample.pdf"
compress_pdf(input_file)

from pypdf import PdfReader, PdfWriter

def compress_pdf(input_pdf_path, output_pdf_path, compress_percentage):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    for page in writer.pages:
        writer.add_page(page)
        page.compress_content_streams(level=9)
        for img in page.images:
            img.replace(img.image, quality=compress_percentage)
    writer.add_metadata(reader.metadata)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

input_file = "Free_Test_Data_10.5MB_PDF (1).pdf"
output_file = "output.pdf"
compression_percentage = int(input("Enter the percentage you want the file to compress at: "))
compress_pdf(input_file, output_file, compression_percentage)

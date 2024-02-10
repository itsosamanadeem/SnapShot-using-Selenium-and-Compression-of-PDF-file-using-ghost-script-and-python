import PyPDF2
import shutil

def rotate(rotate_angle, pdf_path):
    pdf_open = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_open)
    pdf_writer = PyPDF2.PdfWriter()

    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        if rotate_angle == 'r':
            page.rotat(90)
        elif rotate_angle == 'b':
            page.rotate(180)
        elif rotate_angle == 'l':
            page.rotate(270)
        elif rotate_angle == 't':
            page.rotate(360)

        pdf_writer.add_page(page)

    pdf_output = open('output.pdf', 'wb')
    pdf_writer.write(pdf_output)

    pdf_open.close()
    pdf_output.close()

    shutil.move('output.pdf', pdf_path)

pdf_path = input("Enter PDF name: ")
rotate_angle = input("Enter rotation angle (r/l/b/t): ").lower()
rotate(rotate_angle, pdf_path)

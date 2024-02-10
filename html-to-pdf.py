from selenium import webdriver
from PIL import Image
import tempfile
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas

def capture_screenshot(view_type):
    # Set user agent based on view_type
    if view_type == 1:  # Mobile view
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1"
        window_width = 380
        output_filename = "Mobile_view.png"
    elif view_type == 2:  # Desktop view
        user_agent = None
        window_width = 1920
        output_filename = "Desktop_view.png"
    else:
        print("Invalid input.")
        return

    # Set user agent for mobile view
    firefox_options = webdriver.FirefoxOptions()
    if user_agent:
        firefox_options.set_preference("devtools.responsive.userAgentString", user_agent)

    # Start Firefox WebDriver
    driver = webdriver.Firefox(options=firefox_options)
    driver.maximize_window()

    # Navigate to the website
    driver.get("https://www.ilovepdf2.com/")

    # Get the size of the page
    s = driver.get_window_size()
    h = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

    # Set window size to capture full page
    driver.set_window_size(window_width, h)

    # Capture full page screenshot
    driver.get_full_page_screenshot_as_file(output_filename)

    # Quit WebDriver
    driver.quit()

    # Convert screenshot to PDF
    png_to_pdf([output_filename], output_filename.replace(".png", ".pdf"))

def png_to_pdf(png_files, pdf_output, orientation='portrait', page_size='fit', margin='no_margin'):
    for png_file in png_files:
        img = Image.open(png_file)
        img_width, img_height = img.size

        if page_size == 'fit':
            page_width = img_width
            page_height = img_height
        elif page_size == 'A4':
            page_width, page_height = A4
        elif page_size == 'Letter':
            page_width, page_height = letter

        if margin == 'no_margin':
            page_width += 0  # Adjust page width for no margin
            page_height += 0  # Adjust page height for no margin
            left_margin = right_margin = top_margin = bottom_margin = 0
        elif margin == 'small':
            left_margin = right_margin = top_margin = bottom_margin = 20
        elif margin == 'big':
            left_margin = right_margin = top_margin = bottom_margin = 40

        if orientation == 'landscape':
            page_width, page_height = page_height, page_width  # Swap width and height for landscape orientation
            img = img.transpose(Image.ROTATE_270)  # Rotate the image 90 degrees for landscape
        
        c = canvas.Canvas(pdf_output, pagesize=(page_width, page_height))

        # Create a temporary PNG file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_png:
            img.save(temp_png, format="PNG")
            temp_png_path = temp_png.name

            # Calculate the scaled image dimensions
            img_width, img_height = img.size
            scale_factor_width = (page_width - left_margin - right_margin) / img_width
            scale_factor_height = (page_height - top_margin - bottom_margin) / img_height
            scale_factor = min(scale_factor_width, scale_factor_height)

            # Calculate the scaled image position to center it on the page
            scaled_img_width = img_width * scale_factor
            scaled_img_height = img_height * scale_factor
            x = (page_width - scaled_img_width) / 2
            y = (page_height - scaled_img_height) / 2

            # Add the temporary PNG image to the PDF with scaling
            c.drawImage(temp_png_path, x, y, width=scaled_img_width, height=scaled_img_height)

        c.showPage()
        c.save()

# Main program
user_choice = int(input("Enter 1 for mobile view or 2 for desktop view: "))
capture_screenshot(user_choice)

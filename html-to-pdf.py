from selenium import webdriver
from fpdf import FPDF
from PIL import Image
import os

firefox_options = webdriver.FirefoxOptions()
firefox_options.set_preference("devtools.responsive.userAgentString", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1")

driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()

driver.get("https://www.ilovepdf2.com/")
w=390 
h = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
driver.set_window_size(w,h)
driver.get_full_page_screenshot_as_file("osama1.png")

# image = Image.open("osama1.png")

# # Create a PDF document
# pdf = FPDF()
# pdf.add_page()

# # Calculate aspect ratio for the image
# aspect_ratio = image.width / float(image.height)

# # Calculate width and height of the image in points
# width = 210  # Width of A4 paper in mm
# height = width / aspect_ratio

# # Add the image to the PDF document
# pdf.image("osama1.png", x=0, y=0, w=width, h=height)

# # Save the PDF file
# pdf.output("osama1.pdf")

# Optionally, remove the captured screenshot
# os.remove("osama1.png")
driver.quit()

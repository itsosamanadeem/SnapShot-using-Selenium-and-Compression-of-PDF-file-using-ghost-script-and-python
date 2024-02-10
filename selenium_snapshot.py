from selenium import webdriver
from fpdf import FPDF
from PIL import Image
import os

# Set user agent for mobile view
firefox_options = webdriver.FirefoxOptions()
firefox_options.set_preference("devtools.responsive.userAgentString", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1")

# Start Firefox WebDriver
driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()

# Navigate to the website
driver.get("https://www.ilovepdf2.com/")

# Get the size of the page
s = driver.get_window_size()
w = 1920 
h = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

# Set window size to capture full page
driver.set_window_size(w, h)

# Capture full page screenshot
driver.get_full_page_screenshot_as_file("full_page_screenshot.png")

# Quit WebDriver
driver.quit()

# Open captured screenshot
image = Image.open("full_page_screenshot.png")

# Create a PDF document
pdf = FPDF()
pdf.add_page()

# Calculate aspect ratio for the image
aspect_ratio = image.width / float(image.height)

# Calculate width and height of the image in points
width = 210  # Width of A4 paper in mm
height = width / aspect_ratio

# Add the image to the PDF document
pdf.image("full_page_screenshot.png", x=0, y=0, w=width, h=height)

# Save the PDF file
pdf.output("full_page_screenshot.pdf")

# Optionally, remove the captured screenshot
os.remove("full_page_screenshot.png")

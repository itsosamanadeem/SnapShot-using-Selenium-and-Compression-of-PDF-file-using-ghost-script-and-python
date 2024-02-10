import base64
import json
import time
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

class PdfGenerator:
    driver = None
    mobile_print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
        'preferCSSPageSize': True,
        'paperWidth': 5.83,
        'paperHeight': 8.27,
    }

    desktop_print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
        'preferCSSPageSize': True,
        'paperWidth': 9.97,
        'paperHeight': 16.5,
    }

    def __init__(self):
        self.urls = []

    def _get_pdf_from_url(self, url, print_options):
        self.driver.get(url)
        time.sleep(0.3)  # allow the page to load, increase if needed
        screenshot = self._send_devtools(self.driver, "Page.captureScreenshot", {})
        print(screenshot)
        return base64.b64decode(screenshot['data'])


    @staticmethod
    def _send_devtools(driver, cmd, params):
        resource = f"/session/{driver.session_id}/moz/send_command"
        url = driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = driver.command_executor._request('POST', url, body)
        return response.get('value')

    def _generate_pdfs(self, print_options):
        pdf_files = []
        for url in self.urls:
            result = self._get_pdf_from_url(url, print_options)
            file = BytesIO()
            file.write(result)
            pdf_files.append(file)
        return pdf_files

    def generate_mobile_pdfs(self):
        return self._generate_pdfs(self.mobile_print_options)

    def generate_desktop_pdfs(self):
        return self._generate_pdfs(self.desktop_print_options)

    def main(self):
        webdriver_options = FirefoxOptions()
        webdriver_options.headless = True

        try:
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=webdriver_options
            )

            view_choice = input("Choose a view (1 for mobile, 2 for desktop): ")
            while view_choice not in ('1', '2'):
                print("Invalid choice. Please enter 1 for mobile or 2 for desktop.")
                view_choice = input("Choose a view (1 for mobile, 2 for desktop): ")

            while True:
                url = input("Enter URL (leave blank to finish): ")
                if not url:
                    break
                self.urls.append(url)

            if view_choice == '1':
                pdfs = self.generate_mobile_pdfs()
                output_filename = 'mobile.pdf'
            else:
                pdfs = self.generate_desktop_pdfs()
                output_filename = 'desktop.pdf'

        finally:
            self.driver.quit()

        return pdfs, output_filename

if __name__ == "__main__":
    pdf_generator = PdfGenerator()
    pdf_files, output_filename = pdf_generator.main()

    for index, pdf_file in enumerate(pdf_files, start=1):
        with open(output_filename, "wb") as outfile:
            outfile.write(pdf_file.getbuffer())

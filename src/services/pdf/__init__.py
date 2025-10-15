
import base64
import contextlib

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.utils.text_to_uri_data import text_to_uri_data


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--disable-popup-blocking')

params = {
  # ======= Page Setup =======
  'paperWidth'       : 8.27,   # A4 width (in inches)
  'paperHeight'      : 11.69,  # A4 height (in inches)
  'landscape'        : False,  # Portrait orientation
  'scale'            : 1.0,    # Default 100% zoom (avoid clipping)
  'preferCSSPageSize': False,  # Ignore @page size from CSS (use explicit A4)
  
  # ======= Print Appearance =======
  'printBackground'    : False, # Don’t include CSS backgrounds or images
  'displayHeaderFooter': False, # Cleaner output (no default header/footer)

  # ======= Margins =======
  'marginTop'    : 0,
  'marginBottom' : 0,
  'marginLeft'   : 0,
  'marginRight'  : 0,

  # ======= Output Behavior =======
  'transferMode': 'ReturnAsBase64', # Return Base64 data (required for Selenium use)
  'pageRanges'  : '',               # Print all pages
}

@contextlib.contextmanager
def _chrome_driver(options):
  try:
    service = Service()
    with webdriver.Chrome(service = service, options = options) as driver:
      yield driver
  
  finally:
    pass

def _b64_encode(file):
  return base64.b64encode(file).decode('utf-8')

def printHtmlToPDF(text = '', *, 
                   b64_encoded = False,
                  ):
  global chrome_options
  global params

  with _chrome_driver(chrome_options) as driver:
    driver.get(text_to_uri_data(text))
    pdfdata = driver.execute_cdp_cmd("Page.printToPDF", params)
    pdf     = base64.b64decode(pdfdata['data'])

  return pdf if not b64_encoded else _b64_encode(pdf)


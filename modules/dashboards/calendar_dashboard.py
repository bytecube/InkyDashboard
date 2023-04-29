import io
import os

import chromedriver_autoinstaller
from time import sleep
from PIL import Image
from pyvirtualdisplay import Display
from selenium import webdriver


def generate_calendar_dashboard(screen_size):
    if os.environ['CALENDAR_URL'] is None:
        print(f"CALENDAR_URL is not defined, can't retrieve calendar")
        return

    try:
        display = Display(visible=False, size=screen_size)
        display.start()
    except FileNotFoundError:
        print("PyVirtualDisplay not supported on this platform, trying it without")

    chromedriver_autoinstaller.install()

    # Set the screen size
    #
    width, height = screen_size

    # Set the options for the Chrome driver
    chrome_options = webdriver.ChromeOptions()
    options = [
        # Define window size here
        f"--window-size={width},{height}",
        "--ignore-certificate-errors"
        "--headless",
    ]

    for option in options:
        chrome_options.add_argument(option)

    # Start the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the Google calendar
    driver.get(os.environ['CALENDAR_URL'])
    driver.execute_script("document.body.style.fontSize = 'larger';")

    # Wait for the page to load
    driver.implicitly_wait(30)

    sleep(2)

    # Load the PNG image from driver.get_screenshot_as_png()
    png_img = driver.get_screenshot_as_png()

    # Convert the PNG image to a PIL Image object
    img = Image.open(io.BytesIO(png_img))

    # Remove the alpha channel from the PIL Image object
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    return img

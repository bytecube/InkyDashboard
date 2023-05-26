import os
import io

import chromedriver_autoinstaller
from time import sleep
from PIL import Image
from pyvirtualdisplay import Display
from selenium import webdriver

from modules.dashboard_generators.base_dashboard_generator import BaseDashboardGenerator
from modules.display_configuration import DisplayConfiguration


class CalendarDashboardGenerator(BaseDashboardGenerator):

    def build_dashboard(self, button_assignment: int, display_configuration: DisplayConfiguration) -> Image:
        if os.environ['GOOGLE_CALENDAR_URL'] is None:
            print(f"CALENDAR_URL is not defined, can't retrieve calendar")
            return

        try:
            display = Display(visible=False, size=(display_configuration.width, display_configuration.height))
            display.start()
        except FileNotFoundError:
            print("PyVirtualDisplay not supported on this platform, trying it without")

        chromedriver_autoinstaller.install()

        width, height = display_configuration.width, display_configuration.height

        chrome_options = webdriver.ChromeOptions()
        options = [
            f"--window-size={width},{height}",
            "--ignore-certificate-errors"
            "--headless",
        ]

        for option in options:
            chrome_options.add_argument(option)

        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the Google calendar
        driver.get(os.environ['GOOGLE_CALENDAR_URL'])
        driver.execute_script("document.body.style.fontSize = 'larger';")

        # Wait for the page to load
        driver.implicitly_wait(30)
        sleep(2)

        png_img = driver.get_screenshot_as_png()

        # Convert the PNG image to a PIL Image object
        img = Image.open(io.BytesIO(png_img))

        # Remove the alpha channel from the PIL Image object
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        return img


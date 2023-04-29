"""

This script will download the dashboard images generated on GitHub to be displayed
on the Inky Frame.

Buttons 1-4: 	Display dashboards of specific location
Button 5: 		Download updated dashboard images from Github

Project page: https://github.com/bytecube/CalPi2

"""

import os
import gc
import time
import utime

import sdcard
import jpegdec
import inky_frame
import inky_helper
from ntptime import settime
from machine import Pin, SPI
# from picographics import PicoGraphics, DISPLAY_INKY_FRAME as DISPLAY    # 5.7"
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4 as DISPLAY  # 4.0"
# from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY  # 7.3"

from image_downloader import ImageDownloader

DAILY_REFRESH_TIME_O_CLOCK = 5
image_downloader = ImageDownloader()

gc.collect()

# Sync the Inky (always on) RTC to the Pico W so that "time.localtime()" works.
inky_frame.pcf_to_pico_rtc()

# you can change your file names here
IMAGE_A = "sd/1.jpg"
IMAGE_B = "sd/2.jpg"
IMAGE_C = "sd/3.jpg"
IMAGE_D = "sd/4.jpg"
IMAGE_E = "sd/5.jpg"

# set up the display
graphics = PicoGraphics(DISPLAY)

# set up the SD card
sd_spi = SPI(0, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=Pin(16, Pin.OUT))
sd = sdcard.SDCard(sd_spi, Pin(22))
os.mount(sd, "/sd")

def display_image(filename):
    gc.collect()
    
    # Create a new JPEG decoder for our PicoGraphics
    j = jpegdec.JPEG(graphics)

    # Open the JPEG file
    j.open_file(filename)

    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)

    # Display the result
    graphics.update()


def progressbar_increment(i):
    if i == 1: inky_frame.button_a.led_on()
    if i == 2: inky_frame.button_b.led_on()
    if i == 3: inky_frame.button_c.led_on()
    if i == 4: inky_frame.button_d.led_on()
    if i == 5: inky_frame.button_e.led_on()
    

def fetch_images():
    gc.collect()
    
    
    for i in range(1, 6):
        progressbar_increment(i)
        try:
            image_downloader.download_image(f"{i}.jpg")
        except:
            pass
    
    inky_helper.clear_button_leds()


# While loop only required when testing plugged into the computer
# while True:
if inky_frame.woken_by_button():
    inky_helper.clear_button_leds()

    if inky_frame.button_a.read():
        inky_frame.button_a.led_on()
        display_image(IMAGE_A)

    elif inky_frame.button_b.read():
        inky_frame.button_b.led_on()
        display_image(IMAGE_B)

    elif inky_frame.button_c.read():
        inky_frame.button_c.led_on()
        display_image(IMAGE_C)

    elif inky_frame.button_d.read():
        inky_frame.button_d.led_on()
        display_image(IMAGE_D)

    elif inky_frame.button_e.read():
        fetch_images()
        inky_frame.button_e.led_on()


if inky_frame.woken_by_rtc():
    fetch_images()

def get_time_in_minutes_to_sleep():
    
    image_downloader.connect_to_wifi()

    #Get current date and time and set RTC clock
    settime()

    # Get the current time in seconds since the epoch
    now = utime.time()

    # Get the current time in your local timezone
    local_time = utime.localtime(now)

    # Calculate the time until tomorrow morning 5 o'clock in your local timezone
    tomorrow_morning = utime.mktime((local_time[0], local_time[1], local_time[2] + 1, DAILY_REFRESH_TIME_O_CLOCK, 0, 0, 0, 0))
    time_until_tomorrow_morning = tomorrow_morning - now

    # Convert the time to minutes
    time_until_tomorrow_morning_minutes = time_until_tomorrow_morning // 60
    
    # Convert the time to hours
    time_until_tomorrow_morning_hours = time_until_tomorrow_morning_minutes // 60
    
    print("Will sleep for ", time_until_tomorrow_morning_minutes, " minutes or ", time_until_tomorrow_morning_hours, " hours until 5 o'clock in the morning next day")
    
    return time_until_tomorrow_morning_minutes


# Go to sleep if on battery power
inky_frame.sleep_for(get_time_in_minutes_to_sleep())
inky_frame.turn_off()
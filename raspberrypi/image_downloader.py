import os
import gc

import sdcard
import uasyncio
import urequests
from machine import Pin, SPI

import inky_helper
import WIFI_CONFIG
from network_manager import NetworkManager


class ImageDownloader:

    def __init__(self):
        pass
        
    def __mount_sd_card(self):
        # set up the SD card
        sd_spi = SPI(0, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=Pin(16, Pin.OUT))
        sd = sdcard.SDCard(sd_spi, Pin(22))
        os.mount(sd, "/sd")

    def __status_handler(self, mode, status, ip):
        print(mode, status, ip)
        
    def connect_to_wifi(self,):
        network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=self.__status_handler)
        uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
        gc.collect()
    
    def download_image(self, image_name):
        self.connect_to_wifi()
        inky_helper.pulse_network_led()
#         self.__mount_sd_card()

        # define parameters for a request
        token = ''
        owner = 'bytecube'
        repo = 'InkyDashboard'
        
        socket = urequests.request("GET", 'https://api.github.com/repos/{owner}/{repo}/contents/dashboards/{path}'.format(
            owner=owner, repo=repo, path=image_name),
                                    headers={
                                        'accept': 'application/vnd.github.v3.raw',
                                        'authorization': 'token {}'.format(token),
                                        'User-Agent': 'CalPi2'
                                            })
        
        buf = bytearray(256)
        with open(f'sd/{image_name}', "wb") as f:
            while True:
                if socket.raw.readinto(buf) == 0:
                    break
                f.write(buf)
                
        socket.close()
        gc.collect()
        
        return True
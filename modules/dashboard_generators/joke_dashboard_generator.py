import os
import re
from typing import Any

import requests
from PIL import Image, ImageFont, ImageDraw


from modules.dashboard_generators.base_dashboard_generator import BaseDashboardGenerator
from config.config import JOKE_API_ENDPOINT


def get_joke(api_endpoint: str):
    response = requests.get(api_endpoint + os.environ['API_KEY_JOKES'])
    joke = response.json()["joke"]
    return joke


def clean_joke(joke: str) -> str:
    joke = joke.replace('\\\\', '\\')
    joke = re.sub(r'[^\x00-\x7F]+', '', joke)
    return joke


def split_lines(text: str) -> tuple[list[str], list[str | Any]]:
    # Split the text into lines to fit on the image
    lines = text.split('\\n')
    new_lines = []
    for line in lines:
        words = line.split()
        new_line = ''
        for word in words:
            if len(new_line + word) > 55:
                new_lines.append(new_line)
                new_line = word + ' '
            else:
                new_line += word + ' '
        if new_line:
            new_lines.append(new_line)
    return lines, new_lines


class JokeDashboardGenerator(BaseDashboardGenerator):
    def build_dashboard(self, button_assignment, display_configuration) -> Image:
        if os.environ['API_KEY_JOKES'] is None:
            print(f"jokes_api_key is not defined, can't retrieve jokes")
            return

        if JOKE_API_ENDPOINT is None:
            print(f"api_endpoint is not defined, can't retrieve jokes")
            return

        print(f"Generating jokes dashboard")

        print(f"- Requesting joke ")
        joke = get_joke(JOKE_API_ENDPOINT)

        img = Image.new('RGB', (display_configuration.width, display_configuration.height), color='black')

        font = ImageFont.truetype('fonts/Arial.ttf', size=20)
        line_spacing = 0

        # Remove non-ASCII characters
        joke = clean_joke(joke)

        lines, new_lines = split_lines(joke)

        # Adjust font size and line spacing if a text is too long
        while True:
            line_heights = [font.getsize(line)[1] for line in new_lines]
            if sum(line_heights) <= img.height:
                break
            font.size -= 1
            line_spacing = font.getsize('A')[1] // 2
            new_lines = []
            for line in lines:
                words = line.split()
                new_line = ''
                for word in words:
                    if len(new_line + word) > 55:
                        new_lines.append(new_line)
                        new_line = word + ' '
                    else:
                        new_line += word + ' '
                if new_line:
                    new_lines.append(new_line)

        # Calculate the total height of the text
        total_height = sum(line_heights) + line_spacing * (len(new_lines) - 1)

        # Calculate the starting y-coordinate to center the text vertically
        y = (img.height - total_height) // 2

        # Draw the text on the image
        draw = ImageDraw.Draw(img)
        for line in new_lines:
            line_width, line_height = draw.textsize(line, font=font)
            x = (img.width - line_width) // 2
            draw.text((x, y), line, font=font, fill='white')
            y += line_height + line_spacing

        return img

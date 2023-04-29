from PIL import Image

from config.config import TOTAL_BUTTONS


def save_dashboard(button: int, dashboard_img: Image):
    if button <= 0 & button > TOTAL_BUTTONS:
        print(f"Invalid button assignment, could not save dashboard for button {button}")
        return

    path = f'dashboards/{button}.jpg'
    print(f"- Saving dashboard for button {button} in: {path}")
    dashboard_img.save(path)

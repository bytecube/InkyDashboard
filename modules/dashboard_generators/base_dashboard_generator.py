import logging
from abc import ABC
from typing import final

from PIL import Image

from modules.display_configuration import DisplayConfiguration


class BaseDashboardGenerator(ABC):
    """
        Abstract base class for a Dashboard Generator.

        This class provides the base functionality for a dashboard generator. It is designed to be subclassed by
        specific implementations that override the `build_dashboard` method.

        Attributes
        ----------
        __button_assignment : int
            Stores the assigned button id which is used for generating and saving the dashboard.
        __display_configuration : DisplayConfiguration
            Stores the display configuration which is used for generating the dashboard.
        __prepared_dashboard : PIL.Image
            Stores the generated dashboard image.

        Methods
        -------
        generate_dashboard(button_assignment: int, display_configuration: DisplayConfiguration) -> PIL.Image:
            Accepts the button assignment and display configuration, and calls the '__prepare_dashboard'
            and '__save_image' methods to generate and save the dashboard.

        Build_dashboard(button_assignment: int, display_configuration: DisplayConfiguration) -> PIL.Image:
            Abstract method to be overridden in child classes for generating the dashboard image. It raises
            an exception if not implemented.

        __prepare_dashboard():
            A private method that calls 'build_dashboard' method to generate dashboard, handles any exceptions
            that may arise and logs the process.

        __save_image():
            A private method that saves the generated dashboard image to a specific location and handles
            any exceptions that may arise during the process.
        """
    def __init__(self):
        self.__button_assignment = None
        self.__display_configuration = None
        self.__prepared_dashboard = None

    @final
    def generate_dashboard(self, button_assignment: int, display_configuration: DisplayConfiguration) -> Image:
        if button_assignment <= 0:
            print(f"Invalid button assignment, could not save dashboard for button {button_assignment}")
            return
        self.__button_assignment = button_assignment
        self.__display_configuration = display_configuration

        self.__prepare_dashboard()

        if self.__prepared_dashboard is not None:
            self.__save_image()
        else:
            logging.error(f"Could not generate dashboard #{self.__button_assignment}")
            return

    def __prepare_dashboard(self):
        try:
            self.__prepared_dashboard = self.build_dashboard(self.__button_assignment, self.__display_configuration)
            logging.info(f"Generated dashboard #{self.__button_assignment}")
        except Exception as e:
            logging.error(f"Could not generate dashboard #{self.__button_assignment}")
            logging.error(e)
            return

    def __save_image(self):
        path = f'dashboards/{self.__button_assignment}.jpg'

        try:
            self.__prepared_dashboard.save(path)
            print(f"- Saved dashboard #{self.__button_assignment} as '{path}'\n")
        except Exception as e:
            logging.error(f"Could not save dashboard #{self.__button_assignment}'")
            logging.error(e)
            return

    def build_dashboard(self, button_assignment: int, display_configuration: DisplayConfiguration) -> Image:
        raise Exception(f"'build_dashboard' not implemented for {self.__module__}")

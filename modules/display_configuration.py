class DisplayConfiguration:
    """
    Class to define and handle the configuration parameters for a display.

    This class is used to set the eInk display parameters such as height, width, and colors which are
    used in the generation of dashboards. The 'colors' parameter has a default value of 7.

    Attributes
    ----------
    height : int
        The height of the display in pixels.
    width : int
        The width of the display in pixels.
    colors : int, optional
        The number of colors the display supports. Default value is 7.
    """
    def __init__(self, height: int, width: int, colors: int = 7):
        self.height = height
        self.width = width
        self.colors = colors

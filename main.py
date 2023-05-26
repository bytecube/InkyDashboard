"""
This script imports specific dashboard generator classes and a display configuration class.

It then defines a mapping between button assignments and corresponding dashboard generators.
Following that, it sets up a basic display configuration that is used to generate the dashboards.

Finally, it loops through each button assignment, creates an instance of the corresponding dashboard
generator and triggers the dashboard generation process.

Modules
-------
modules.dashboard_generators.joke_dashboard_generator : JokeDashboardGenerator
    Dashboard generator class for generating a joke dashboard.
modules.dashboard_generators.calendar_dashboard_generator : CalendarDashboardGenerator
    Dashboard generator class for generating a calendar dashboard.
modules.dashboard_generators.weather_dashboard_generator : WeatherDashboardGenerator
    Dashboard generator class for generating a weather dashboard.
modules.display_configuration : DisplayConfiguration
    Class to configure the display parameters used to prepare the images.

Variables
---------
dashboard_configuration : dict
    A dictionary mapping button assignments to their corresponding dashboard generator classes.
display_configuration : DisplayConfiguration
    An instance of DisplayConfiguration class, configuring the display parameters for generating the dashboards.
button_assignment : int
    In the loop, it holds the current button assignment number used to fetch the corresponding dashboard generator class.
dashboard_generator : BaseDashboardGenerator subclass
    An instance of the dashboard generator class corresponding to the current button assignment.
"""

from modules.dashboard_generators.joke_dashboard_generator import JokeDashboardGenerator
from modules.dashboard_generators.calendar_dashboard_generator import CalendarDashboardGenerator
from modules.dashboard_generators.weather_dashboard_generator import WeatherDashboardGenerator
from modules.display_configuration import DisplayConfiguration


# <BUTTON_NO>: <DASHBOARD_MODULE>
dashboard_configuration = {
    1: WeatherDashboardGenerator,
    2: CalendarDashboardGenerator,
    3: JokeDashboardGenerator,
}

display_configuration = DisplayConfiguration(width=640, height=400, colors=7)

for button_assignment in dashboard_configuration:
    dashboard_generator = dashboard_configuration.get(button_assignment)()
    dashboard_generator.generate_dashboard(button_assignment, display_configuration)

from .MainMenu import displayPage as mainMenuDisplay
from .GameMenu import displayPage as gameMenuDisplay
from .Settings import displayPage as settingsDisplay, options_buttons
from .Data import (
    getMainMenuButtons,
    getGamesMenuButtons,
    getDefaultSettings,
    getSettingsOptions,
    getSettingsButtons,
    getConfirmationButtons,
)
from .Dropdown import displayPage as dropdownDisplay, xy_range, setOptionsButtons
from .ColourPicker import displayPage as colourPickerDisplay
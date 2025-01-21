import pygame
import sys

class Settings:
# Default incase it wants to be reset to default
    default_settings = {
            "width": 1920,
            "height": 1080,
            "windowtype": "windowedfullscreen",
            "background": (52, 53, 65),
            "primary": (168, 213, 186),
            "secondary": (255, 154, 162),
            "tertiary": (255, 243, 176)
    }
    window_flags = {
        "fullscreen": pygame.FULLSCREEN,
        "windowedfullscreen": pygame.NOFRAME,
        "windowed": 0
    }
    def __init__(self):
        self.settings = self.setSettings()
        self.applySettings()
    def getSettings(self):
        return self.settings
    def resetSettings(self):
        self.settings = self.default_settings.copy()
        return self.settings
    def setSettings(self):
        self.settings = self.default_settings.copy() # To ensure values are all filled and anything not found is replaced with default values
        try:
            with open("./settings.txt", "r") as file:
                for line in file:
                    # Ignore empty lines and comments
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    
                    # Split at the '=' sign to separate the key and value
                    key, value = line.split(" = ", 1)
                    key = key  # Normalize key to lowercase
                    value = value.strip()

                    # Handle different types of values and only update if the key exists in default settings
                    if key in self.settings:  # Only update if the key exists in default settings
                        if "," in value:  # Check for comma-separated values (like RGB)
                            self.settings[key] = tuple(map(int, value.split(",")))  # Convert to tuple
                        elif value.isdigit():  # Check for numeric values
                            self.settings[key] = int(value)  # Convert to integer
                        else:  # Otherwise, treat as a string (e.g., windowtype)
                            self.settings[key] = value
        except FileNotFoundError:
            print("Error: settings.txt not found. Using default values.")
        except ValueError as e:
            print(f"Error: Incorrect format in settings.txt ({e}). Using default values.")

        return self.settings
    def applySettings(self):
        global screen
        flags = self.window_flags.get(self.settings["windowtype"], pygame.NOFRAME) # Sets the window type based on the settings file or defaults to windowed fullscreen

        screen = pygame.display.set_mode((self.settings['width'], self.settings['height']), flags)

        print(f"Screen set to: {self.settings['width']}x{self.settings['height']} in {self.settings['windowtype']} mode.")

pygame.init()

settingsClass = Settings()
settings = settingsClass.getSettings()

pygame.display.set_caption("Sharp Minds")

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(settings['background'])
    pygame.display.flip()  # Update the display
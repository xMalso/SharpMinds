import pygame
import sys
from pages import *


class Settings:
    # Default incase it wants to be reset to default
    default_settings = getDefaultSettings()

    def __init__(self):
        global screen, font, pygame
        self.settings = self.setSettings()
        self.applySettings()
        text_surface = font.render(
            "Loading Game...",
            self.settings["Antialiasing Text"],
            self.settings["Background Font"],
        )
        screen.blit(
            text_surface,
            (
                self.settings["Width"] // 2 - text_surface.get_width() // 2,
                self.settings["Height"] // 2 - text_surface.get_height() // 2,
            ),
        )
        pygame.display.flip()

    def getSettings(self):
        return self.settings

    def resetSettings(self):
        self.settings = self.default_settings.copy()
        return self.settings

    def setSettings(self):
        self.settings = (
            self.default_settings.copy()
        )  # To ensure values are all filled and anything not found is replaced with default values
        try:
            with open("./settings.txt", "r") as file:
                for line in file:
                    # Ignore empty lines and comments
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    key, value = line.split(": ", 1)
                    value = value.strip(",")
                    key = key.strip("'")

                    if (
                        key in self.settings
                    ):  # Only update if it is a setting that has been defined
                        if "," in value:
                            self.settings[key] = tuple(
                                map(int, value.strip("()").split(", "))
                            )  # Convert to tuple (mainly for RGB values)
                        elif value.isdigit():  # Check for numbers
                            self.settings[key] = int(value)
                        elif (
                            value.lower() == "True" or value.lower() == "False"
                        ):  # Check for boolean
                            self.settings[key] = value.lower() == "True"
                        else:  # Otherwise must be a string
                            self.settings[key] = value.strip('"')
                    else:
                        print(
                            f"Warning: Unknown setting '{key}' found in settings.txt. Ignoring."
                        )
        except FileNotFoundError:
            print("Error: settings.txt not found. Using default values.")
        except ValueError as e:
            print(
                f"Error: Incorrect format in settings.txt ({e}). Using default values."
            )

        return self.settings

    def applySettings(self):
        global screen
        global font
        window_flags = {
            "Fullscreen": pygame.FULLSCREEN,
            "Borderless": pygame.NOFRAME,
            "Windowed": 0,
        }
        flags = window_flags.get(
            self.settings["Window Type"], pygame.NOFRAME
        )  # Sets the window type based on the settings file or defaults to borderless
        font = pygame.font.SysFont(self.settings["Font"], self.settings["Font Size"])
        screen = pygame.display.set_mode(
            (self.settings["Width"], self.settings["Height"]), flags
        )
        pygame.display.flip()

        print(
            f"Screen set to: {self.settings['Width']}x{self.settings['Height']} in {self.settings['Window Type']} mode."
        )


def loadUpValues():
    global content_height, max_scroll, scroll, main_menu_buttons, games_buttons, settings_buttons, page
    content_height = (  # 1/30th of the screen per setting and 1/8th of the screen for back and save button and 200 pixel padding on bottom
        len(settings) * settings["Height"] // 32 + settings["Height"] // 8
    )
    # Calculate max scrolling based on size of settings
    max_scroll = max(0, content_height - settings["Height"])
    scroll = 0
    main_menu_buttons = getMainMenuButtons(pygame, settings)
    games_buttons = getGamesMenuButtons(pygame, settings)
    settings_buttons = getSettingsButtons(pygame, settings)
    page = "Main Menu"


def initialLoadUp():
    global pygame
    pygame.init()
    pygame.display.set_caption("Sharp Minds")

    screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
    screen.fill((31, 31, 31))
    default_font = pygame.font.SysFont("Arial", 30)
    default_text_surface = default_font.render(
        "Loading Settings...", True, (217, 217, 217)
    )
    screen.blit(
        default_text_surface,
        (
            1920 // 2 - default_text_surface.get_width() // 2,
            1080 // 2 - default_text_surface.get_height() // 2,
        ),
    )
    pygame.display.flip()


initialLoadUp()
settingsClass = Settings()
settings = settingsClass.getSettings()
loadUpValues()

while True:
    screen.fill(settings["Background"])
    if page == "Main Menu":
        mainMenuDisplay(settings, screen, font, pygame, main_menu_buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in main_menu_buttons:  # Check for each button
                    if button["Pygame Button"].collidepoint(
                        event.pos
                    ):  # Check if location of mouse is within the boundaries of the button when mouse is pressed
                        page = button["Page"]  # Set page if button is pressed
                        print(f"Page set to: {page}")
    elif page == "Game Menu":
        gameMenuDisplay(settings, screen, font, pygame, games_buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for game in games_buttons:  # Check for each button
                    if game["Pygame Button"].collidepoint(
                        event.pos
                    ):  # Check if location of mouse is within the boundaries of the button when mouse is pressed
                        page = game["Page"]  # Set page if button is pressed
                        print(f"Page set to: {page}")
    elif page == "Settings":
        settingsDisplay(
            settings, screen, font, pygame, scroll, content_height, settings_buttons
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                scroll = max(
                    0,
                    min(
                        content_height - settings["Height"],
                        scroll - event.y * settings["Height"] // 32,
                    ),
                )
            # if save.collidepoint(event.pos):
            #     with open("settings.txt", "w") as file:
            #         for key, value in settings.items():
            #             file.write(f"{key}: {value}\n")
            #     print("Settings saved.")
    elif page == "Quit":
        pygame.quit()
        sys.exit()
    pygame.display.flip()

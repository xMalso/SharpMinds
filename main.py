import pygame, sys, os
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
            self.settings["Background Font Colour"],
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
                    key = key.strip('"')

                    if (
                        key in self.settings
                    ):  # Only update if it is a setting that has been defined
                        if "," in value:
                            try:
                                self.settings[key] = tuple(
                                    map(int, value.strip("()").split(", "))
                                )  # Convert to int tuple (for RGB values)
                            except:
                                self.settings[key] = tuple(
                                    map(float, value.strip("()").split(", "))
                                )  # Convert to float tuple (for adaptive difficulty)
                        elif value.isdigit():  # Check for numbers
                            self.settings[key] = int(value)
                        elif (
                            value.lower() == "true" or value.lower() == "false"
                        ):  # Check for boolean
                            self.settings[key] = value.lower() == "true"
                        else:  # Otherwise must be a string
                            self.settings[key] = value.strip('"')
                    else:
                        print(
                            f"Warning: Unknown setting '{key}' found in settings.txt. Ignoring."
                        )
                if os.path.isfile(
                    os.path.join(r"assets/fonts/fonts", self.settings["Font"])
                ):
                    self.settings["Font Type"] = "Custom"
                else:
                    self.settings["Font Type"] = "System"
        except FileNotFoundError:
            print("Error: settings.txt not found. Using default values.")
        except ValueError as e:
            print(
                f"Error: Incorrect format in settings.txt ({e}). Using default values."
            )
        global choice
        self.settings["Font Size"] = (
            self.settings["Width"] // self.settings["Font Size"]
        )
        choice = self.settings.copy()
        del choice["Font Type"]
        self.saveSettings()
        del choice["Adaptive Difficulty"]
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
        size = self.settings["Font Size"]
        if self.settings["Font Type"] == "System":
            font = pygame.font.SysFont(
                self.settings["Font"],
                size,
            )
        else:
            font = pygame.font.Font(
                os.path.join(r"assets/fonts/fonts", self.settings["Font"]),
                size,
            )
        screen = pygame.display.set_mode(
            (self.settings["Width"], self.settings["Height"]), flags
        )
        pygame.display.flip()

    def saveSettings(self):
        choice["Adaptive Difficulty"] = choice["Adaptive Difficulty"]
        choice["Font Size"] = choice["Width"] // choice["Font Size"]
        with open("settings.txt", "w") as file:
            for key, value in choice.items():
                file.write(f'"{key}": {value},\n')
        self.settings = choice.copy()
        choice["Font Size"] = choice["Width"] // choice["Font Size"]
        if os.path.isfile(os.path.join(r"assets/fonts/fonts", self.settings["Font"])):
            self.settings["Font Type"] = "Custom"
        else:
            self.settings["Font Type"] = "System"
        self.settings["Font Size"] = (
            self.settings["Width"] // self.settings["Font Size"]
        )


def loadUp():
    global pygame, settingsClass
    pygame.init()
    pygame.display.set_caption("Sharp Minds")

    screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
    screen.fill((31, 31, 31))
    default_font = pygame.font.Font(
        "assets\\fonts\\fonts\\OpenDyslexic-Regular.otf", 30
    )
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
    settingsClass = Settings()
    loadUpValues()


def loadUpValues():
    global main_menu_buttons, games_buttons, settings_buttons, meta, options, options_buttons
    global choice, settings, text_surface, i, frame, confirmation_buttons
    settings = settingsClass.getSettings()
    settingsClass.applySettings()
    frame = pygame.time.get_ticks()
    i = 1
    text_surface = None
    options_buttons = getOptionsButtons()
    main_menu_buttons = getMainMenuButtons(pygame, settings, font)
    games_buttons = getGamesMenuButtons(pygame, settings)
    settings_buttons = getSettingsButtons(pygame, settings, font)
    confirmation_buttons = getConfirmationButtons(pygame, settings, font)
    try:
        meta = meta
    except:
        meta = "Main Menu"
    options = getSettingsOptions(settings, font)


def getFps():
    global frame, i, screen, text_surface, settings, font
    if (pygame.time.get_ticks() - frame) > 100:
        fps = 1 / (pygame.time.get_ticks() - frame) * i * 1000
        if settings["Show FPS"] == True:
            text_surface = font.render(
                f"FPS: {fps:.2f}",
                settings["Antialiasing Text"],
                settings["Background Font Colour"],
            )
            screen.blit(text_surface, (0, 0))
        frame = pygame.time.get_ticks()
        i = 1
    else:
        i += 1
        if text_surface and settings["Show FPS"]:
            screen.blit(text_surface, (0, 0))


def checkExit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


loadUp()


while True:  # Main loop
    if meta == "Main Menu":
        meta, choice = mainMenuDisplay(
            pygame, sys, os, settings, screen, font, main_menu_buttons, getFps
        )
    elif meta == "Game Menu":
        meta = gameMenuDisplay(
            pygame, sys, os, settings, screen, font, games_buttons, getFps
        )
    elif meta == "Settings":
        choice, val = settingsDisplay(
            pygame,
            sys,
            settings,
            screen,
            font,
            settings_buttons,
            options,
            choice,
            confirmation_buttons,
            getFps,
        )
        if val == "Main Menu":
            meta = "Main Menu"
            scroll = 0
        elif val == "Save and Leave":
            choice["Adaptive Difficulty"] = settings["Adaptive Difficulty"]
            settingsClass.saveSettings()
            del choice["Adaptive Difficulty"]
            meta = "Main Menu"
            print("Settings saved.")
            loadUpValues()
        elif val == "Save":
            choice["Adaptive Difficulty"] = settings["Adaptive Difficulty"]
            settingsClass.saveSettings()
            del choice["Adaptive Difficulty"]
            print("Settings saved.")
            loadUpValues()
        elif val == "Default":
            difficulty = settings["Adaptive Difficulty"]
            settings = settingsClass.resetSettings()
            choice = settings.copy()
            choice["Adaptive Difficulty"] = difficulty
            del choice["Font Type"]
            settingsClass.saveSettings()
            del choice["Adaptive Difficulty"]
            print("Settings reset.")
            loadUpValues()
    elif meta == "Quit":
        pygame.quit()
        sys.exit()
    elif meta == "Expose the Impostor":
        score, adjustment, meta = Game1(pygame, settings, screen, font)
        if score != None:
            score = score / (settings["Adaptive Difficulty"][0] ** 0.65)
            difficulty1, difficulty2, difficulty3 = settings["Adaptive Difficulty"]
            settings["Adaptive Difficulty"] = (
                max(difficulty1 + adjustment, 0.2),
                difficulty2,
                difficulty3,
            )
            choice = settings.copy()
            del choice["Font Type"]
            settingsClass.saveSettings()
            del choice["Adaptive Difficulty"]
            print("Adaptive Difficulty saved.")
    elif meta == "Pattern Rush":
        Game2()
    elif meta == "Memory Experiment":
        Game3()
    elif meta == "Game 1 Over" or meta == "Game 2 Over" or meta == "Game 3 Over":
        gameOverDisplay(pygame, settings, font, meta, score)
        meta = "Main Menu"
    else:
        print(f"Page '{meta}' is currently in development, sending back to main menu.")
        meta = "Main Menu"
    # if settings["FPS Limit"] > 0:
    # limiter = (1/settings["FPS Limit"]) - (pygame.time.get_ticks() - frame) / i
    # print(f"FPS: {fps}, Limiter: {limiter}, pygame.time.get_ticks(): {pygame.time.get_ticks()}, frame: {frame}, i: {i}")
    # if limiter > 0:
    # pygame.time.Clock().tick(limiter)
    # print(pygame.time.get_ticks())
    pygame.display.flip()

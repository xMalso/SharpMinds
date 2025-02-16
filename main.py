import pygame
import sys
import os
from pages import *

# import firebase_admin
# from dotenv import load_dotenv
# from firebase_admin import credentials, firestore
# import steam
# steamworks = steam.SteamWorks()

# if steamworks.is_running():
#     user = steamworks.user
#     steam_id = user.steam_id
#     print(f"User Steam ID: {steam_id}")
# else:
#     print("Steam is not running.")

# load_dotenv()
# private_key_path = os.getenv("FIREBASE_PRIVATE_KEY_PATH")

# print(private_key_path)
# cred = credentials.Certificate(private_key_path)
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# leaderboard_ref = db.collection('leaderboard')


class Settings:
    # Default incase it wants to be reset to default

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
        self.settings = default_settings.copy()
        return self.settings

    def setSettings(self):
        # To ensure values are all filled and anything not found is replaced with default values
        self.settings = default_settings.copy()
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
                                    # Convert to float tuple (for adaptive difficulty)
                                )
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
        choice = self.settings.copy()
        del choice["Font Type"]
        self.saveSettings()
        del choice["Adaptive Difficulty"]
        return self.settings

    def applySettings(self):
        global screen
        global font, title_font, small_font
        window_flags = {
            "Fullscreen": pygame.FULLSCREEN,
            "Borderless": pygame.NOFRAME,
            "Windowed": 0,
        }
        # Sets the window type based on the settings file or defaults to borderless
        flags = window_flags.get(self.settings["Window Type"], pygame.NOFRAME)
        size = self.settings["Font Size"]
        if self.settings["Font Type"] == "System":
            font = pygame.font.SysFont(
                self.settings["Font"],
                size,
            )
            title_font = pygame.font.SysFont(
                self.settings["Font"],
                size * 3,
                bold=True,
            )
            small_font = pygame.font.SysFont(
                self.settings["Font"],
                size // 2,
            )
        else:
            font = pygame.font.Font(
                os.path.join(r"assets/fonts/fonts", self.settings["Font"]),
                size,
            )
            title_font = pygame.font.Font(
                os.path.join(r"assets/fonts/fonts", self.settings["Bold Font"]),
                size * 3,
            )
            small_font = pygame.font.Font(
                os.path.join(r"assets/fonts/fonts", self.settings["Font"]),
                size // 2,
            )
        screen = pygame.display.set_mode(
            (self.settings["Width"], self.settings["Height"]), flags
        )
        pygame.display.flip()

    def saveSettings(self):
        with open("settings.txt", "w") as file:
            for key, value in choice.items():
                file.write(f'"{key}": {value},\n')
        self.settings = choice.copy()
        if os.path.isfile(os.path.join(r"assets/fonts/fonts", self.settings["Font"])):
            self.settings["Font Type"] = "Custom"
        else:
            self.settings["Font Type"] = "System"


def loadUp():
    global pygame
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
    global settingsClass, default_settings
    default_settings = {
        "Width": 1920,
        "Height": 1080,
        "Window Type": "Borderless",
        "Show FPS": True,
        "FPS Limit": 0,
        "Background Colour": (31, 31, 31),
        "Background Font Colour": (217, 217, 217),
        "Grid Background Colour": (63, 63, 63),
        "Grid Line Colour": (217, 217, 217),
        "Dropdown Background Colour": (63, 63, 63),
        "Dropdown Font Colour": (217, 217, 217),
        "Input Background Colour": (85, 85, 85),
        "Selected Input Colour": (60, 60, 60),
        "Input Font Colour": (217, 217, 217),
        "Button Primary Colour": (99, 139, 102),
        "Font Primary Colour": (217, 217, 217),
        "Button Secondary Colour": (90, 115, 225),
        "Font Secondary Colour": (217, 217, 217),
        "Button Tertiary Colour": (210, 100, 50),
        "Font Tertiary Colour": (217, 217, 217),
        "Button Quaternary Colour": (90, 90, 90),
        "Font Quaternary Colour": (217, 217, 217),
        "Button Quinary Colour": (255, 102, 68),
        "Font Quinary Colour": (217, 217, 217),
        "Font": "OpenDyslexic-Regular.otf",
        "Bold Font": "OpenDyslexic-Bold.otf",
        "Italic Font": "OpenDyslexic-Italic.otf",
        "BoldItalic Font": "OpenDyslexic-Bold-Italic.otf",
        "Font Type": "Custom",
        "Font Size": 30,
        "Antialiasing Text": True,
        "Game Primary Colour": (0, 255, 127),
        "Game Secondary Colour": (255, 191, 191),
        "Game Tertiary Colour": (0, 0, 255),
        "Adaptive Difficulty": (2, 2, 2),
        # "Scroll Speed": 100,
    }
    settingsClass = Settings()
    loadUpValues()


def loadUpValues():
    global meta, choice, settings, text_surface, i, frame, confirmation_buttons
    settings = settingsClass.getSettings()
    settingsClass.applySettings()
    frame = pygame.time.get_ticks()
    i = 1
    text_surface = None
    settingsInit(settings, font, small_font)
    mainMenuInit(settings, font, title_font)
    gameMenuInit(settings, small_font)
    gameOverInit(settings, font, title_font)
    game2Init(settings, small_font, font)


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


def exit():
    pygame.quit()
    sys.exit()


def executeSettingsResults(val):
    global choice, settings
    if val == "Main Menu":
        return "Main Menu"
    elif val == "Save and Leave":
        choice["Adaptive Difficulty"] = settings["Adaptive Difficulty"]
        settingsClass.saveSettings()
        del choice["Adaptive Difficulty"]
        print("Settings saved.")
        loadUpValues()
        return "Main Menu"
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
    return "Settings"


def adjustDifficulty(adjustment):
    global settings, meta, choice
    difficulty1, difficulty2, difficulty3 = settings["Adaptive Difficulty"]
    if game == "Expose the Criminal":
        settings["Adaptive Difficulty"] = (
            max(difficulty1 + adjustment, 0.2),
            difficulty2,
            difficulty3,
        )
        
    elif game == "Memory Experiment":
        settings["Adaptive Difficulty"] = (
            difficulty1,
            max(difficulty2 + adjustment, 0.2),
            difficulty3,
        )
    elif game == "Pattern Rush":
        settings["Adaptive Difficulty"] = (
            difficulty1,
            difficulty2,
            max(difficulty3 + adjustment, 0.2),
        )
    else:
        print("Error: Game not found, difficulty not adjusted and sending to main menu")
        meta = "Main Menu"
    del adjustment
    del difficulty1, difficulty2, difficulty3
    choice = settings.copy()
    del choice["Font Type"]
    settingsClass.saveSettings()
    del choice["Adaptive Difficulty"]
    print("Adaptive Difficulty saved.")


loadUp()
meta = "Main Menu"
# meta = "Game Over"
# game = "Expose the Criminal"
# score = 530.7385

while True:  # Main loop
    if meta == "Main Menu":
        meta, choice = mainMenuDisplay(settings, screen, font, getFps, exit)
    elif meta == "Game Menu":
        meta = gameMenuDisplay(
            settings, screen, font, title_font, small_font, getFps, exit
        )
    elif meta == "Settings":
        scroll = 0
        choice, val = settingsDisplay(
            settings, screen, font, title_font, small_font, choice, getFps, exit
        )
        meta = executeSettingsResults(val)
    elif meta == "Quit":
        pygame.quit()
        sys.exit()
    elif meta == "Expose the Criminal":
        score, adjustment, meta = Game1(settings, screen, font, getFps, exit)
        if score != None:
            game = "Expose the Criminal"
            adjustDifficulty(adjustment)
    elif meta == "Memory Experiment":
        score, adjustment, meta = Game2(settings, screen, font, getFps, exit)
        if score != None:
            game = "Memory Experiment"
            adjustDifficulty(adjustment)
    elif meta == "Pattern Rush":
        print(f"Page '{meta}' is currently in development, sending back to main menu.")
        score, adjustment, meta = Game3(settings, screen, font, getFps, exit)
        if score != None:
            game = "Pattern Rush"
            adjustDifficulty(adjustment)
    elif meta == "Game Over":
        meta = gameOverDisplay(screen, settings, font, game, score, getFps, exit)
    elif meta == "Leaderboards":
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

import pygame, sys, os, random, hashlib, requests, logging, traceback
from datetime import datetime
from pages import *
import dotenv

dotenv.load_dotenv()

lb = os.getenv("LB_URL")

global game
game_names = ["Expose the Criminal", "Memory Experiment", "Pattern Rush"]

logging.basicConfig(
    level=logging.WARNING,
    filename="latestlog.txt",
    filemode="w",
    format="%(filename)s:%(lineno)d | %(asctime)s - %(message)s",
)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)


# import steam
# steamworks = steam.SteamWorks()

# if steamworks.is_running():
#     user = steamworks.user
#     steam_id = user.steam_id
#     logging.debug(f"User Steam ID: {steam_id}")
# else:
#     logging.error("Error: Steam is not running.")


class Settings:

    def __init__(self):
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
                        elif value.isdigit():
                            self.settings[key] = int(value)
                        elif (
                            value.lower() == "true" or value.lower() == "false"
                        ):  # Check for boolean
                            self.settings[key] = value.lower() == "true"
                        else:  # Otherwise assume to be a string
                            self.settings[key] = value.strip('"')
                    else:
                        logging.warning(
                            f"Warning: Unknown setting '{key}' found in settings.txt. Ignoring."
                        )
            if os.path.isfile(
                os.path.join(r"assets/fonts/fonts", self.settings["Font"])
            ):
                self.settings["Font Type"] = "Custom"
            else:
                self.settings["Font Type"] = "System"
        except FileNotFoundError:
            logging.error("Error: settings.txt not found. Using default values.")
        except ValueError as e:
            logging.warning(
                f"Error: Incorrect format in settings.txt ({e}). Using default values."
            )
            logging.critical(
                f"Error: Incorrect format in settings.txt ({e}). Using default values."
            )
        global choice
        choice = self.settings.copy()
        del choice["Font Type"]
        self.saveSettings()
        del choice["Adaptive Difficulty"]
        return self.settings

    def applySettings(self):
        global font, title_font, small_font, bold_font, small_title_font, screen
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
            small_title_font = pygame.font.SysFont(
                self.settings["Font"],
                size * 2,
                bold=True,
            )
            bold_font = pygame.font.SysFont(
                self.settings["Bold Font"],
                size,
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
            small_title_font = pygame.font.Font(
                os.path.join(r"assets/fonts/fonts", self.settings["Bold Font"]),
                size * 2,
            )
            bold_font = pygame.font.Font(
                os.path.join(r"assets/fonts/fonts", self.settings["Bold Font"]),
                size,
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
    pygame.init()
    info = pygame.display.Info()
    pygame.display.set_caption("Sharp Minds")
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    global settingsClass, default_settings, meta, game
    default_settings = {
        "Width": info.current_w,
        "Height": info.current_h,
        "Window Type": "Borderless",
        "Show FPS": True,
        # "FPS Limit": 0,
        "Background Colour": (31, 31, 31),
        "Background Font Colour": (217, 217, 217),
        "Grid Background Colour": (63, 63, 63),
        "Grid Line Colour": (217, 217, 217),
        "Grid Selected Colour": (63, 94, 63),
        "Grid Selected Line Colour": (0, 0, 0),
        "Dropdown Background Colour": (63, 63, 63),
        "Dropdown Font Colour": (217, 217, 217),
        "Input Background Colour": (85, 85, 85),
        "Input Font Colour": (217, 217, 217),
        "Button Primary Colour": (99, 139, 102),
        "Font Primary Colour": (217, 217, 217),
        "Button Secondary Colour": (90, 115, 225),
        "Font Secondary Colour": (217, 217, 217),
        "Button Tertiary Colour": (210, 100, 50),
        "Font Tertiary Colour": (217, 217, 217),
        "Button Quaternary Colour": (90, 90, 90),
        "Font Quaternary Colour": (217, 217, 217),
        "Button Quinary Colour": (255, 85, 68),
        "Font Quinary Colour": (217, 217, 217),
        "Bold Contrasting Font Colour": (255, 215, 0),
        "Font": "OpenDyslexic-Regular.otf",
        "Bold Font": "OpenDyslexic-Bold.otf",
        "Italic Font": "OpenDyslexic-Italic.otf",
        "BoldItalic Font": "OpenDyslexic-Bold-Italic.otf",
        "Font Type": "Custom",
        "Font Size": 30,
        "Antialiasing Text": True,
        "Game Primary Colour": (0, 255, 127),
        "Game Primary Font Colour": (63, 63, 63),
        "Game Secondary Colour": (255, 191, 191),
        "Game Secondary Font Colour": (63, 63, 63),
        "Game Tertiary Colour": (85, 85, 221),
        "Game Tertiary Font Colour": (217, 217, 217),
        "Adaptive Difficulty": (2, 2, 2),
    }
    settingsClass = Settings()
    loadUpValues()

    meta = "Main Menu"
    game = 1
    getID()


def loadUpValues():
    global settings, text_surface, i, frame
    settings = settingsClass.getSettings()
    settingsClass.applySettings()
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    frame = pygame.time.get_ticks()
    i = 1
    text_surface = None
    settingsInit(settings, font, small_font)
    mainMenuInit(settings, font, title_font)
    gameMenuInit(settings, small_font, font, title_font, splitText)
    game1Init(settings, font, small_font, splitText)
    game2Init(settings, font, title_font, splitText)
    game3Init(settings, font, small_font, splitText)
    gameOverInit(settings, font, splitText)
    leaderboardInit(settings, small_font, font, title_font)


def updateLB(game, data):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    game_url = f"{lb}/game{game}/{user_id}.json"
    response = requests.get(game_url, headers=headers)
    try:
        old_score = float(response.json()["score"])
        if old_score < data["score"]:
            response = requests.put(game_url, json=data, headers=headers)
            if response.status_code == 200:
                logging.info("Entry updated.")
            else:
                logging.critical(
                    f"Error: {response.status_code}\n\n\n {response.text}\n\n\n url: {game_url}\n\n\n data: {data}"
                )
        else:
            logging.info("No new highscore.")
    except:
        logging.warning(f"No previous score found {traceback.format_exc()}")
        response = requests.put(game_url, json=data, headers=headers)
        if response.status_code == 200:  # Success
            logging.info("New entry created.")
        else:
            logging.critical(
                f"Error: {response.status_code}\n\n\n {response.text}\n\n\n url: {game_url}\n\n\n data: {data}"
            )
        old_score = 0
    return old_score


def getLB(game, user_id=None):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if user_id == None:
        game_url = f"{lb}/game{game}.json"
    else:
        game_url = f"{lb}/game{game}/{user_id}.json"
    response = requests.get(game_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logging.critical(
            f"Error: {response.status_code}\n\n\n {response.text}\n\n\n url: {game_url}"
        )
        return None


def getID():
    global user_id, user_key, username
    try:
        try:
            return user_id, user_key, str(username)
        except NameError:
            logging.info("ID and username not loaded, loading ID and username.")
            user_id = None
            with open("id.txt", "r") as file:
                for line in file:
                    user_id, user_key, username = line.split(", ")
                    username = str(username)
                    break
            if user_id:
                return user_id, user_key, str(username)
        logging.warning("id.txt found but empty, creating new ID and username.")
        generateUsername(settings, font, getFps, exitGame)
        return user_id, user_key, str(username)
    except FileNotFoundError:
        logging.warning("id.txt not found, creating new ID and username.")
        generateUsername(settings, font, getFps, exitGame)
        return user_id, user_key, str(username)


def generateUsername(settings, font, getFps, exitGame):
    global user_id, user_key, username
    username = ""
    never = True
    loop = True
    wlc = font.render(
        "Welcome to Sharp Minds!",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    username_text = font.render(
        "Please enter a username:",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    while loop:
        screen.fill(settings["Background Colour"])
        screen.blit(
            wlc,
            (
                settings["Width"] // 2 - wlc.get_width() // 2,
                settings["Height"] // 3 - wlc.get_height() // 2,
            ),
        )
        screen.blit(
            username_text,
            (
                settings["Width"] // 2 - username_text.get_width() // 2,
                settings["Height"] // 2 - username_text.get_height() // 2,
            ),
        )
        text_surface = font.render(
            username, settings["Antialiasing Text"], settings["Background Font Colour"]
        )
        screen.blit(
            text_surface,
            (
                settings["Width"] // 2 - text_surface.get_width() // 2,
                settings["Height"] // 2 + text_surface.get_height() // 2,
            ),
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    if username == "":
                        username = f"Player-{hashlib.sha256(str(random.randint(0, 2 ** 32)).encode()).hexdigest()[:16]}"
                    loop = False
                    break
                else:
                    username += event.unicode
                    username = username[:16]
        getFps(never)
        never = False
        pygame.display.flip()
    user_key = random.randint(0, 2**32)
    user_id = hashlib.sha256(f"{username}{user_key}".encode()).hexdigest()
    with open("id.txt", "w") as file:
        file.write(f"{user_id}, {user_key}, {username}")
    updateLB(
        1,
        {
            "loss": float(0),
            "green": 0,
            "red": float(0),
            "game": 1,
            "id": user_id,
            "username": str(username),
            "score": float(0),
            "max": float(1),
        },
    )
    updateLB(
        2,
        {
            "empty": 0,
            "right": 0,
            "kinda": 0,
            "game": 2,
            "id": user_id,
            "username": str(username),
            "score": float(0),
            "max": float(0),
        },
    )
    updateLB(
        3,
        {
            "duration": float(20000),
            "time": float(20000),
            "pairs": 0,
            "game": 3,
            "id": user_id,
            "username": str(username),
            "score": float(0),
            "max": float(300),
            "loss": 0,
            "difficulty": 1,
        },
    )
    return


def getFps(never):
    global frame, i, text_surface
    if (pygame.time.get_ticks() - frame) > 100 or never:
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


def exitGame():
    pygame.quit()
    sys.exit()


def splitText(
    font, max_width, antialiasing, colour, words="Press ESC to return to games menu"
):
    words = words.split()
    lines = []
    current_line = ""
    return_text = []
    for word in words:
        test_line = current_line + " " + word if current_line else word
        text_width = font.size(test_line)[0]

        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    for text in lines:
        return_text.append(
            font.render(
                text,
                antialiasing,
                colour,
            )
        )
    return return_text


def changeSettings(val):
    global choice, settings
    if val == "Main Menu":
        return "Main Menu"
    elif val == "Save and Leave":
        choice["Adaptive Difficulty"] = settings["Adaptive Difficulty"]
        settingsClass.saveSettings()
        del choice["Adaptive Difficulty"]
        logging.info(f"Settings saved. {datetime.now()}")
        loadUpValues()
        return "Main Menu"
    elif val == "Save":
        choice["Adaptive Difficulty"] = settings["Adaptive Difficulty"]
        settingsClass.saveSettings()
        del choice["Adaptive Difficulty"]
        logging.info(f"Settings saved. {datetime.now()}")
        loadUpValues()
    elif val == "Default":
        difficulty = settings["Adaptive Difficulty"]
        settings = settingsClass.resetSettings()
        choice = settings.copy()
        choice["Adaptive Difficulty"] = difficulty
        del choice["Font Type"]
        settingsClass.saveSettings()
        del choice["Adaptive Difficulty"]
        logging.info(f"Settings reset. {datetime.now()}")
        loadUpValues()
    return "Settings"


def adjustDifficulty(adjustment):
    global settings, meta, choice
    difficulty1, difficulty2, difficulty3 = settings["Adaptive Difficulty"]
    if game == 1:
        settings["Adaptive Difficulty"] = (
            max(difficulty1 + adjustment, 0.2),
            difficulty2,
            difficulty3,
        )
    elif game == 2:
        settings["Adaptive Difficulty"] = (
            difficulty1,
            max(difficulty2 + adjustment, 0.2),
            difficulty3,
        )
    elif game == 3:
        settings["Adaptive Difficulty"] = (
            difficulty1,
            difficulty2,
            max(difficulty3 + adjustment, 0.2),
        )
    else:
        logging.critical(
            f"Error: Game not found, difficulty not adjusted and sending to main menu {traceback.format_exc()} Game: {game}, adjustment: {adjustment}, score: {new_score}, meta: {meta}"
        )
        meta = "Main Menu"
    choice = settings.copy()
    del choice["Font Type"]
    settingsClass.saveSettings()
    del choice["Adaptive Difficulty"]
    logging.info(f"Adaptive Difficulty saved. {datetime.now()}")


try:
    loadUp()
    # meta = "Game Over"
    # new_score = 530.7385
    # old_score = 200.34
    # game_name = "Expose the Criminal"
    # game = 1
    # adjustment = 0.1

    while True:
        if meta == "Main Menu":
            meta, choice = mainMenuDisplay(settings, screen, font, getFps, exitGame)
        elif meta == "Game Menu":
            meta = gameMenuDisplay(settings, screen, getFps, exitGame)
        elif meta == "Settings":
            scroll = 0
            choice, val = settingsDisplay(
                settings,
                screen,
                font,
                title_font,
                small_font,
                choice,
                getFps,
                exitGame,
                splitText,
            )
            meta = changeSettings(val)
        elif meta == "Quit":
            exitGame()
        elif meta == "Expose the Criminal":
            new_score, adjustment, meta, old_score = game1(
                settings, screen, font, getFps, exitGame, getID, updateLB
            )
            if new_score != None:
                game = 1
                adjustDifficulty(adjustment)
        elif meta == "Memory Experiment":
            new_score, adjustment, meta, old_score = game2(
                settings, screen, font, getFps, exitGame, getID, updateLB, splitText
            )
            if new_score != None:
                game = 2
                adjustDifficulty(adjustment)
        elif meta == "Pattern Rush":
            new_score, adjustment, meta, old_score = game3(
                settings, screen, font, getFps, exitGame, getID, updateLB
            )
            if new_score != None:
                game = 3
                adjustDifficulty(adjustment)
        elif meta == "Game Over":
            meta = gameOverDisplay(
                screen,
                settings,
                font,
                small_title_font,
                bold_font,
                game_names[game - 1],
                new_score,
                old_score,
                adjustment,
                getFps,
                exitGame,
            )
        elif meta == "Leaderboards":
            meta == leaderboardsDisplay(
                settings,
                screen,
                font,
                bold_font,
                small_font,
                game,
                user_id,
                getFps,
                exitGame,
                getLB,
            )
            meta = "Main Menu"
        else:
            logging.warning(
                f"Page '{meta}' is currently in development, sending back to main menu."
            )
            meta = "Main Menu"
        # if settings["FPS Limit"] > 0:
        # limiter = (1/settings["FPS Limit"]) - (pygame.time.get_ticks() - frame) / i
        # logging.debug(f"FPS: {fps}, Limiter: {limiter}, pygame.time.get_ticks(): {pygame.time.get_ticks()}, frame: {frame}, i: {i}")
        # if limiter > 0:
        # pygame.time.Clock().tick(limiter)
        # logging.debug(pygame.time.get_ticks())
        pygame.display.flip()
except KeyboardInterrupt:
    pass
except SystemExit:
    pass
except:
    logging.critical(traceback.format_exc())
    exitGame()

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
                            self.settings[key] = tuple(
                                map(int, value.strip("()").split(", "))
                            )  # Convert to tuple (mainly for RGB values)
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
        if self.settings["Font Type"] == "System":
            font = pygame.font.SysFont(
                self.settings["Font"],
                self.settings["Font Size"],
            )
        else:
            font = pygame.font.Font(
                os.path.join(r"assets/fonts/fonts", self.settings["Font"]),
                self.settings["Font Size"],
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
        choice["Font Size"] = choice["Width"] // choice["Font Size"]
        if os.path.isfile(os.path.join(r"assets/fonts/fonts", self.settings["Font"])):
            self.settings["Font Type"] = "Custom"
        else:
            self.settings["Font Type"] = "System"
        print("Settings saved.")


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
    global content_height, scroll, main_menu_buttons, games_buttons, settings_buttons, meta, font_height, options, colour_picker_buttons, options_buttons
    global choice, settings, text_surface, i, frame, confirmation, confirmation_buttons, current_colour_picker, current_dropdown, input_text, input_selected
    settings = settingsClass.getSettings()
    settingsClass.applySettings()
    frame = pygame.time.get_ticks()
    i = 1
    confirmation, current_colour_picker, current_dropdown, text_surface = (
        None,
        None,
        None,
        None,
    )
    input_text = "#"
    input_selected = False
    font_height = font.size("Save and Leave")[1]
    content_height = (
        len(settings)
        + int(
            (int((settings["Height"] * ((3 / 32) + 0.02))) + font_height * 4)
            / (font_height + settings["Height"] // 200)
        )
    ) * (font_height + settings["Height"] // 200) + (
        settings["Height"] % (font_height + settings["Height"] // 200)
    )
    options_buttons = getOptionsButtons()
    main_menu_buttons = getMainMenuButtons(pygame, settings, font)
    games_buttons = getGamesMenuButtons(pygame, settings)
    settings_buttons = getSettingsButtons(pygame, settings, font)
    confirmation_buttons = getConfirmationButtons(pygame, settings, font)
    colour_picker_buttons = getColourPickerButtons(pygame, settings, font)
    try:
        meta = meta
        scroll = 0
    except:
        meta = "Main Menu"
        scroll = 0
    options = getSettingsOptions(pygame, settings, font)
    choice = settings.copy()
    del choice["Font Type"]


def checkExit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


def checkCollide(loc):
    global current_dropdown, current_colour_picker, input_text, input_selected
    colour_buttons = getColourButtons()
    dropdown_buttons = getDropdownButtons()
    if current_dropdown != None:
        for button in dropdown_buttons.values():
            if button["Pygame Button"].collidepoint(loc):
                print(choice[current_dropdown["Name"]], button["Name"])
                choice[current_dropdown["Name"]] = button["Name"]
        current_dropdown = None
        resetDropdownButtons()
    else:
        for button in colour_buttons.values():
            if button["Pygame Button"].collidepoint(loc):
                if button["Name"] == "Confirm":
                    input_text = input_text[1:].ljust(6, "0")
                    hex = tuple(int(input_text[i : i + 2], 16) for i in (0, 2, 4))
                    choice[current_colour_picker["Name"]] = hex
                    current_colour_picker = None
                    input_text = "#"
                    input_selected = False
                    selectInput(False)
                    resetColourButtons()
                    return
                elif button["Name"] == "Discard":
                    current_colour_picker = None
                    input_text = "#"
                    input_selected = False
                    selectInput(False)
                    resetColourButtons()
                    return
                elif button["Name"] == "Input":
                    input_selected = not input_selected
                    selectInput(input_selected)
                    return
                else:
                    print("Unknown colour picker button.")
        current_colour_picker = None
        input_text = "#"
        input_selected = False
        selectInput(False)
        resetColourButtons()


loadUp()


while True:  # Main loop
    screen.fill(settings["Background Colour"])
    if meta == "Main Menu":
        mainMenuDisplay(settings, screen, font, pygame, main_menu_buttons)
        for event in pygame.event.get():
            checkExit(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in main_menu_buttons:  # Check for each button
                    if button["Pygame Button"].collidepoint(
                        event.pos
                    ):  # Check if location of mouse is within the boundaries of the button when mouse is pressed
                        print(f"Page set from {button["Meta"]} to {meta}")
                        meta = button["Meta"]  # Set page if button is pressed
    elif meta == "Game Menu":
        gameMenuDisplay(settings, screen, font, pygame, games_buttons)
        for event in pygame.event.get():
            checkExit(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for game in games_buttons:  # Check for each button
                    if game["Pygame Button"].collidepoint(
                        event.pos
                    ):  # Check if location of mouse is within the boundaries of the button when mouse is pressed
                        print(f"Page set from {button["Meta"]} to {meta}")
                        meta = game["Meta"]  # Set page if button is pressed
    elif meta == "Settings":
        settingsDisplay(
            settings,
            screen,
            font,
            pygame,
            scroll,
            content_height,
            settings_buttons,
            options,
            choice,
            confirmation,
            confirmation_buttons,
        )
        if current_dropdown != None:
            dropdownDisplay(
                pygame,
                settings,
                font,
                screen,
                current_dropdown["Pygame Button"],
                options[current_dropdown["Name"]],
                scroll,
            )
        if current_colour_picker != None:
            colourPickerDisplay(
                pygame,
                settings,
                font,
                screen,
                current_colour_picker,
                colour_picker_buttons,
                scroll,
                input_text,
            )
        for event in pygame.event.get():
            checkExit(event)
            if event.type == pygame.MOUSEWHEEL:
                scroll = max(
                    0,
                    min(
                        content_height - settings["Height"],
                        scroll - event.y * (font_height + settings["Height"] // 200),
                    ),
                )
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not (current_dropdown == None and current_colour_picker == None):
                    checkCollide(event.pos)
                elif confirmation == None:
                    for button in options_buttons.values():  # Check for each button
                        if button["Pygame Button"].collidepoint(
                            (event.pos[0], event.pos[1] + scroll)
                        ):
                            if button["Type"] == "Dropdown":
                                current_dropdown = button
                                print("Dropdown")
                            elif button["Type"] == "Colour Picker":
                                current_colour_picker = button
                                input_text = "#{:02X}{:02X}{:02X}".format(
                                    *choice[current_colour_picker["Name"]]
                                )
                                print("Colour Picker")
                if confirmation != None:
                    for button in confirmation_buttons:
                        if button["Pygame Button"].collidepoint(event.pos):
                            if button["Name"] == "Confirm":
                                if confirmation == "Default":
                                    print("Default confirmation")
                                    settings = settingsClass.resetSettings()
                                    choice = settings.copy()
                                    del choice["Font Type"]
                                    with open("settings.txt", "w") as file:
                                        for key, value in choice.items():
                                            file.write(f'"{key}": {value},\n')
                                    print("Settings reset.")
                                    loadUpValues()
                                elif confirmation == "Discard":
                                    choice = settings.copy()
                                    del choice["Font Type"]
                                    print("Settings discarded.")
                                elif confirmation == "Main Menu":
                                    choice = settings.copy()
                                    del choice["Font Type"]
                                    meta = "Main Menu"
                                else:
                                    print(
                                        f"Error: Unknown request. {confirmation}, {button["Name"]}"
                                    )
                                confirmation = None
                            elif button["Name"] == "Decline":
                                confirmation = None
                            else:
                                print(f"Error: Unknown confirmation button. {button}")
                for button in settings_buttons:  # Check for each button
                    if button["Pygame Button"].collidepoint(event.pos):
                        if any(
                            choice.get(k) != settings[k]
                            for k in settings
                            if k != "Font Type"
                        ):
                            if button["Meta"] == "Save":
                                settingsClass.saveSettings()
                                print("Settings saved.")
                                loadUpValues()
                            elif button["Meta"] == "Save and Leave":
                                settingsClass.saveSettings()
                                meta = "Main Menu"
                                print("Settings saved and page set to Main Menu")
                                loadUpValues()
                            elif button["Meta"] == "Discard":
                                if confirmation == None:
                                    confirmation = "Discard"
                        if button["Meta"] == "Default":
                            if confirmation == None:
                                print("Settings returned to default.")
                                confirmation = "Default"
                        elif button["Meta"] == "Main Menu":
                            if (
                                any(
                                    choice.get(k) != settings[k]
                                    for k in settings
                                    if k != "Font Type"
                                )
                                and confirmation == None
                            ):
                                confirmation = "Main Menu"
                            elif confirmation == None:
                                meta = "Main Menu"
            if event.type == pygame.KEYDOWN and input_selected:
                if event.key == pygame.K_BACKSPACE:
                    if len(input_text) > 1:
                        input_text = input_text[:-1]
                elif event.unicode.upper() in "0123456789ABCDEF":
                    if len(input_text) != 7:
                        input_text += event.unicode.upper()
    elif meta == "Quit":
        pygame.quit()
        sys.exit()
    # FPS Counter
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
    # if settings["FPS Limit"] > 0:
    # limiter = (1/settings["FPS Limit"]) - (pygame.time.get_ticks() - frame) / i
    # print(f"FPS: {fps}, Limiter: {limiter}, pygame.time.get_ticks(): {pygame.time.get_ticks()}, frame: {frame}, i: {i}")
    # if limiter > 0:
    # pygame.time.Clock().tick(limiter)
    # print(pygame.time.get_ticks())
    pygame.display.flip()

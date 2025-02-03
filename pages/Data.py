import os


def getMainMenuButtons(pygame, settings, font):
    text = font.size("Leaderboards and Personal Bests")
    # Screen is split into 5 sections vertically for 5 buttons each section takes 12% of the screen with 1% as a gap between each button and 32% to write the title of the Screen
    # The width is set to half the screen and is centered in the middle of the screen
    main_menu_buttons = [
        {
            "Name": "Games Menu",
            "Pygame Button": pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) // 2,
                settings["Height"] // 3,
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour": settings["Button Primary Colour"],
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Game Menu",
        },
        {
            "Name": "Leaderboards and Personal Bests",
            "Pygame Button": pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) // 2,
                settings["Height"] // 3 + (text[1] + settings["Height"] // 18),
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Font Colour": settings["Font Secondary Colour"],
            "Meta": "Leaderboards",
        },
        {
            "Name": "Friends",
            "Pygame Button": pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) // 2,
                settings["Height"] // 3 + (text[1] + settings["Height"] // 18) * 2,
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour": settings["Button Tertiary Colour"],
            "Font Colour": settings["Font Tertiary Colour"],
            "Meta": "Friends",
        },
        {
            "Name": "Settings",
            "Pygame Button": pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) // 2,
                settings["Height"] // 3 + (text[1] + settings["Height"] // 18) * 3,
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour": settings["Button Quaternary Colour"],
            "Font Colour": settings["Font Quaternary Colour"],
            "Meta": "Settings",
        },
        {
            "Name": "Quit",
            "Pygame Button": pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) // 2,
                settings["Height"] // 3 + (text[1] + settings["Height"] // 18) * 4,
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour": settings["Button Quinary Colour"],
            "Font Colour": settings["Font Quinary Colour"],
            "Meta": "Quit",
        },
    ]
    return main_menu_buttons


def getGamesMenuButtons(pygame, settings):
    if settings["Font Type"] == "System":
        text = pygame.font.SysFont(settings["Font"], settings["Font Size"] // 2).size(
            "Back to Main Menu"
        )
    else:
        text = pygame.font.Font(
            os.path.join(r"assets/fonts/fonts", settings["Font"]),
            settings["Font Size"] // 2,
        ).size("Back to Main Menu")
    games_buttons = [
        {
            "Name": "Expose the Impostor",
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Expose the Impostor",
            "Image": pygame.image.load("assets/images/blank.jpg"),
        },
        {
            "Name": "Memory Experiment",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 32) // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Memory Experiment",
            "Image": pygame.image.load("assets/images/blank.jpg"),
        },
        {
            "Name": "Pattern Rush",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 63) // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Pattern Rush",
            "Image": pygame.image.load("assets/images/blank.jpg"),
        },
        {
            "Name": "Back to Main Menu",
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                settings["Height"] // 16,
                text[0] + settings["Width"] // 64,
                text[1] + settings["Height"] // 90,
            ),
            "Colour": settings["Button Quinary Colour"],
            "Font Colour": settings["Font Quinary Colour"],
            "Meta": "Main Menu",
        },
    ]

    return games_buttons


def getDefaultSettings():
    default_settings = {
        "Width": 1920,
        "Height": 1080,
        "Window Type": "Borderless",
        "Show FPS": True,
        "FPS Limit": 0,
        "Background Colour": (31, 31, 31),
        "Background Font Colour": (217, 217, 217),
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
        "Game Primary Colour": (168, 213, 186),
        "Game Secondary Colour": (255, 154, 162),
        "Game Tertiary Colour": (255, 243, 176),
        "Adaptive Difficulty": 1,
        # "Scroll Speed": 100,

    }
    return default_settings


def getSettingsButtons(pygame, settings, font):
    text_width, text_height = font.size("Save and Leave")
    text_height = text_height // 2
    text_width = text_width // 2
    buttons = [
        # Save and Leave
        {
            "Name": "Save and Leave",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 100) // 128 - (text_width * 5),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Primary Colour"],
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Save and Leave",
        },
        # Save
        {
            "Name": "Save",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 105) // 128 - (text_width * 4),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Font Colour": settings["Font Secondary Colour"],
            "Meta": "Save",
        },
        # Discard
        {
            "Name": "Discard",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 110) // 128 - (text_width * 3),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Quinary Colour"],
            "Font Colour": settings["Font Quinary Colour"],
            "Meta": "Discard",
        },
        # Default
        {
            "Name": "Default",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 115) // 128 - (text_width * 2),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Quaternary Colour"],
            "Font Colour": settings["Font Quaternary Colour"],
            "Meta": "Default",
        },
        # Main Menu
        {
            "Name": "Main Menu",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 120) // 128 - text_width,
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Tertiary Colour"],
            "Font Colour": settings["Font Tertiary Colour"],
            "Meta": "Main Menu",
        },
    ]
    return buttons


def getSettingsOptions(settings, font):
    options = {
        "Width": {"Options": [3840, 2560, 1920, 1440, 1366, 1280, 1024]},
        "Height": {"Options": [2160, 1440, 1080, 768, 720]},
        "Window Type": {"Options": ["Borderless", "Fullscreen", "Windowed"]},
        "Show FPS": {"Options": [True, False]},
        "FPS Limit": {"Options": [0, 30, 60, 120, 144, 165, 240]},
        "Font": {
            "Options": [
                "arial",
                "verdana",
                "timesnewroman",
                "couriernew",
                "comicsansms",
                "georgia",
                "trebuchetms",
                "lucidaconsole",
                "tahoma",
                "impact",
            ]
        },
        "Bold Font": {"Options": []},
        "Italic Font": {"Options": []},
        "BoldItalic Font": {"Options": []},
        "Font Size": {"Options": [48, 56, 64, 72, 80, 128, 160]},
        "Antialiasing Text": {"Options": [True, False]},
        # "Adaptive Difficulty": {"Options": [1, 2, 3, 4, 5, 6, 7]},
        # "Scroll Speed": {"Options": [50, 75, 100, 125, 150]},
    }
    dir = r"assets/fonts/fonts"
    if os.path.exists(dir):
        for file in os.listdir(dir):
            if file.endswith((".ttf", ".otf")):
                if "Bold" in file and "Italic" in file:
                    options["BoldItalic Font"]["Options"].append(file)
                elif "Italic" in file:
                    options["Italic Font"]["Options"].append(file)
                elif "Bold" in file:
                    options["Bold Font"]["Options"].append(file)
                else:
                    options["Font"]["Options"].append(file)
    else:
        print(f"Directory, {dir}, does not exist")

    for index, choice in enumerate(options["Font Size"]["Options"]):
        options["Font Size"]["Options"][index] = settings["Width"] // choice
    for option in options.values():
        largest = max(font.size(str(choice))[0] for choice in option["Options"])
        option["Largest"] = largest
    return options


def getConfirmationButtons(pygame, settings, font):
    text_size = font.size("Confirm")
    buttons = [
        {
            "Pygame Button": pygame.Rect(
                settings["Width"] * 28 // 60 - text_size[0],
                settings["Height"] // 2,
                text_size[0] + settings["Width"] // 96,
                text_size[1] // 2 + settings["Height"] // 54,
            ),
            "Name": "Confirm",
            "Colour": settings["Button Quinary Colour"],
            "Font Colour": settings["Font Quinary Colour"],
        },
        {
            "Pygame Button": pygame.Rect(
                settings["Width"] * 32 // 60,
                settings["Height"] // 2,
                text_size[0] + settings["Width"] // 96,
                text_size[1] // 2 + settings["Height"] // 54,
            ),
            "Name": "Decline",
            "Colour": settings["Button Primary Colour"],
            "Font Colour": settings["Font Primary Colour"],
        },
    ]
    return buttons


def getColourPickerButtons(settings, font):
    widest_char_width = max(font.size(str(char))[0] for char in "0123456789ABCDEF")
    text_size = (
        widest_char_width * 6 + font.size("#")[0] + settings["Width"] // 32,
        font.size("#")[1] + settings["Height"] // 100 - 1,
    )
    buttons = [
        {
            "Name": "Input",
            "Size": text_size,
            "Buffer Size": (
                settings["Width"] // 100,
                # (settings["Width"] * 21) // 100,
                (settings["Height"] * 3) // 128 + text_size[1] * 2,
            ),
            "Colour": settings["Input Background Colour"],
            "Font Colour": settings["Input Font Colour"],
        },
        {
            "Name": "Selected Input",
            "Size": text_size,
            "Buffer Size": (
                settings["Width"] // 100,
                # (settings["Width"] * 21) // 100,
                (settings["Height"] * 3) // 128 + text_size[1] * 2,
            ),
            "Colour": settings["Selected Input Colour"],
            "Font Colour": settings["Input Font Colour"],
        },
        {
            "Name": "Confirm",
            "Size": text_size,
            "Buffer Size": (
                settings["Width"] // 100,
                # (settings["Width"] * 21) // 100,
                settings["Height"] // 64 + text_size[1],
            ),
            "Text": "Confirm",
            "Colour": settings["Button Primary Colour"],
            "Font Colour": settings["Font Primary Colour"],
        },
        {
            "Name": "Discard",
            "Size": text_size,
            "Buffer Size": (settings["Width"] // 100, settings["Height"] // 128),
            # "Buffer Size": ((settings["Width"] * 21) // 100, settings["Height"] // 128),
            "Text": "Discard",
            "Colour": settings["Button Quinary Colour"],
            "Font Colour": settings["Font Quinary Colour"],
        },
    ]
    return buttons

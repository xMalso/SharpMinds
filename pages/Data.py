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
        text = pygame.font.SysFont(
            settings["Font"], settings["Width"] // settings["Font Size Divider"] // 2
        ).size("Back to Main Menu")
    else:
        text = pygame.font.Font(
            settings["Font"], settings["Width"] // settings["Font Size Divider"] // 2
        ).size("Back to Main Menu")
    # Screen is split into 3 sections horizontally for 3 games each section takes 30/94 of the screen with 1/94 as a gap between each game
    # The height of each section section is 8/15
    #  of the screen with 1/15
    #  as a gap above and below with 5/15
    #  extra to write the title of the Screen

    games_buttons = [
        {
            "Name": "Game 1",
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Game 1",
            "Image": pygame.image.load("assets/images/blank.jpg"),
        },
        {
            "Name": "Game 2",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 32) // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Game 2",
            "Image": pygame.image.load("assets/images/blank.jpg"),
        },
        {
            "Name": "Game 3",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 63) // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Game 3",
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
        "Background": (31, 31, 31),
        "Background Font Colour": (217, 217, 217),
        "Dropdown Background": (63, 63, 63),
        "Dropdown Font Colour": (217, 217, 217),
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
        "Font": "assets\\fonts\\opendyslexic-0.91.12\\compiled\\OpenDyslexic-Regular.otf",
        "Bold Font": "assets\\fonts\\opendyslexic-0.91.12\\compiled\\OpenDyslexic-Bold.otf",
        "Italic Font": "assets\\fonts\\opendyslexic-0.91.12\\compiled\\OpenDyslexic-Italic.otf",
        "BoldItalic Font": "assets\\fonts\\opendyslexic-0.91.12\\compiled\\OpenDyslexic-Bold-Italic.otf",
        "Font Type": "Custom",
        "Font Size Divider": 64,
        "Antialiasing Text": True,
        "Game Primary Colour": (168, 213, 186),
        "Game Secondary Colour": (255, 154, 162),
        "Game Tertiary Colour": (255, 243, 176),
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


def getSettingsOptions(pygame):
    options = {
        "Width": [1920, 1600, 1366, 1280, 1024, 800, 640],
        "Height": [1080, 900, 768, 720, 600, 480],
        "Window Type": ["Borderless", "Fullscreen", "Windowed"],
        "Show FPS": [True, False],
        "FPS Limit": [0, 30, 60, 120, 144, 165, 240],
        # "Background": (rgb tuple),
        # "Background Font Colour": (rgb tuple),
        # "Dropdown Background": (rgb tuple),
        # "Dropdown Font Colour": (rgb tuple),
        # "Button Primary Colour": (rgb tuple),
        # "Font Primary Colour": (rgb tuple),
        # "Button Secondary Colour": (rgb tuple),
        # "Font Secondary Colour": (rgb tuple),
        # "Button Tertiary Colour": (rgb tuple),
        # "Font Tertiary Colour": (rgb tuple),
        # "Button Quaternary Colour": (rgb tuple),
        # "Font Quaternary Colour": (rgb tuple),
        # "Button Quinary Colour": (rgb tuple),
        # "Font Quinary Colour": (rgb tuple),
        "Font": [
            "assets\\fonts\\opendyslexic-0.91.12\\compiled\\OpenDyslexic-Regular.otf"],
        "Bold Font": [
            "assets\\fonts\\opendyslexic-0.91.12\\compiled\\OpenDyslexic-Bold.otf"
        ],
        "Italic Font": [
            "assets\\fonts\\opendyslexic-0.91.12\\compiled\\OpenDyslexic-Italic.otf"
        ],
        "BoldItalic Font": [
            "assets\\fonts\\opendyslexic-0.91.12\\compiled\\OpenDyslexic-Bold-Italic.otf"
        ],
        "Font Type": ["Custom", "System"],
        "Font Size Divider": [48, 56, 64, 72, 80],
        "Antialiasing Text": [True, False],
        # "Game Primary Colour": "rgb tuple",
        # "Game Secondary Colour": "rgb tuple",
        # "Game Tertiary Colour": "rgb tuple",
        # "Scroll Speed": [50, 75, 100, 125, 150],
    }
    options["Font"] += pygame.font.get_fonts()
    return options

def getMainMenuButtons(pygame, settings):
    # Screen is split into 5 sections vertically for 5 buttons each section takes 12% of the screen with 1% as a gap between each button and 32% to write the title of the Screen
    # The width is set to half the screen and is centered in the middle of the screen
    main_menu_buttons = [
        {
            "Name": "Games Menu",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 3) // 8,
                (settings["Height"] * 30) // 100,
                settings["Width"] // 4,
                (settings["Height"] * 10) // 100,
            ),
            "Colour": settings["Button Primary Colour"],
            "Font Colour": settings["Font Primary Colour"],
            "Page": "Game Menu",
        },
        {
            "Name": "Leaderboards and Personal Bests",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 3) // 8,
                (settings["Height"] * 43) // 100,
                settings["Width"] // 4,
                (settings["Height"] * 10) // 100,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Font Colour": settings["Font Secondary Colour"],
            "Page": "Leaderboards",
        },
        {
            "Name": "Friends",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 3) // 8,
                (settings["Height"] * 56) // 100,
                settings["Width"] // 4,
                (settings["Height"] * 10) // 100,
            ),
            "Colour": settings["Button Tertiary Colour"],
            "Font Colour": settings["Font Tertiary Colour"],
            "Page": "Friends",
        },
        {
            "Name": "Settings",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 3) // 8,
                (settings["Height"] * 69) // 100,
                settings["Width"] // 4,
                (settings["Height"] * 10) // 100,
            ),
            "Colour": settings["Button Quaternary Colour"],
            "Font Colour": settings["Font Quaternary Colour"],
            "Page": "Settings",
        },
        {
            "Name": "Quit",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 3) // 8,
                (settings["Height"] * 82) // 100,
                settings["Width"] // 4,
                (settings["Height"] * 10) // 100,
            ),
            "Colour": settings["Button Quinary Colour"],
            "Font Colour": settings["Font Quinary Colour"],
            "Page": "Quit",
        },
    ]
    return main_menu_buttons

def getGamesMenuButtons(pygame, settings):
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
            "Page": "Game 1",
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
            "Page": "Game 2",
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
            "Page": "Game 3",
            "Image": pygame.image.load("assets/images/blank.jpg"),
        },
        {
            "Name": "Back to Main Menu",
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                (settings["Height"] * 1.5) // 16,
                (settings["Width"] * 20) // 94,
                (settings["Height"] * 1) // 16,
            ),
            "Colour": settings["Button Quinary Colour"],
            "Font Colour": settings["Font Quinary Colour"],
            "Page": "Main Menu",
        },
    ]

    return games_buttons

def getDefaultSettings():
    default_settings = {
        "Width": 1920,
        "Height": 1080,
        "Window Type": "Borderless",
        "Background": (52, 53, 65),
        "Button Primary Colour": (99, 139, 102),
        "Button Secondary Colour": (120, 145, 255),
        "Button Tertiary Colour": (255, 120, 80),
        "Button Quaternary Colour": (140, 140, 140),
        "Button Quinary Colour": (255, 102, 68),
        "Background Font": (217, 217, 217),
        "Font Primary Colour": (217, 217, 217),
        "Font Secondary Colour": (217, 217, 217),
        "Font Tertiary Colour": (217, 217, 217),
        "Font Quaternary Colour": (217, 217, 217),
        "Font Quinary Colour": (217, 217, 217),
        "Font": "Arial",
        "Font Size": 30,
        "Antialiasing Text": True,
        "Game Primary Colour": (168, 213, 186),
        "Game Secondary Colour": (255, 154, 162),
        "Game Tertiary Colour": (255, 243, 176),
    }
    return default_settings

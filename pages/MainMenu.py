import pygame


def init(settings, font, title_font):
    makeButtons(settings, font)
    makeText(title_font, settings)


def makeText(title_font, settings):
    global title_text
    title_text = title_font.render(
        "Main Menu", settings["Antialiasing Text"], settings["Font Primary Colour"]
    )


def makeButtons(settings, font):
    text = font.size("Leaderboards and Personal Bests")
    # text = font.size(max(["Games Menu", "Leaderboards", "Friends", "Settings", "Quit"], key=lambda x: font.size(x)[0]))
    global buttons
    buttons = [
        {
            "Text": font.render(
                "Games Menu",
                settings["Antialiasing Text"],
                settings["Font Primary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) // 2,
                # settings["Height"] // 3,
                settings["Height"] // 3 + (text[1] + settings["Height"] // 18),
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour": settings["Button Primary Colour"],
            "Meta": "Game Menu",
        },
        {
            "Text": font.render(
                "Leaderboards",
                settings["Antialiasing Text"],
                settings["Font Secondary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) // 2,
                # settings["Height"] // 3 + (text[1] + settings["Height"] // 18),
                settings["Height"] // 3 + (text[1] + settings["Height"] // 18) * 2,
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Meta": "Leaderboards",
        },
        # {
        #     "Text": font.render("Friends", settings["Antialiasing Text"], settings["Font Tertiary Colour"]),
        #     "Pygame Button": pygame.Rect(
        #         (settings["Width"] - (text[0] + settings["Width"] // 19.2)) // 2,
        # settings["Height"] // 3 + (text[1] + settings["Height"] // 18) * 2,
        #         text[0] + settings["Width"] // 19.2,
        #         text[1] + settings["Height"] // 27,
        #     ),
        #     "Colour": settings["Button Tertiary Colour"],
        #     "Meta": "Friends",
        # },
        {
            "Text": font.render(
                "Settings",
                settings["Antialiasing Text"],
                settings["Font Quaternary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) // 2,
                settings["Height"] // 3 + (text[1] + settings["Height"] // 18) * 3,
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour": settings["Button Quaternary Colour"],
            "Meta": "Settings",
        },
        {
            "Text": font.render(
                "Quit", settings["Antialiasing Text"], settings["Font Quinary Colour"]
            ),
            "Pygame Button": pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) // 2,
                settings["Height"] // 3 + (text[1] + settings["Height"] // 18) * 4,
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour": settings["Button Quinary Colour"],
            "Meta": "Quit",
        },
    ]


def displayPage(settings, screen, font, getFps, exitGame):
    never = True
    while True:
        screen.fill(settings["Background Colour"])
        screen.blit(
            title_text,
            (
                settings["Width"] // 2 - title_text.get_width() // 2,
                # (settings["Height"] * 17) // 100 - title_text.get_height() // 2,
                (settings["Height"] * 25) // 100 - title_text.get_height() // 2,
            ),
        )
        for button in buttons:
            pygame.draw.rect(
                screen,
                button["Colour"],
                button["Pygame Button"],
                border_radius=settings["Width"] // 40,
            )
            screen.blit(
                button["Text"],
                (
                    button["Pygame Button"].centerx - button["Text"].get_width() // 2,
                    button["Pygame Button"].centery - button["Text"].get_height() // 2,
                ),
            )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:  # Check for each button
                    if button["Pygame Button"].collidepoint(event.pos):
                        meta = button["Meta"]
                        if meta == "Settings":
                            choice = settings.copy()
                            del choice["Font Type"]
                            del choice["Adaptive Difficulty"]
                            return meta, choice
                        return meta, None
        getFps(never)
        never = False
        pygame.display.flip()

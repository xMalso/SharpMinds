def makeButtons(pygame, settings, font):
    text = font.size("Leaderboards and Personal Bests")
    # Screen is split into 5 sections vertically for 5 buttons each section takes 12% of the screen with 1% as a gap between each button and 32% to write the title of the Screen
    # The width is set to half the screen and is centered in the middle of the screen
    main_menu_buttons = [
        {
            "Name":
            "Games Menu",
            "Pygame Button":
            pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) //
                2,
                settings["Height"] // 3,
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour":
            settings["Button Primary Colour"],
            "Font Colour":
            settings["Font Primary Colour"],
            "Meta":
            "Game Menu",
        },
        {
            "Name":
            "Leaderboards and Personal Bests",
            "Pygame Button":
            pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) //
                2,
                settings["Height"] // 3 + (text[1] + settings["Height"] // 18),
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour":
            settings["Button Secondary Colour"],
            "Font Colour":
            settings["Font Secondary Colour"],
            "Meta":
            "Leaderboards",
        },
        {
            "Name":
            "Friends",
            "Pygame Button":
            pygame.Rect(
                (settings["Width"] -
                 (text[0] + settings["Width"] // 19.2)) // 2,
                settings["Height"] // 3 +
                (text[1] + settings["Height"] // 18) * 2,
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour":
            settings["Button Tertiary Colour"],
            "Font Colour":
            settings["Font Tertiary Colour"],
            "Meta":
            "Friends",
        },
        {
            "Name":
            "Settings",
            "Pygame Button":
            pygame.Rect(
                (settings["Width"] -
                 (text[0] + settings["Width"] // 19.2)) // 2,
                settings["Height"] // 3 +
                (text[1] + settings["Height"] // 18) * 3,
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour":
            settings["Button Quaternary Colour"],
            "Font Colour":
            settings["Font Quaternary Colour"],
            "Meta":
            "Settings",
        },
        {
            "Name":
            "Quit",
            "Pygame Button":
            pygame.Rect(
                (settings["Width"] - (text[0] + settings["Width"] // 19.2)) //
                2,
                settings["Height"] // 3 +
                (text[1] + settings["Height"] // 18) * 4,
                text[0] + settings["Width"] // 19.2,
                text[1] + settings["Height"] // 27,
            ),
            "Colour":
            settings["Button Quinary Colour"],
            "Font Colour":
            settings["Font Quinary Colour"],
            "Meta":
            "Quit",
        },
    ]
    return main_menu_buttons


def displayPage(pygame, sys, settings, screen, font, title_font,
                getFps):
    choice = None
    buttons = makeButtons(pygame, settings, font)
    title_text = title_font.render("Main Menu", settings["Antialiasing Text"],
                                   settings["Font Primary Colour"])
    while True:
        screen.fill(settings["Background Colour"])
        screen.blit(
            title_text,
            (
                settings["Width"] // 2 - title_text.get_width() // 2,
                (settings["Height"] * 17) // 100 -
                title_text.get_height() // 2,
            ),
        )
        for button in buttons:
            pygame.draw.rect(screen,
                             button["Colour"],
                             button["Pygame Button"],
                             border_radius=25)
            button_text = font.render(button["Name"],
                                      settings["Antialiasing Text"],
                                      button["Font Colour"])
            screen.blit(
                button_text,
                (
                    button["Pygame Button"].x +
                    button["Pygame Button"].width // 2 -
                    button_text.get_width() // 2,
                    button["Pygame Button"].y +
                    button["Pygame Button"].height // 2 -
                    button_text.get_height() // 2,
                ),
            )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:  # Check for each button
                    if button["Pygame Button"].collidepoint(
                            event.pos
                    ):  # Check if location of mouse is within the boundaries of the button when mouse is pressed
                        meta = button["Meta"]  # Set page if button is pressed
                        if meta == "Settings":
                            choice = settings.copy()
                            del choice["Font Type"]
                            del choice["Adaptive Difficulty"]
                        return meta, choice
        getFps()
        pygame.display.flip()

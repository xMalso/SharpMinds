def displayPage(pygame, sys, os, settings, screen, font, buttons, getFps):
    choice = None
    if settings["Font Type"] == "System":
        title_font = pygame.font.SysFont(
            settings["Font"],
            settings["Font Size"] * 3,
            bold=True,
        )
    else:
        title_font = pygame.font.Font(
            os.path.join(r"assets/fonts/fonts", settings["Bold Font"]),
            settings["Font Size"] * 3,
        )
    title_text = title_font.render(
        "Main Menu", settings["Antialiasing Text"], settings["Font Primary Colour"]
    )
    while True:
        screen.fill(settings["Background Colour"])
        screen.blit(
            title_text,
            (
                settings["Width"] // 2 - title_text.get_width() // 2,
                (settings["Height"] * 17) // 100 - title_text.get_height() // 2,
            ),
        )
        for button in buttons:
            pygame.draw.rect(
                screen, button["Colour"], button["Pygame Button"], border_radius=25
            )
            button_text = font.render(
                button["Name"], settings["Antialiasing Text"], button["Font Colour"]
            )
            screen.blit(
                button_text,
                (
                    button["Pygame Button"].x
                    + button["Pygame Button"].width // 2
                    - button_text.get_width() // 2,
                    button["Pygame Button"].y
                    + button["Pygame Button"].height // 2
                    - button_text.get_height() // 2,
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

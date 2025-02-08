def displayPage(pygame, sys, os, settings, screen, font, buttons, getFps):
    back = buttons[-1]
    if settings["Font Type"] == "System":
        title_font = pygame.font.SysFont(settings["Font"],
                                         settings["Font Size"] * 3,
                                         bold=True)
    else:
        title_font = pygame.font.Font(
            os.path.join(r"assets/fonts/fonts", settings["Bold Font"]),
            settings["Font Size"] * 3,
        )
    title_text = title_font.render("Games Menu", settings["Antialiasing Text"],
                                   settings["Font Primary Colour"])
    while True:
        screen.fill(settings["Background Colour"])
        screen.blit(
            title_text,
            (
                settings["Width"] // 2 - title_text.get_width() // 2,
                (settings["Height"] * 2) // 16 - title_text.get_height() // 2,
            ),
        )
        for button in buttons[:-1]:
            button_height, button_width = (
                button["Pygame Button"].height,
                button["Pygame Button"].width,
            )
            height = 408
            width = 370
            scale = max(button_width / width, button_height / height)
            cropped_surface = pygame.Rect(
                0,
                0,
                button_width / scale,
                button_height / scale,
            )
            cropped_image = button["Image"].subsurface(cropped_surface)
            scaled_image = pygame.transform.scale(
                cropped_image, (button_width, button_height))
            screen.blit(scaled_image, button["Pygame Button"].topleft)
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
                    button["Pygame Button"].height +
                    button_text.get_height() // 2,
                ),
            )
        if settings["Font Type"] == "System":
            back_font = pygame.font.SysFont(settings["Font"],
                                            settings["Font Size"] // 2)
        else:
            back_font = pygame.font.Font(
                os.path.join(r"assets/fonts/fonts", settings["Font"]),
                settings["Font Size"] // 2,
            )
        pygame.draw.rect(screen,
                         back["Colour"],
                         back["Pygame Button"],
                         border_radius=25)
        back_text = back_font.render(back["Name"],
                                     settings["Antialiasing Text"],
                                     button["Font Colour"])
        screen.blit(
            back_text,
            (
                back["Pygame Button"].x + back["Pygame Button"].width // 2 -
                back_text.get_width() // 2,
                back["Pygame Button"].y + back["Pygame Button"].height // 2 -
                back_text.get_height() // 2,
            ),
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for game in buttons:  # Check for each button
                    if game["Pygame Button"].collidepoint(
                            event.pos
                    ):  # Check if location of mouse is within the boundaries of the button when mouse is pressed
                        meta = game["Meta"]  # Set page if button is pressed
                        return meta
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                meta = "Main Menu"
                return meta
        getFps()
        pygame.display.flip()

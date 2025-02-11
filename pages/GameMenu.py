def init(pygame, settings, small_font):
    makeButtons(pygame, settings, small_font)

def makeButtons(pygame, settings, small_font):
    text = small_font.size("Back to Main Menu")
    games_buttons = [
        {
            "Name":
            "Expose the Impostor",
            "Pygame Button":
            pygame.Rect(
                settings["Width"] // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Font Colour":
            settings["Font Primary Colour"],
            "Meta":
            "Expose the Impostor",
            "Image":
            pygame.image.load("assets/images/game1.jpg"),
        },
        {
            "Name":
            "Memory Experiment",
            "Pygame Button":
            pygame.Rect(
                (settings["Width"] * 32) // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Font Colour":
            settings["Font Primary Colour"],
            "Meta":
            "Memory Experiment",
            "Image":
            pygame.image.load("assets/images/game2.jpg"),
        },
        {
            "Name":
            "Pattern Rush",
            "Pygame Button":
            pygame.Rect(
                (settings["Width"] * 63) // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Font Colour":
            settings["Font Primary Colour"],
            "Meta":
            "Pattern Rush",
            "Image":
            pygame.image.load("assets/images/game3.jpg"),
        },
        {
            "Name":
            "Back to Main Menu",
            "Pygame Button":
            pygame.Rect(
                settings["Width"] // 94,
                settings["Height"] // 16,
                text[0] + settings["Width"] // 64,
                text[1] + settings["Height"] // 90,
            ),
            "Colour":
            settings["Button Quinary Colour"],
            "Font Colour":
            settings["Font Quinary Colour"],
            "Meta":
            "Main Menu",
        },
    ]

    return games_buttons


def displayPage(pygame, sys, settings, screen, font, title_font, small_font,
                getFps):
    buttons = makeButtons(pygame, settings, small_font)
    back = buttons[-1]
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
        pygame.draw.rect(screen,
                         back["Colour"],
                         back["Pygame Button"],
                         border_radius=25)
        back_text = small_font.render(back["Name"],
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

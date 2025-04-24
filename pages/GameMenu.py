import pygame


def init(settings, small_font, font, title_font, splitText):
    global title_text, return_text
    title_text = title_font.render(
        "Games Menu", settings["Antialiasing Text"], settings["Font Primary Colour"]
    )
    return_text = splitText(font, settings["Width"] // 4, settings["Antialiasing Text"], settings["Background Font Colour"], words="Press ESC to return to main menu")
    makeButtons(settings, font, small_font)


def makeButtons(settings, font, small_font):
    global buttons
    text = small_font.size("Back to Main Menu")
    buttons = [
        {
            "Text": font.render(
                "Expose the Criminal",
                settings["Antialiasing Text"],
                settings["Font Primary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Meta": "Expose the Criminal",
            "Image": pygame.image.load("assets/images/game1.jpg"),
        },
        {
            "Text": font.render(
                "Memory Experiment",
                settings["Antialiasing Text"],
                settings["Font Primary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 32) // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Meta": "Memory Experiment",
            "Image": pygame.image.load("assets/images/game2.jpg"),
        },
        {
            "Text": font.render(
                "Pattern Rush",
                settings["Antialiasing Text"],
                settings["Font Primary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 63) // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Meta": "Pattern Rush",
            "Image": pygame.image.load("assets/images/game3.jpg"),
        },
        {
            "Text": small_font.render(
                "Back to Main Menu",
                settings["Antialiasing Text"],
                settings["Font Primary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                settings["Height"] // 16,
                text[0] + settings["Width"] // 64,
                text[1] + settings["Height"] // 90,
            ),
            "Colour": settings["Button Quinary Colour"],
            "Meta": "Main Menu",
        },
    ]


def displayPage(settings, screen, getFps, exitGame):
    never = True
    while True:
        screen.fill(settings["Background Colour"])
        screen.blit(
            title_text,
            (
                settings["Width"] // 2 - title_text.get_width() // 2,
                (settings["Height"] * 2) // 16 - title_text.get_height() // 2,
            ),
        )
        height = settings["Height"] // 200
        for line in return_text:
            screen.blit(
                line,
                (
                    settings["Width"] * 7 // 8
                    - line.get_width() // 2
                    - settings["Width"] // 200,
                    height,
                ),
            )
            height += line.get_height()

        for button in buttons[:-1]:
            button_height, button_width = (
                button["Pygame Button"].height,
                button["Pygame Button"].width,
            )
            height = button["Image"].get_height()
            width = button["Image"].get_width()
            if button["Meta"] == "Expose the Criminal":
                scale = max(button_width / width, button_height / height)
                left = (width - button_width / scale) / 2
                top = (height - button_height / scale) / 2
                cropped_surface = pygame.Rect(
                    left,
                    top,
                    button_width / scale,
                    button_height / scale,
                )
                cropped_image = button["Image"].subsurface(cropped_surface)
                scaled_image = pygame.transform.scale(
                    cropped_image, (button_width, button_height)
                )
                screen.blit(scaled_image, button["Pygame Button"].topleft)
            else:
                scale = min(button_width / width, button_height / height)
                left = (width - button_width / scale) / 2 * scale
                top = (height - button_height / scale) / 2 * scale
                button_width, button_height = (width * scale, height * scale)
                scaled_image = pygame.transform.scale(
                    button["Image"], (button_width, button_height)
                )
                screen.blit(
                    scaled_image,
                    (button["Pygame Button"].x - left, button["Pygame Button"].y - top),
                )
            screen.blit(
                button["Text"],
                (
                    button["Pygame Button"].centerx - button["Text"].get_width() // 2,
                    button["Pygame Button"].bottom + button["Text"].get_height() // 2,
                ),
            )
        pygame.draw.rect(
            screen,
            buttons[-1]["Colour"],
            buttons[-1]["Pygame Button"],
            border_radius=settings["Width"] // 40,
        )
        screen.blit(
            buttons[-1]["Text"],
            (
                buttons[-1]["Pygame Button"].centerx - buttons[-1]["Text"].get_width() // 2,
                buttons[-1]["Pygame Button"].centery - buttons[-1]["Text"].get_height() // 2,
            ),
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for game in buttons:  # Check for each button
                    if game["Pygame Button"].collidepoint(event.pos):
                        meta = game["Meta"]
                        return meta
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                meta = "Main Menu"
                return meta
        getFps(never)
        never = False
        pygame.display.flip()

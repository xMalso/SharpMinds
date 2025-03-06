global pygame
import pygame


def init(settings, small_font):
    makeButtons(settings, small_font)


def makeButtons(settings, small_font):
    global buttons
    text = small_font.size("Back to Main Menu")
    buttons = [
        {
            "Name": "Expose the Criminal",
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                (settings["Height"] * 4) // 16,
                (settings["Width"] * 30) // 94,
                (settings["Height"] * 10) // 16,
            ),
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Expose the Criminal",
            "Image": pygame.image.load("assets/images/game1.jpg"),
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
            "Image": pygame.image.load("assets/images/game2.jpg"),
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
            "Image": pygame.image.load("assets/images/game3.jpg"),
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


def displayPage(settings, screen, font, title_font, small_font, getFps, exit):
    never = True
    back = buttons[-1]
    title_text = title_font.render(
        "Games Menu", settings["Antialiasing Text"], settings["Font Primary Colour"]
    )
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
            height = button["Image"].get_height()
            width = button["Image"].get_width()
            if button["Name"] == "Expose the Criminal":
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
                    + button["Pygame Button"].height
                    + button_text.get_height() // 2,
                ),
            )
        pygame.draw.rect(
            screen,
            back["Colour"],
            back["Pygame Button"],
            border_radius=settings["Width"] // 40,
        )
        back_text = small_font.render(
            back["Name"], settings["Antialiasing Text"], button["Font Colour"]
        )
        screen.blit(
            back_text,
            (
                back["Pygame Button"].x
                + back["Pygame Button"].width // 2
                - back_text.get_width() // 2,
                back["Pygame Button"].y
                + back["Pygame Button"].height // 2
                - back_text.get_height() // 2,
            ),
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
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

import os
def displayPage(settings, screen, font, pygame, buttons):
    if settings["Font Type"] == "System":
        title_font = pygame.font.SysFont(
            settings["Font"],
            settings["Width"] // settings["Font Size Divider"] * 3,
            bold=True,
        )
    else:
        title_font = pygame.font.Font(
            os.path.join(r"assets/fonts/fonts", settings["Bold Font"]),
            settings["Width"] // settings["Font Size Divider"] * 3,
        )
    title_text = title_font.render(
        "Main Menu", settings["Antialiasing Text"], settings["Font Primary Colour"]
    )
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

def displayPage(settings, screen, font, pygame, buttons):
    back = buttons[-1]
    title_font = pygame.font.SysFont(settings["Font"], settings["Font Size"] * 3)
    title_text = title_font.render(
        "Games Menu", settings["Antialiasing Text"], settings["Font Primary Colour"]
    )
    screen.blit(
        title_text,
        (
            settings["Width"] // 2 - title_text.get_width() // 2,
            (settings["Height"] * 2) // 16 - title_text.get_height() // 2,
        ),
    )
    for button in buttons[:-1]:
        scaled_image = pygame.transform.scale(button['Image'], (button['Pygame Button'].width, button['Pygame Button'].height))
        screen.blit(scaled_image, button["Pygame Button"].topleft)
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
    pygame.draw.rect(screen, back["Colour"], back["Pygame Button"], border_radius=25)
    back_text = font.render(
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
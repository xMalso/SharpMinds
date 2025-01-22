def displayPage(settings, screen, font, pygame, buttons):
    title_font = pygame.font.SysFont(settings["Font"], settings["Font Size"] * 1)
    title_text = title_font.render(
        "Games Menu", settings["Antialiasing Text"], settings["Font Primary Colour"]
    )
    del title_font
    screen.blit(
        title_text,
        (
            settings["Width"] // 2 - title_text.get_width() // 2,
            (settings["Height"] * 2) // 15 - title_text.get_height() // 2,
        ),
    )
    del title_text
    for button in buttons.values():
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
                + button["Pygame Button"].height // 2
                - button_text.get_height() // 2,
            ),
        )
        # pygame.draw.rect(screen, button['Colour'], button['Pygame Button'])
        # button_text = font.render(button['Name'], settings['Antialiasing Text'], button['Font Colour'])
        # screen.blit(button_text, (button['Pygame Button'].x + button['Pygame Button'].width//2 - button_text.get_width()//2, button['Pygame Button'].y + button['Pygame Button'].height//2 - button_text.get_height()//2))
        del button_text

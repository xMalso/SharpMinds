def displayPage(settings, screen, font, pygame, scroll, content_height, buttons):
    settings_surface = pygame.Surface((settings["Width"], content_height))
    settings_surface.fill(settings["Background"])
    if settings["Font Type"] == "System":
        title_font = pygame.font.SysFont(
            settings["Font"],
            settings["Width"] // settings["Font Size Divider"] * 3,
            bold=True,
        )
    else:
        title_font = pygame.font.Font(
            settings["Bold Font"],
            settings["Width"] // settings["Font Size Divider"] * 3,
        )
    title_text = title_font.render(
        "Settings", settings["Antialiasing Text"], settings["Font Primary Colour"]
    )
    settings_surface.blit(
        title_text,
        (
            settings["Width"] // 2 - title_text.get_width() // 2,
            (settings["Height"]) // 100 + scroll,
        ),
    )
    text_height = font.size("Save and Quit")[1]
    y_offset = text_height * 3 + (settings["Height"] // 50)

    for key, value in settings.items():
        text_surface = font.render(
            f"{key}: {value}", settings["Antialiasing Text"], (255, 255, 255)
        )
        # Check if the text is meant to be visible
        if not (
            y_offset
            > scroll
            - text_height
            + (settings["Height"] * 29) // 32  # Check if below screen
            or y_offset + text_surface.get_height()
            < scroll
            + text_height * 4
            + settings["Height"] // 50  # Check if above scren
        ):
            settings_surface.blit(text_surface, (settings["Width"] // 20, y_offset))

        y_offset += text_height
    for button in buttons:
        pygame.draw.rect(
            screen, button["Colour"], button["Pygame Button"], border_radius=25
        )
        if settings["Font Type"] == "System":
            small_font = pygame.font.SysFont(
                settings["Font"],
                settings["Width"] // (settings["Font Size Divider"] * 2),
            )
        else:
            small_font = pygame.font.Font(
                settings["Font"],
                settings["Width"] // (settings["Font Size Divider"] * 2),
            )
        pygame.draw.rect(
            settings_surface, button["Colour"], button["Pygame Button"], border_radius=25
        )
        button_text = small_font.render(
            button["Name"], settings["Antialiasing Text"], button["Font Colour"]
        )
        settings_surface.blit(
            button_text,
            (
                button["Pygame Button"].x
                + button["Pygame Button"].width // 2
                - button_text.get_width() // 2,
                button["Pygame Button"].y
                + button["Pygame Button"].height // 2
                - button_text.get_height() // 2
                + scroll,
            ),
        )
        # print(button["Pygame Button"])
    # print (buttons)
    screen.blit(settings_surface, (0, -scroll))

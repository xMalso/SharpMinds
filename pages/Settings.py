def displayPage(settings, screen, font, pygame, scroll, content_height, buttons):
    settings_surface = pygame.Surface((settings["Width"], content_height))
    settings_surface.fill(settings["Background"])

    y_offset = settings["Height"] // 8  # Leaves space for back button
    for key, value in settings.items():
        text_surface = font.render(
            f"{key}: {value}", settings["Antialiasing Text"], (255, 255, 255)
        )
        if not (
            y_offset > scroll + (settings["Height"] * 7) // 8
            or y_offset + text_surface.get_height() < scroll + settings["Height"] // 8
        ):
            settings_surface.blit(text_surface, (settings["Width"] // 20, y_offset))
        y_offset += (
            settings["Height"] // 32
        )  # Move location of each item by 1/32th of the screen (size of each item)
    screen.blit(settings_surface, (0, -scroll))
    pygame.display.flip()

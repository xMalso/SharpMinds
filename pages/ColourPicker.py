inverted = False

def displayPage(pygame, settings, font, screen, button, options, height, scroll):
    global inverted
    buffer_width = font.size(" ")[0] * 0.6 + font.size("▼ ")[0] - font.size("▶ ")[0]
    y = button.y
    x = button.x
    # space_width = font.size(" ")[0]
    # arrow_width = font.size("▼ ")[0]
    # width = options["Largest"] + space_width + arrow_width
    width = button.width
    height = button.height
    offset = -scroll
    if y - scroll > settings["Height"] // 2:
        inverted = True
    for index, option in enumerate(options["Options"]):
        dropdown_rect = pygame.Rect(
            (x, y + offset, width, height),
        )
        update_button({"Name": option, "Pygame Button": dropdown_rect})
        if len(options["Options"]) == 1:
            pygame.draw.rect(
                screen,
                settings["Dropdown Background"],
                dropdown_rect,
                border_radius=25,
            )
        elif (index == 0 and not inverted) or (
            inverted and index == len(options["Options"]) - 1
        ):
            pygame.draw.rect(
                screen,
                settings["Dropdown Background"],
                dropdown_rect,
                border_top_left_radius=25,
                border_top_right_radius=25,
            )
        elif (index == len(options["Options"]) - 1 and not inverted) or (
            inverted and index == 0
        ):
            pygame.draw.rect(
                screen,
                settings["Dropdown Background"],
                dropdown_rect,
                border_bottom_left_radius=25,
                border_bottom_right_radius=25,
            )
        else:
            pygame.draw.rect(
                screen,
                settings["Dropdown Background"],
                dropdown_rect,
            )
        offset += increment
    for button in options_buttons.values():
        text_surface = font.render(
            f"▶ {button["Name"]}",
            settings["Antialiasing Text"],
            settings["Dropdown Font Colour"],
        )
        screen.blit(
            text_surface,
            (button["Pygame Button"].x + buffer_width, button["Pygame Button"].y),
        )
    global xy_range
    xy_range = {"y": [y, y + offset], "x": [x, x + width]}

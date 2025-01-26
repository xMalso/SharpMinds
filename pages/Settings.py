global options_buttons

# try:
#     print(options_buttons)
#     print("success")
# except:
#     print("fail")
options_buttons = {}


def update_button(new_button):
    button_name = new_button["Name"]
    options_buttons[button_name] = new_button


def pasteButton(button, pygame, settings, screen, settings_surface, scroll):
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
        settings_surface,
        button["Colour"],
        (
            button["Pygame Button"].x,
            button["Pygame Button"].y + scroll,
            button["Pygame Button"].width,
            button["Pygame Button"].height,
        ),
        border_radius=25,
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


def displayPage(
    settings,
    screen,
    font,
    pygame,
    scroll,
    content_height,
    buttons,
    options,
    choice,
    changed,
):
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
    text_height = font.size("Save and Leave")[1]
    y_offset = text_height * 3 + (settings["Height"] // 50)

    for key in settings.keys():
        # text_surface = font.render(
        #     f"{key}: {value}", settings["Antialiasing Text"], (255, 255, 255)
        # )
        # Check if the text is meant to be visible
        text_width, text_height = font.size(str(choice[key]))  # {key}: ▼
        buffer_width = font.size(f"{key}: ▼ ")[0]
        if not (
            y_offset
            > scroll
            - text_height
            + (settings["Height"] * 29) // 32  # Check if below screen
            or y_offset
            < scroll
            + text_height * 3
            + settings["Height"] // 50  # Check if above scren
        ):
            if key in options:
                # Render a dropdown menu for selectable options
                dropdown_rect = pygame.Rect(
                    buffer_width + settings["Width"] // 50,
                    y_offset,
                    text_width + settings["Width"] // 25,
                    text_height,
                )
                pygame.draw.rect(
                    settings_surface, settings["Dropdown Background"], dropdown_rect
                )
                dropdown_surface = font.render(
                    f"{key}: ▼ {choice[key]}",
                    settings["Antialiasing Text"],
                    settings["Dropdown Font Colour"],
                )
                settings_surface.blit(
                    dropdown_surface, (settings["Width"] // 20, y_offset)
                )
                update_button(
                    {"Pygame Button": dropdown_rect, "Name": key, "Type": "Dropdown"},
                )
            else:
                text_surface = font.render(
                    f"{key}: {choice[key]}",
                    settings["Antialiasing Text"],
                    settings["Background Font Colour"],
                )
                #     # Render a colour picker for RGB tuples

                settings_surface.blit(text_surface, (settings["Width"] // 20, y_offset))
                colour_box_rect = pygame.Rect(
                    settings["Width"] // 20 + text_surface.get_width() - text_width,
                    y_offset,
                    text_width,
                    text_height,
                )
                pygame.draw.rect(
                    settings_surface,
                    choice[key],
                    (colour_box_rect),
                )
                update_button(
                    {
                        "Pygame Button": colour_box_rect,
                        "Name": key,
                        "Type": "Colour Picker",
                    },
                )
        #     pygame.draw.rect(
        #         settings_surface,
        #         (255, 255, 255),
        #         (input_x, y_offset, colour_box_size, colour_box_size),
        #         2,
        #     )

        y_offset += text_height + settings["Height"] // 200
    buttons, back = buttons[:-1], buttons[-1]
    if changed:
        for button in buttons:
            pasteButton(button, pygame, settings, screen, settings_surface, scroll)
    pasteButton(back, pygame, settings, screen, settings_surface, scroll)
    screen.blit(settings_surface, (0, -scroll))

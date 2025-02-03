import os
global options_buttons

# try:
#     print(options_buttons)
#     print("success")
# except:
#     print("fail")
options_buttons = {}

def getOptionsButtons():
    return options_buttons

confirmation_text = {
    "Main Menu": "discard and go to main menu",
    "Discard": "discard changes",
    "Default": "return to default settings",
}


def update_button(new_button):
    button_name = new_button["Name"]
    options_buttons[button_name] = new_button


def pasteButton(button, pygame, settings, screen):
    global small_font
    if settings["Font Type"] == "System":
        small_font = pygame.font.SysFont(
            settings["Font"], (settings["Font Size"] // 2),
        )
    else:
        small_font = pygame.font.Font(
            os.path.join(r"assets/fonts/fonts", settings["Font"]), (settings["Font Size"] // 2),
        )
    pygame.draw.rect(
        screen,
        (button["Colour"]),
        (
            button["Pygame Button"].x,
            button["Pygame Button"].y,
            button["Pygame Button"].width,
            button["Pygame Button"].height,
        ),
        border_radius=25,
    )
    button_text = small_font.render(
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
    confirmation,
    confirmation_buttons,
):
    settings_surface = pygame.Surface((settings["Width"], content_height))
    settings_surface.fill(settings["Background Colour"])
    if settings["Font Type"] == "System":
        title_font = pygame.font.SysFont(
            settings["Font"],
            settings["Font Size"] * 3,
            bold=True,
        )
    else:
        title_font = pygame.font.Font(
            os.path.join(r"assets/fonts/fonts", settings["Bold Font"]),
            settings["Font Size"] * 3,
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
    text_size = font.size("Save and Leave")
    y_offset = text_size[1] * 3 + (settings["Height"] // 50)
    space_width = font.size(" ")[0]
    arrow_width = font.size("▼ ")[0]
    for key in choice.keys():
        # text_surface = font.render(
        #     f"{key}: {value}", settings["Antialiasing Text"], (255, 255, 255)
        # )
        # Check if the text is meant to be visible
        text_width = font.size(str(choice[key]))[0]
        key_width = font.size(f"{key}:")[0]
        if not (
            y_offset
            > scroll
            - text_size[1]
            + (settings["Height"] * 29) // 32  # Check if below screen
            or y_offset
            < scroll
            + text_size[1] * 3
            + settings["Height"] // 50  # Check if above scren
        ):
            if key == "Background Colour":
                text_surface = font.render(
                    f"{key}: ",
                    settings["Antialiasing Text"],
                    settings["Background Font Colour"],
                )
                #     # Render a colour picker for RGB tuples

                settings_surface.blit(text_surface, (settings["Width"] // 20, y_offset))
                colour_box_rect = pygame.Rect(
                    settings["Width"] // 20 + text_surface.get_width() - 20,
                    y_offset,
                    text_width + 50,
                    text_size[1],
                )
                pygame.draw.rect(
                    settings_surface, choice["Background Font Colour"], (colour_box_rect), border_radius=25
                )
                pygame.draw.rect(
                    settings_surface, choice[key], (colour_box_rect.x+1, colour_box_rect.y+1, colour_box_rect.width -2, colour_box_rect.height-2), border_radius=25
                )
                update_button(
                    {
                        "Pygame Button": colour_box_rect,
                        "Name": key,
                        "Type": "Colour Picker",
                    },
                )
            elif key in options:
                # Render a dropdown menu for selectable options
                dropdown_rect = pygame.Rect(
                    space_width * 0.4 + key_width + settings["Width"] // 20,
                    y_offset,
                    text_width + space_width + arrow_width,
                    text_size[1],
                )
                pygame.draw.rect(
                    settings_surface,
                    settings["Dropdown Background Colour"],
                    dropdown_rect,
                    border_radius=25,
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
            # elif "Game" in key:
            else:
                text_surface = font.render(
                    f"{key}: ",
                    settings["Antialiasing Text"],
                    settings["Background Font Colour"],
                )
                #     # Render a colour picker for RGB tuples

                settings_surface.blit(text_surface, (settings["Width"] // 20, y_offset))
                colour_box_rect = pygame.Rect(
                    settings["Width"] // 20 + text_surface.get_width() - 20,
                    y_offset,
                    text_width + 50,
                    text_size[1],
                )
                pygame.draw.rect(
                    settings_surface, choice[key], (colour_box_rect), border_radius=25
                )
                update_button(
                    {
                        "Pygame Button": colour_box_rect,
                        "Name": key,
                        "Type": "Colour Picker",
                    },
                )
            # elif "Font" in key:
            #     text_surface = font.render(
            #         f"{key}: ",
            #         settings["Antialiasing Text"],
            #         settings["Background Font Colour"],
            #     )
            #     #     # Render a colour picker for RGB tuples

            #     settings_surface.blit(text_surface, (settings["Width"] // 20, y_offset))
            #     colour_box_rect = pygame.Rect(
            #         settings["Width"] // 20 + text_surface.get_width() - 20,
            #         y_offset,
            #         text_width + 50,
            #         text_size[1],
            #     )
            #     pygame.draw.rect(
            #         settings_surface, choice[background], (colour_box_rect), border_radius=25
            #     )
            #     update_button(
            #         {
            #             "Pygame Button": colour_box_rect,
            #             "Name": key,
            #             "Type": "Colour Picker",
            #         },
            #     )
            # else:
            #     background = key
        #     pygame.draw.rect(
        #         settings_surface,
        #         (255, 255, 255),
        #         (input_x, y_offset, colour_box_size, colour_box_size),
        #         2,
        #     )

        y_offset += text_size[1] + settings["Height"] // 200
    screen.blit(settings_surface, (0, -scroll))
    buttons, last2 = buttons[:-2], buttons[-2:]
    if any(choice.get(k) != settings[k] for k in settings if k != "Font Type" and k != "Adaptive Difficulty"):
        for button in buttons:
            pasteButton(button, pygame, settings, screen)
    for button in last2:
        pasteButton(button, pygame, settings, screen)
    if confirmation != None:
        confirmation_surface = pygame.Surface(
            (settings["Width"] // 3, settings["Height"] // 8), pygame.SRCALPHA
        )
        confirmation_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(
            confirmation_surface,
            settings["Button Quaternary Colour"],
            confirmation_surface.get_rect(),
            border_radius=25,
        )
        text_surface = small_font.render(
            f"Are you sure you want to {confirmation_text[confirmation]}?",
            settings["Antialiasing Text"],
            settings["Font Quaternary Colour"],
        )
        confirmation_surface.blit(
            text_surface,
            (
                settings["Width"] // 6 - text_surface.get_width() // 2,
                settings["Height"] // 64,
            ),
        )
        screen.blit(
            confirmation_surface,
            (settings["Width"] * 2 // 6, settings["Height"] * 7 // 16),
        )
        for button in confirmation_buttons:
            pasteButton(
                button,
                pygame,
                settings,
                screen,
            )

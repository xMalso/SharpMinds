global colour_buttons
colour_buttons = {}

def getColourButtons():
    return colour_buttons

def resetColourButtons():
    global colour_buttons
    colour_buttons = {}

def update_button(new_button):
    button_name = new_button["Name"]
    colour_buttons[button_name] = new_button

def displayPage(pygame, settings, font, screen, button, options, scroll, input_text):
    global inverted
    y = button["Pygame Button"].y
    x = button["Pygame Button"].x
    width = button["Pygame Button"].width
    for option in options[1:]:
        temp = pygame.Rect(
            x + width + option["Buffer Size"][0],
            y - option["Buffer Size"][1] - scroll,
            option["Size"][0],
            option["Size"][1],
        )
        update_button({"Name": option["Name"], "Pygame Button": temp})
        pygame.draw.rect(screen, option["Colour"], temp, border_radius=25)
        text_surface = font.render(
            f"{option["Text"]}",
            settings["Antialiasing Text"],
            option["Font Colour"],
        )
        screen.blit(
            text_surface,
            (
                temp.x + (temp.width - text_surface.get_width()) // 2,
                temp.y + (temp.height - text_surface.get_height()) // 2,
            ),
        )
    temp = pygame.Rect(
        x + width + options[0]["Buffer Size"][0],
        y - options[0]["Buffer Size"][1] - scroll,
        options[0]["Size"][0],
        options[0]["Size"][1],
    )
    update_button({"Name": options[0]["Name"], "Pygame Button": temp})
    pygame.draw.rect(screen, options[0]["Colour"], temp, border_radius=25)
    # if input_text == None:
    #     input_text = "#{:02X}{:02X}{:02X}".format(*settings[button["Name"]])
    # else:
    #     input_text = "#" + str(input_text)
    text_surface = font.render(
        input_text, settings["Antialiasing Text"], options[0]["Font Colour"]
    )
    screen.blit(
        text_surface,
        (
            temp.x + (temp.width - text_surface.get_width()) // 2,
            temp.y + (temp.height - text_surface.get_height()) // 2,
        ),
    )

    # buffer_width = font.size(" ")[0] * 0.6 + font.size("▼ ")[0] - font.size("▶ ")[0]
    # space_width = font.size(" ")[0]
    # arrow_width = font.size("▼ ")[0]
    # width = options["Largest"] + space_width + arrow_width
    # for index, option in enumerate(options["Options"]):
    #     dropdown_rect = pygame.Rect(
    #         (x, y + offset, width, height),
    #     )
    #     update_button({"Name": option, "Pygame Button": dropdown_rect})
    #     if len(options["Options"]) == 1:
    #         pygame.draw.rect(
    #             screen,
    #             settings["Dropdown Background Colour"],
    #             dropdown_rect,
    #             border_radius=25,
    #         )
    #     elif (index == 0 and not inverted) or (
    #         inverted and index == len(options["Options"]) - 1
    #     ):
    #         pygame.draw.rect(
    #             screen,
    #             settings["Dropdown Background Colour"],
    #             dropdown_rect,
    #             border_top_left_radius=25,
    #             border_top_right_radius=25,
    #         )
    #     elif (index == len(options["Options"]) - 1 and not inverted) or (
    #         inverted and index == 0
    #     ):
    #         pygame.draw.rect(
    #             screen,
    #             settings["Dropdown Background Colour"],
    #             dropdown_rect,
    #             border_bottom_left_radius=25,
    #             border_bottom_right_radius=25,
    #         )
    #     else:
    #         pygame.draw.rect(
    #             screen,
    #             settings["Dropdown Background Colour"],
    #             dropdown_rect,
    #         )
    #     offset += increment

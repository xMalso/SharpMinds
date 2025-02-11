global colour_buttons, selected
selected = False
colour_buttons = {}

def getColourButtons():
    return colour_buttons


def resetColourButtons():
    global colour_buttons
    colour_buttons = {}


def updateButton(new_button):
    button_name = new_button["Name"]
    colour_buttons[button_name] = new_button


def selectInput(selection):
    global selected
    selected = selection


def displayPage(pygame, settings, font, screen, button, colour_picker_buttons, scroll, input_text):
    y = button["Pygame Button"].y
    x = button["Pygame Button"].x
    width = button["Pygame Button"].width
    for option in colour_picker_buttons[2:]:
        temp = pygame.Rect(
            x + width + option["Buffer Size"][0],
            y - option["Buffer Size"][1] - scroll,
            option["Size"][0],
            option["Size"][1],
        )
        updateButton({"Name": option["Name"], "Pygame Button": temp})
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
    global selected
    if selected:
        button = colour_picker_buttons[1]
    else:
        button = colour_picker_buttons[0]
    temp = pygame.Rect(
        x + width + button["Buffer Size"][0],
        y - button["Buffer Size"][1] - scroll,
        button["Size"][0],
        button["Size"][1],
    )
    updateButton({"Name": button["Name"], "Pygame Button": temp})
    pygame.draw.rect(screen, button["Colour"], temp, border_radius=25)
    text_surface = font.render(
        input_text, settings["Antialiasing Text"], button["Font Colour"]
    )
    screen.blit(
        text_surface,
        (
            temp.x + (temp.width - text_surface.get_width()) // 2,
            temp.y + (temp.height - text_surface.get_height()) // 2,
        ),
    )

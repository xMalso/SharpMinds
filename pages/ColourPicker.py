global colour_buttons, pygame
import pygame

colour_buttons = {}


def getColourButtons():
    return colour_buttons


def resetColourButtons():
    global colour_buttons
    colour_buttons = {}


def updateButton(new_button):
    button_name = new_button["Name"]
    colour_buttons[button_name] = new_button


def displayPage(
    settings, font, screen, button, colour_picker_buttons, scroll, input_text
):
    y = button["Pygame Button"].y
    x = button["Pygame Button"].x
    width = button["Pygame Button"].width
    for option in colour_picker_buttons:
        temp = pygame.Rect(
            x + width + option["Buffer Size"][0],
            y - option["Buffer Size"][1] - scroll,
            option["Size"][0],
            option["Size"][1],
        )
        updateButton({"Name": option["Name"], "Pygame Button": temp})
        pygame.draw.rect(
            screen, option["Colour"], temp, border_radius=settings["Width"] // 40
        )
        if option["Name"] == "Input":
            text = f"#{input_text}"
        else:
            text = option["Text"]
        text_surface = font.render(
            text,
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
    screen.blit(
        text_surface,
        (
            temp.x + (temp.width - text_surface.get_width()) // 2,
            temp.y + (temp.height - text_surface.get_height()) // 2,
        ),
    )

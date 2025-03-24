global colour_buttons
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
        updateButton({"Name": option["Meta"], "Pygame Button": temp, "Meta": option["Meta"]})
        pygame.draw.rect(
            screen, option["Colour"], temp, border_radius=settings["Width"] // 40
        )
        if option["Meta"] == "Input":
            text = font.render(
            f"#{input_text}",
            settings["Antialiasing Text"],
            settings["Input Font Colour"],)
        else:
            text = option["Text"]
        screen.blit(
            text,
            (
                temp.centerx - text.get_width() // 2,
                temp.centery - text.get_height() // 2,
            ),
        )
    # screen.blit(
    #     text,
    #     (
    #         temp.centerx - text.get_width() // 2,
    #         temp.centery - text.get_height() // 2,
    #     ),
    # )

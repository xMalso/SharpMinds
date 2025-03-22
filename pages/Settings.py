from .Dropdown import (
    displayPage as dropdownDisplay,
    resetDropdownButtons,
    getDropdownButtons,
)
from .ColourPicker import (
    displayPage as colourPickerDisplay,
    resetColourButtons,
    getColourButtons,
)

global os, pygame, current_colour_picker, current_dropdown, options_buttons, backspace_held
import os, pygame

current_colour_picker = None
current_dropdown = None
options_buttons = {}
confirmation_text = {
    "Main Menu": "discard and go to main menu",
    "Discard": "discard changes",
    "Default": "return to default settings",
}
backspace_held = False


def init(settings, font, small_font):
    makeColourPickerButtons(settings, font)
    makeOptions(settings, font)
    makeConfirmationButtons(settings, small_font)
    makeButtons(settings, small_font)


def splitText(font, max_width, words):
    words = words.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        text_width = font.size(test_line)[0]

        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return lines


def makeColourPickerButtons(settings, font):
    global colour_picker_buttons
    widest_char_width = max(font.size(str(char))[0] for char in "0123456789ABCDEF")
    text_size = (
        widest_char_width * 6 + font.size("#")[0] + settings["Width"] // 32,
        font.size("#")[1] + settings["Height"] // 100 - 1,
    )
    colour_picker_buttons = [
        {
            "Name": "Input",
            "Size": text_size,
            "Buffer Size": (
                settings["Width"] // 100,
                (settings["Height"] * 3) // 128 + text_size[1] * 2,
            ),
            "Colour": settings["Input Background Colour"],
            "Font Colour": settings["Input Font Colour"],
        },
        {
            "Name": "Confirm",
            "Size": text_size,
            "Buffer Size": (
                settings["Width"] // 100,
                settings["Height"] // 64 + text_size[1],
            ),
            "Text": "Confirm",
            "Colour": settings["Button Primary Colour"],
            "Font Colour": settings["Font Primary Colour"],
        },
        {
            "Name": "Discard",
            "Size": text_size,
            "Buffer Size": (settings["Width"] // 100, settings["Height"] // 128),
            "Text": "Discard",
            "Colour": settings["Button Quinary Colour"],
            "Font Colour": settings["Font Quinary Colour"],
        },
    ]


def makeOptions(settings, font):
    global options
    options = {
        "Width": {"Options": [3840, 2560, 1920, 1600, 1536, 1440, 1366, 1280, 1024]},
        "Height": {"Options": [2160, 1440, 1080, 900, 768, 720]},
        "Window Type": {"Options": ["Borderless", "Fullscreen", "Windowed"]},
        "Show FPS": {"Options": [True, False]},
        "FPS Limit": {"Options": [0, 30, 60, 120, 144, 165, 240]},
        "Font": {
            "Options": [
                "arial",
                "verdana",
                "timesnewroman",
                "couriernew",
                "comicsansms",
                "georgia",
                "trebuchetms",
                "lucidaconsole",
                "tahoma",
                "impact",
            ]
        },
        "Bold Font": {"Options": []},
        "Italic Font": {"Options": []},
        "BoldItalic Font": {"Options": []},
        "Font Size": {"Options": [48, 56, 64, 72, 80, 128, 160]},
        "Antialiasing Text": {"Options": [True, False]},
    }
    dir = r"assets/fonts/fonts"
    if os.path.exists(dir):
        for file in os.listdir(dir):
            if file.endswith((".ttf", ".otf")):
                if "Bold" in file and "Italic" in file:
                    options["BoldItalic Font"]["Options"].append(file)
                elif "Italic" in file:
                    options["Italic Font"]["Options"].append(file)
                elif "Bold" in file:
                    options["Bold Font"]["Options"].append(file)
                else:
                    options["Font"]["Options"].append(file)
    else:
        print(f"Directory, {dir}, does not exist")

    for index, choice in enumerate(options["Font Size"]["Options"]):
        options["Font Size"]["Options"][index] = settings["Width"] // choice
    for option in options.values():
        largest = max(font.size(str(choice))[0] for choice in option["Options"])
        option["Largest"] = largest


def makeConfirmationButtons(settings, small_font):
    global confirmation_buttons
    text_size = small_font.size("Confirm")
    confirmation_buttons = [
        {
            "Pygame Button": pygame.Rect(
                settings["Width"] * 28 // 60 - text_size[0],
                settings["Height"] // 2 - text_size[1],
                text_size[0] + settings["Width"] // 96,
                text_size[1] + settings["Height"] // 100,
            ),
            "Name": "Confirm",
            "Colour": settings["Button Quinary Colour"],
            "Font Colour": settings["Font Quinary Colour"],
        },
        {
            "Pygame Button": pygame.Rect(
                settings["Width"] * 32 // 60,
                settings["Height"] // 2 - text_size[1],
                text_size[0] + settings["Width"] // 96,
                text_size[1] + settings["Height"] // 100,
            ),
            "Name": "Decline",
            "Colour": settings["Button Primary Colour"],
            "Font Colour": settings["Font Primary Colour"],
        },
    ]


def makeButtons(settings, small_font):
    global buttons, last
    text_width, text_height = small_font.size("Save and Leave")
    buttons = [
        # Save and Leave
        {
            "Name": "Save and Leave",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 100) // 128 - (text_width * 5),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Primary Colour"],
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Save and Leave",
        },
        # Save
        {
            "Name": "Save",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 105) // 128 - (text_width * 4),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Font Colour": settings["Font Secondary Colour"],
            "Meta": "Save",
        },
        # Discard
        {
            "Name": "Discard",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 110) // 128 - (text_width * 3),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Quinary Colour"],
            "Font Colour": settings["Font Quinary Colour"],
            "Meta": "Discard",
        },
    ]
    last = [
        # Default
        {
            "Name": "Default",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 115) // 128 - (text_width * 2),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Quaternary Colour"],
            "Font Colour": settings["Font Quaternary Colour"],
            "Meta": "Default",
        },
        # Main Menu
        {
            "Name": "Main Menu",
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 120) // 128 - text_width,
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Tertiary Colour"],
            "Font Colour": settings["Font Tertiary Colour"],
            "Meta": "Main Menu",
        },
    ]


def checkCollide(loc):
    global current_dropdown, current_colour_picker, input_text, input_selected, choice, backspace_held
    colour_buttons = getColourButtons()
    dropdown_buttons = getDropdownButtons()
    if current_dropdown != None:
        for button in dropdown_buttons.values():
            if button["Pygame Button"].collidepoint(loc):
                choice[current_dropdown["Name"]] = button["Name"]
        current_dropdown = None
        resetDropdownButtons()
    else:
        for button in colour_buttons.values():
            if button["Pygame Button"].collidepoint(loc):
                if button["Name"] == "Confirm":
                    input_text = input_text.ljust(6, "0")
                    hex = tuple(int(input_text[i : i + 2], 16) for i in (0, 2, 4))
                    choice[current_colour_picker["Name"]] = hex
                    current_colour_picker = None
                    input_text = ""
                    input_selected = False
                    backspace_held = False
                    resetColourButtons()
                    return
                elif button["Name"] == "Discard":
                    current_colour_picker = None
                    input_text = ""
                    input_selected = False
                    backspace_held = False
                    resetColourButtons()
                    return
                elif button["Name"] == "Input":
                    input_selected = True
                    return
                else:
                    print("Unknown colour picker button.")
        current_colour_picker = None
        input_text = ""
        input_selected = False
        backspace_held = False
        resetColourButtons()


def updateButton(new_button):
    global options_buttons
    button_name = new_button["Name"]
    options_buttons[button_name] = new_button


def pasteButton(button, settings, screen):
    global small_font
    pygame.draw.rect(
        screen,
        button["Colour"],
        button["Pygame Button"],
        border_radius=settings["Width"] // 40,
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


def displayPage(settings, screen, font, title_font, small_fonts, choices, getFps, exit):
    global current_dropdown, current_colour_picker, input_selected, choice, input_text, small_font, backspace_held
    never = True
    small_font = small_fonts
    font_height = font.size("Save and Leave")[1]
    content_height = (
        len(settings)
        + int(
            (int((settings["Height"] * ((3 / 32) + 0.02))) + font_height * 4)
            / (font_height + settings["Height"] // 200)
        )
    ) * (font_height + settings["Height"] // 200) + (
        settings["Height"] % (font_height + settings["Height"] // 200)
    )
    confirmation = None
    scroll = 0
    choice = choices.copy()
    input_selected = False
    title_text = title_font.render(
        "Settings", settings["Antialiasing Text"], settings["Font Primary Colour"]
    )
    text_size = font.size("Save and Leave")
    space_width = font.size(" ")[0]
    arrow_width = font.size("▼ ")[0]
    settings_surface = pygame.Surface((settings["Width"], content_height))
    while True:
        settings_surface.fill(settings["Background Colour"])
        settings_surface.blit(
            title_text,
            (
                settings["Width"] // 2 - title_text.get_width() // 2,
                (settings["Height"]) // 100 + scroll,
            ),
        )
        y_offset = text_size[1] * 3 + (settings["Height"] // 50)
        for key in choice.keys():
            text_width = font.size(str(choice[key]))[0]
            key_width = font.size(f"{key}:")[0]
            if not (
                y_offset > scroll - text_size[1] + (settings["Height"] * 29) // 32
                or y_offset < scroll + text_size[1] * 3 + settings["Height"] // 50
            ):
                if key == "Background Colour":
                    text_surface = font.render(
                        f"{key}: ",
                        settings["Antialiasing Text"],
                        settings["Background Font Colour"],
                    )

                    settings_surface.blit(
                        text_surface, (settings["Width"] // 20, y_offset)
                    )
                    colour_box_rect = pygame.Rect(
                        settings["Width"] // 20 + text_surface.get_width() - 20,
                        y_offset,
                        text_width + 50,
                        text_size[1],
                    )
                    pygame.draw.rect(
                        settings_surface,
                        choice["Background Font Colour"],
                        (colour_box_rect),
                        border_radius=settings["Width"] // 40,
                    )
                    pygame.draw.rect(
                        settings_surface,
                        choice[key],
                        (
                            colour_box_rect.x + 1,
                            colour_box_rect.y + 1,
                            colour_box_rect.width - 2,
                            colour_box_rect.height - 2,
                        ),
                        border_radius=settings["Width"] // 40,
                    )
                    updateButton(
                        {
                            "Pygame Button": colour_box_rect,
                            "Name": key,
                            "Type": "Colour Picker",
                        },
                    )
                elif key in options:
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
                        border_radius=settings["Width"] // 40,
                    )
                    dropdown_surface = font.render(
                        f"{key}: ▼ {choice[key]}",
                        settings["Antialiasing Text"],
                        settings["Dropdown Font Colour"],
                    )
                    settings_surface.blit(
                        dropdown_surface, (settings["Width"] // 20, y_offset)
                    )
                    updateButton(
                        {
                            "Pygame Button": dropdown_rect,
                            "Name": key,
                            "Type": "Dropdown",
                        },
                    )
                else:
                    text_surface = font.render(
                        f"{key}: ",
                        settings["Antialiasing Text"],
                        settings["Background Font Colour"],
                    )
                    settings_surface.blit(
                        text_surface, (settings["Width"] // 20, y_offset)
                    )
                    colour_box_rect = pygame.Rect(
                        settings["Width"] // 20 + text_surface.get_width() - 20,
                        y_offset,
                        text_width + 50,
                        text_size[1],
                    )
                    pygame.draw.rect(
                        settings_surface,
                        choice[key],
                        (colour_box_rect),
                        border_radius=settings["Width"] // 40,
                    )
                    updateButton(
                        {
                            "Pygame Button": colour_box_rect,
                            "Name": key,
                            "Type": "Colour Picker",
                        },
                    )
            y_offset += text_size[1] + settings["Height"] // 200
        screen.blit(settings_surface, (0, -scroll))
        if any(
            choice.get(k) != settings[k]
            for k in settings
            if k != "Font Type" and k != "Adaptive Difficulty"
        ):
            for button in buttons:
                pasteButton(button, settings, screen)
        for button in last:
            pasteButton(button, settings, screen)
        if confirmation != None:
            printed_text = splitText(
                font,
                settings["Width"] // 3.1,
                f"Are you sure you want to {confirmation_text[confirmation]}?",
            )
            small_text = small_font.size(printed_text[0])[1]
            buffer_height = small_text * (len(printed_text) - 1)
            confirmation_surface = pygame.Surface(
                (
                    settings["Width"] // 3,
                    settings["Height"] // 12 + buffer_height,
                ),
                pygame.SRCALPHA,
            )
            pygame.draw.rect(
                confirmation_surface,
                settings["Button Quaternary Colour"],
                confirmation_surface.get_rect(),
                border_radius=settings["Width"] // 40,
            )
            height = small_text * (len(printed_text)) + settings["Height"] // 100
            for line in printed_text[::-1]:
                text_surface = small_font.render(
                    line,
                    settings["Antialiasing Text"],
                    settings["Font Quaternary Colour"],
                )
                height -= text_surface.get_height()
                confirmation_surface.blit(
                    text_surface,
                    (
                        settings["Width"] // 6 - text_surface.get_width() // 2,
                        height,
                    ),
                )
            screen.blit(
                confirmation_surface,
                (
                    settings["Width"] * 2 // 6,
                    settings["Height"] * 7 // 16 - buffer_height,
                ),
            )
            for button in confirmation_buttons:
                pasteButton(button, settings, screen)
        if current_dropdown != None:
            dropdownDisplay(
                settings,
                font,
                screen,
                current_dropdown["Pygame Button"],
                options[current_dropdown["Name"]],
                scroll,
            )
        if current_colour_picker != None:
            colourPickerDisplay(
                settings,
                font,
                screen,
                current_colour_picker,
                colour_picker_buttons,
                scroll,
                input_text,
            )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEWHEEL:
                scroll = max(
                    0,
                    min(
                        content_height - settings["Height"],
                        scroll - event.y * (font_height + settings["Height"] // 200),
                    ),
                )
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not (current_dropdown == None and current_colour_picker == None):
                    checkCollide(event.pos)
                elif confirmation == None:
                    for button in options_buttons.values():  # Check for each button
                        if button["Pygame Button"].collidepoint(
                            (event.pos[0], event.pos[1] + scroll)
                        ):
                            if button["Type"] == "Dropdown":
                                current_dropdown = button
                            elif button["Type"] == "Colour Picker":
                                current_colour_picker = button
                                input_selected = True
                                input_text = "{:02X}{:02X}{:02X}".format(
                                    *choice[current_colour_picker["Name"]]
                                )
                if confirmation != None:
                    for button in confirmation_buttons:
                        if button["Pygame Button"].collidepoint(event.pos):
                            if button["Name"] == "Confirm":
                                if confirmation == "Default":
                                    return None, "Default"
                                elif confirmation == "Discard":
                                    choice = settings.copy()
                                    del choice["Font Type"]
                                    del choice["Adaptive Difficulty"]
                                    print("Settings discarded.")
                                elif confirmation == "Main Menu":
                                    return None, "Main Menu"
                                else:
                                    print(
                                        f"Error: Unknown request. {confirmation}, {button["Name"]}"
                                    )
                                confirmation = None
                            elif button["Name"] == "Decline":
                                confirmation = None
                            else:
                                print(f"Error: Unknown confirmation button. {button}")
                for button in buttons + last:  # Check for each button
                    if button["Pygame Button"].collidepoint(event.pos):
                        if any(
                            choice.get(k) != settings[k]
                            for k in settings
                            if k != "Font Type" and k != "Adaptive Difficulty"
                        ):
                            if button["Meta"] == "Save":
                                return choice, "Save"
                            elif button["Meta"] == "Save and Leave":
                                return choice, "Save and Leave"
                            elif button["Meta"] == "Discard":
                                if confirmation == None:
                                    confirmation = "Discard"
                        if button["Meta"] == "Default":
                            if confirmation == None:
                                confirmation = "Default"
                        elif button["Meta"] == "Main Menu":
                            if (
                                any(
                                    choice.get(k) != settings[k]
                                    for k in settings
                                    if k != "Font Type" and k != "Adaptive Difficulty"
                                )
                                and confirmation == None
                            ):
                                confirmation = "Main Menu"
                            elif confirmation == None:
                                return None, "Main Menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if (
                        any(
                            choice.get(k) != settings[k]
                            for k in settings
                            if k != "Font Type" and k != "Adaptive Difficulty"
                        )
                        and confirmation == None
                    ):
                        confirmation = "Main Menu"
                    elif confirmation == None:
                        return None, "Main Menu"
                elif input_selected:
                    if event.key == pygame.K_BACKSPACE:
                        backspace_held = True
                        time_held = pygame.time.get_ticks() + 250
                        input_text = input_text[:-1]
                    elif event.unicode.upper() in "0123456789ABCDEF":
                        if len(input_text) != 6:
                            input_text += event.unicode.upper()
            elif input_selected and event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    backspace_held = False
        if backspace_held:
            current = pygame.time.get_ticks()
            if current - time_held > 60:
                time_held = current
                input_text = input_text[:-1]
        getFps(never)
        never = False
        pygame.display.flip()

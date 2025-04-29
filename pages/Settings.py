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

global current_colour_picker, current_dropdown, options_buttons, backspace_held
import os, pygame, logging
from datetime import datetime

logging.basicConfig(
    level=logging.WARNING,
    filename = "latestlog.txt",
    filemode='w',
    format="%(filename)s:%(lineno)d | %(asctime)s - %(message)s",
)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

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


def makeColourPickerButtons(settings, font):
    global colour_picker_buttons
    widest_char_width = max(font.size(str(char))[0] for char in "0123456789ABCDEF")
    text_size = (
        widest_char_width * 6 + font.size("#")[0] + settings["Width"] // 32,
        font.size("#")[1] + settings["Height"] // 100 - 1,
    )
    colour_picker_buttons = [
        {
            "Text": font.render(
                "Input", settings["Antialiasing Text"], settings["Input Font Colour"]
            ),
            "Size": text_size,
            "Buffer Size": (
                settings["Width"] // 100,
                (settings["Height"] * 3) // 128 + text_size[1] * 2,
            ),
            "Colour": settings["Input Background Colour"],
            "Meta": "Input",
        },
        {
            "Text": font.render(
                "Confirm",
                settings["Antialiasing Text"],
                settings["Font Primary Colour"],
            ),
            "Size": text_size,
            "Buffer Size": (
                settings["Width"] // 100,
                settings["Height"] // 64 + text_size[1],
            ),
            "Colour": settings["Button Primary Colour"],
            "Meta": "Confirm",
        },
        {
            "Text": font.render(
                "Discard",
                settings["Antialiasing Text"],
                settings["Font Quinary Colour"],
            ),
            "Size": text_size,
            "Buffer Size": (settings["Width"] // 100, settings["Height"] // 128),
            "Colour": settings["Button Quinary Colour"],
            "Meta": "Discard",
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
        logging.critical(f"Directory, {dir}, does not exist")

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
            "Text": small_font.render(
                "Confirm",
                settings["Antialiasing Text"],
                settings["Font Quinary Colour"],
            ),
            "Colour": settings["Button Quinary Colour"],
            "Meta": "Confirm",
        },
        {
            "Pygame Button": pygame.Rect(
                settings["Width"] * 32 // 60,
                settings["Height"] // 2 - text_size[1],
                text_size[0] + settings["Width"] // 96,
                text_size[1] + settings["Height"] // 100,
            ),
            "Text": small_font.render(
                "Decline",
                settings["Antialiasing Text"],
                settings["Font Primary Colour"],
            ),
            "Colour": settings["Button Primary Colour"],
            "Meta": "Decline",
        },
    ]


def makeButtons(settings, small_font):
    global buttons, last
    text_width, text_height = small_font.size("Save and Leave")
    buttons = [
        # Save and Leave
        {
            "Text": small_font.render(
                "Save and Leave",
                settings["Antialiasing Text"],
                settings["Font Primary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 100) // 128 - (text_width * 5),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Primary Colour"],
            "Meta": "Save and Leave",
        },
        # Save
        {
            "Text": small_font.render(
                "Save", settings["Antialiasing Text"], settings["Font Secondary Colour"]
            ),
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 105) // 128 - (text_width * 4),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Meta": "Save",
        },
        # Discard
        {
            "Text": small_font.render(
                "Discard",
                settings["Antialiasing Text"],
                settings["Font Quinary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 110) // 128 - (text_width * 3),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Quinary Colour"],
            "Meta": "Discard",
        },
    ]
    last = [
        # Default
        {
            "Text": small_font.render(
                "Default",
                settings["Antialiasing Text"],
                settings["Font Quaternary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 115) // 128 - (text_width * 2),
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Quaternary Colour"],
            "Meta": "Default",
        },
        # Main Menu
        {
            "Text": small_font.render(
                "Main Menu",
                settings["Antialiasing Text"],
                settings["Font Tertiary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                (settings["Width"] * 120) // 128 - text_width,
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Tertiary Colour"],
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
                if button["Meta"] == "Confirm":
                    input_text = input_text.ljust(6, "0")
                    hex = tuple(int(input_text[i : i + 2], 16) for i in (0, 2, 4))
                    choice[current_colour_picker["Name"]] = hex
                    current_colour_picker = None
                    input_text = ""
                    input_selected = False
                    backspace_held = False
                    resetColourButtons()
                    return
                elif button["Meta"] == "Discard":
                    current_colour_picker = None
                    input_text = ""
                    input_selected = False
                    backspace_held = False
                    resetColourButtons()
                    return
                elif button["Meta"] == "Input":
                    input_selected = True
                    return
                else:
                    logging.error("Unknown colour picker button.")
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
    pygame.draw.rect(
        screen,
        button["Colour"],
        button["Pygame Button"],
        border_radius=settings["Width"] // 40,
    )
    screen.blit(
        button["Text"],
        (
            button["Pygame Button"].centerx - button["Text"].get_width() // 2,
            button["Pygame Button"].centery - button["Text"].get_height() // 2,
        ),
    )


def displayPage(
    settings, screen, font, title_font, small_font, choices, getFps, exitGame, splitText
):
    global current_dropdown, current_colour_picker, input_selected, choice, input_text, backspace_held
    never = True
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
            outputed_text = splitText(
                font,
                settings["Width"] // 3.1,
                settings["Antialiasing Text"],
                settings["Font Quaternary Colour"],
                words=f"Are you sure you want to {confirmation_text[confirmation]}?",
            )
            small_text = outputed_text[0][0].get_height()
            buffer_height = small_text * (len(outputed_text) - 1)
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
            height = buffer_height + small_text + settings["Height"] // 100
            for line in outputed_text[::-1]:
                height -= line.get_height()
                confirmation_surface.blit(
                    line,
                    (
                        settings["Width"] // 6 - line.get_width() // 2,
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
                exitGame()
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
                            if button["Meta"] == "Confirm":
                                if confirmation == "Default":
                                    return None, "Default"
                                elif confirmation == "Discard":
                                    choice = settings.copy()
                                    del choice["Font Type"]
                                    del choice["Adaptive Difficulty"]
                                    logging.info(
                                        f"Settings discarded. {datetime.now()}"
                                    )
                                elif confirmation == "Main Menu":
                                    return None, "Main Menu"
                                else:
                                    logging.error(
                                        f"Error: Unknown request. {confirmation}, {button["Meta"]}"
                                    )
                                confirmation = None
                            elif button["Meta"] == "Decline":
                                confirmation = None
                            else:
                                logging.error(
                                    f"Error: Unknown confirmation button. {button}"
                                )
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

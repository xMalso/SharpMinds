from .Dropdown import (
	displayPage as dropdownDisplay,
	resetDropdownButtons,
	getDropdownButtons,
)
from .ColourPicker import (
	displayPage as colourPickerDisplay,
	resetColourButtons,
	getColourButtons,
	selectInput,
)
from .Data import getColourPickerButtons

global os, current_colour_picker, current_dropdown
current_colour_picker = None
current_dropdown = None
import os

global options_buttons
options_buttons = {}


def checkCollide(loc):
	global current_dropdown, current_colour_picker, input_text, input_selected, choice
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
					input_text = input_text[1:].ljust(6, "0")
					hex = tuple(int(input_text[i : i + 2], 16) for i in (0, 2, 4))
					choice[current_colour_picker["Name"]] = hex
					current_colour_picker = None
					input_text = "#"
					input_selected = False
					selectInput(False)
					resetColourButtons()
					return
				elif button["Name"] == "Discard":
					current_colour_picker = None
					input_text = "#"
					input_selected = False
					selectInput(False)
					resetColourButtons()
					return
				elif button["Name"] == "Input":
					input_selected = not input_selected
					selectInput(input_selected)
					return
				else:
					print("Unknown colour picker button.")
		current_colour_picker = None
		input_text = "#"
		input_selected = False
		selectInput(False)
		resetColourButtons()


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


# def displayPage(
#			 pygame,
#			 sys,
#			 settings,
#			 screen,
#			 font,
#			 content_height,
#			 settings_buttons,
#			 options,
#			 choice,
#			 confirmation,
#			 confirmation_buttons,
#			 getFps,
#		 )
def displayPage(
	pygame,
	sys,
	settings,
	screen,
	font,
	buttons,
	options,
	choices,
	confirmation_buttons,
	getFps,
):
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
	buttons, last2 = buttons[:-2], buttons[-2:]
	scroll = 0
	colour_picker_buttons = getColourPickerButtons(settings, font)
	global current_dropdown, current_colour_picker, input_selected, choice, small_font, input_text
	if settings["Font Type"] == "System":
		small_font = pygame.font.SysFont(
			settings["Font"],
			(settings["Font Size"] // 2),
		)
	else:
		small_font = pygame.font.Font(
			os.path.join(r"assets/fonts/fonts", settings["Font"]),
			(settings["Font Size"] // 2),
		)
	choice = choices.copy()
	input_selected = False
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
	text_size = font.size("Save and Leave")
	space_width = font.size(" ")[0]
	arrow_width = font.size("▼ ")[0]
	settings_surface = pygame.Surface((settings["Width"], content_height))
	while True:
		# screen.fill(settings["Background Colour"])
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
						border_radius=25,
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
						border_radius=25,
					)
					update_button(
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
						border_radius=25,
					)
					update_button(
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
		if current_dropdown != None:
			dropdownDisplay(
				pygame,
				settings,
				font,
				screen,
				current_dropdown["Pygame Button"],
				options[current_dropdown["Name"]],
				scroll,
			)
		if current_colour_picker != None:
			colourPickerDisplay(
				pygame,
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
				pygame.quit()
				sys.exit()
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
								input_text = "#{:02X}{:02X}{:02X}".format(
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
				for button in buttons + last2:  # Check for each button
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
						if len(input_text) > 1:
							input_text = input_text[:-1]
					elif event.unicode.upper() in "0123456789ABCDEF":
						if len(input_text) != 7:
							input_text += event.unicode.upper()
		getFps()
		pygame.display.flip()

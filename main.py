import pygame
import sys
from pages import *

class Settings:
# Default incase it wants to be reset to default
    default_settings = {
        'Width': 1920,
        'Height': 1080,
        'Window Type': "Borderless",
        'Background': (52, 53, 65),
        'Button Primary Colour': (99, 139, 102),
        'Button Secondary Colour': (120, 145, 255),
        'Button Tertiary Colour': (255, 120, 80),
        'Button Quaternary Colour': (140, 140, 140),
        'Button Quinary Colour': (255, 102, 68),
        'Background Font': (217, 217, 217),
        'Font Primary Colour': (217, 217, 217),
        'Font Secondary Colour': (217, 217, 217),
        'Font Tertiary Colour': (217, 217, 217),
        'Font Quaternary Colour': (217, 217, 217),
        'Font Quinary Colour': (217, 217, 217),
        'Font': "Arial",
        'Font Size': 30,
        'Antialiasing Text': True,
        'Game Primary Colour': (168, 213, 186),
        'Game Secondary Colour': (255, 154, 162),
        'Game Tertiary Colour': (255, 243, 176),
    }
    def __init__(self):
        self.settings = self.setSettings()
        self.applySettings()
    def getSettings(self):
        return self.settings
    def resetSettings(self):
        self.settings = self.default_settings.copy()
        return self.settings
    def setSettings(self):
        self.settings = self.default_settings.copy() # To ensure values are all filled and anything not found is replaced with default values
        try:
            with open("./settings.txt", "r") as file:
                for line in file:
                    # Ignore empty lines and comments
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    key, value = line.split(": ", 1)
                    value = value.strip(',')
                    key = key.strip('\'')

                    if key in self.settings:  # Only update if it is a setting that has been defined
                        if ',' in value:
                            self.settings[key] = tuple(map(int, value.strip('()').split(", ")))  # Convert to tuple (mainly for RGB values)
                        elif value.isdigit():  # Check for numbers
                            self.settings[key] = int(value)
                        elif value.lower() == "True" or value.lower() == "False":  # Check for boolean
                            self.settings[key] = value.lower() == "True"
                        else:  # Otherwise must be a string
                            self.settings[key] = value.strip('"')
                    else: print(f"Warning: Unknown setting '{key}' found in settings.txt. Ignoring.")
        except FileNotFoundError:
            print("Error: settings.txt not found. Using default values.")
        except ValueError as e:
            print(f"Error: Incorrect format in settings.txt ({e}). Using default values.")

        return self.settings
    def applySettings(self):
        global screen
        global font
        window_flags = {
            'Fullscreen': pygame.FULLSCREEN,
            'Borderless': pygame.NOFRAME,
            'Windowed': 0
        }
        flags = window_flags.get(self.settings['Window Type'], pygame.NOFRAME) # Sets the window type based on the settings file or defaults to borderless
        font = pygame.font.SysFont(self.settings['Font'], self.settings['Font Size'])
        screen = pygame.display.set_mode((self.settings['Width'], self.settings['Height']), flags)
        pygame.display.flip()

        print(f"Screen set to: {self.settings['Width']}x{self.settings['Height']} in {self.settings['Window Type']} mode.")

pygame.init()
pygame.display.set_caption("Sharp Minds")

screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
screen.fill((52, 53, 65))
default_font = pygame.font.SysFont('Arial', 30)
default_text_surface = default_font.render('Loading Settings...', True, (217, 217, 217))
del default_font
screen.blit(default_text_surface, (0,0))
del default_text_surface
pygame.display.flip()

settingsClass = Settings()
settings = settingsClass.getSettings()
text_surface = font.render('Loading Game...', settings['Antialiasing Text'], settings['Background Font'])
screen.blit(text_surface, (settings['Width']//2 - text_surface.get_width()//2, settings['Height']//2 - text_surface.get_height()//2))
del text_surface
pygame.display.flip()

main_menu_buttons = {
    'Games Menu': {
        'Pygame Button': pygame.Rect(settings['Width']//2 - 200, settings['Height']//2 + 100, 400, 50),
        'Colour': settings['Button Primary Colour'],
        'Font Colour': settings['Font Primary Colour'],
        'Name': "Games Menu",
        'Page': "Game Menu"
    },
    'Leaderboards': {
        'Pygame Button': pygame.Rect(settings['Width']//2 - 200, settings['Height']//2 + 160, 400, 50),
        'Colour': settings['Button Secondary Colour'],
        'Font Colour': settings['Font Secondary Colour'],
        'Name': "Leaderboards and Personal Bests",
        'Page': "Leaderboards"
    },
    'Friends': {
        'Pygame Button': pygame.Rect(settings['Width']//2 - 200, settings['Height']//2 + 220, 400, 50),
        'Colour': settings['Button Tertiary Colour'],
        'Font Colour': settings['Font Tertiary Colour'],
        'Name': "Friends",
        'Page': "Friends"
    },
    'Settings': {
        'Pygame Button': pygame.Rect(settings['Width']//2 - 200, settings['Height']//2 + 280, 400, 50),
        'Colour': settings['Button Quaternary Colour'],
        'Font Colour': settings['Font Quaternary Colour'],
        'Name': "Settings",
        'Page': "Settings"
    },
    'Quit': {
        'Pygame Button': pygame.Rect(settings['Width']//2 - 200, settings['Height']//2 + 340, 400, 50),
        'Colour': settings['Button Quinary Colour'],
        'Font Colour': settings['Font Quinary Colour'],
        'Name': "Quit",
        'Page': "Quit"
    },
}
games_buttons = {}
page = "Main Menu"

while True:
    screen.fill(settings['Background'])
    if page == "Main Menu":
        main_menu_display(settings, screen, font, pygame, main_menu_buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in main_menu_buttons.values():  # Check for each button
                    if button['Pygame Button'].collidepoint(event.pos):  # Check if location of mouse is within the boundaries of the button when mouse is pressed
                        page = button['Page'] # Set page if button is pressed  
                        print(f"Page set to: {page}")
    elif page == "Game Menu":
        # game_menu_display(settings, screen, font, pygame, games_buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for game_name, game in games_buttons.values():  # Check for each button
                    if game['Pygame button'].collidepoint(event.pos):  # Check if location of mouse is within the boundaries of the button when mouse is pressed
                        page = game['Page'] # Set page if button is pressed  
                        print(f"Page set to: {page}")
    pygame.display.flip()
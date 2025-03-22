global pygame
import pygame

def init(settings, font):
    makeButtons(settings, font)

def makeButtons(settings, font):
    global buttons
    # friends?
    # game 1/2/3 (their names)
    # main menu



def displayPage(settings, screen, font, game, getFps, exit, getLB):
    lb = getLB(game)
    never = True
    while True:
        screen.fill(settings["Background Colour"])
        # screen.blit(game_over_text, game_over_text_rect)
        # screen.blit(score_text, score_text_rect)
        # for button in buttons:
            # pygame.draw.rect(
            #     screen,
            #     (button["Colour"]),
            #     button["Pygame Button"],
            #     border_radius=settings["Width"] // 40,
            # )
            # button_text = font.render(
            #     button["Name"], settings["Antialiasing Text"], button["Font Colour"]
            # )
            # screen.blit(
            #     button_text,
            #     (
            #         button["Pygame Button"].x
            #         + button["Pygame Button"].width // 2
            #         - button_text.get_width() // 2,
            #         button["Pygame Button"].y
            #         + button["Pygame Button"].height // 2
            #         - button_text.get_height() // 2,
            #     ),
            # )
        getFps(never)
        never = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button["Pygame Button"].collidepoint(event.pos):
                        return button["Meta"]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Main Menu"
        pygame.display.flip()



def init(settings):
    pass

global pygame
import pygame


def init(settings, font, small_font):
    makeButtons(settings, font, small_font)


def makeButtons(settings, font, small_font):
    global buttons, game_text
    text = small_font.size("Back to Main Menu")
    game_text = font.size(max(["Expose the Criminal", "Memory Experiment", "Pattern Rush"], key=lambda x: font.size(x)[0]))
    buttons = [
        {
            "Text": small_font.render("Back to Main Menu", settings["Antialiasing Text"], settings["Font Quinary Colour"]),
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                settings["Height"] // 16,
                text[0] + settings["Width"] // 64,
                text[1] + settings["Height"] // 90,
            ),
            "Colour": settings["Button Quinary Colour"],
            "Meta": "Main Menu",
        },
        {
            "Text": font.render("Friends",settings["Antialiasing Text"], settings["Font Primary Colour"]),
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                (settings["Height"] * 4) // 16,
                font.size("Friends")[0] + settings["Width"] // 64,
                font.size("Friends")[1] + settings["Height"] // 90,
            ),
            "Colour": settings["Button Primary Colour"],
            "Meta": "Friends",
        },
        {
            "Text": font.render("Expose the Criminal",settings["Antialiasing Text"], settings["Font Secondary Colour"]),
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                (settings["Height"] * 7) // 16,
                game_text[0] + settings["Width"] // 64,
                game_text[1] + settings["Height"] // 90,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Meta": "Game 1",
        },
        {
            "Text": font.render("Memory Experiment",settings["Antialiasing Text"], settings["Font Secondary Colour"]),
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                (settings["Height"] * 10) // 16,
                game_text[0] + settings["Width"] // 64,
                game_text[1] + settings["Height"] // 90,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Meta": "Game 2",
        },
        {
            "Text": font.render("Pattern Rush", settings["Antialiasing Text"], settings["Font Secondary Colour"]),
            "Pygame Button": pygame.Rect(
                settings["Width"] // 94,
                (settings["Height"] * 13) // 16,
                game_text[0] + settings["Width"] // 64,
                game_text[1] + settings["Height"] // 90,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Meta": "Game 3",
        },
    ]
    # friends?
    # game 1/2/3 (their names)
    # main menu


def displayPage(settings, screen, font, game, getFps, exit, getLB):
    lb = getLB(game)
    never = True
    while True:
        screen.fill(settings["Background Colour"])
        for button in buttons:
            pygame.draw.rect(
                screen,
                (button["Colour"]),
                button["Pygame Button"],
                border_radius=settings["Width"] // 40,
            )
            screen.blit( button["Text"], button["Pygame Button"].topleft)

                
        # screen.blit(game_over_text, game_over_text_rect)
        # screen.blit(score_text, score_text_rect)
        # for button in buttons:
        # pygame.draw.rect(
        #     screen,
        #     (button["Colour"]),
        #     button["Pygame Button"],
        #     border_radius=settings["Width"] // 40,
        # )
        # screen.blit(
        #     button["Text"],
        #     (
        #         button["Pygame Button"].centerx
        #         - button_text.get_width() // 2,
        #         button["Pygame Button"].centery
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
                        meta = button["Meta"]
                        if meta == "Main Menu":
                            return "Main Menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Main Menu"

        pygame.display.flip()

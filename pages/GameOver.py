import pygame


def init(settings, font, title_font):
    makeButtons(settings, font)
    makeText(settings, title_font)


def makeButtons(settings, font):
    global buttons
    text_width, text_height = font.size("Leaderboards")
    buttons = [
        # Default
        {
            "Name": "Leaderboards",
            "Pygame Button": pygame.Rect(
                settings["Width"] // 2 - text_width - settings["Width"] // 16,
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Font Colour": settings["Font Secondary Colour"],
            "Meta": "Leaderboards",
        },
        # Main Menu
        {
            "Name": "Main Menu",
            "Pygame Button": pygame.Rect(
                settings["Width"] // 2 + text_width + settings["Width"] // 16,
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Primary Colour"],
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Main Menu",
        },
    ]


def makeText(settings, title_font):
    global game_over_text, game_over_text_rect
    game_over_text = title_font.render(
        "Game Over", True, settings["Background Font Colour"]
    )
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.midtop = (settings["Width"] // 2, settings["Height"] // 30)


def displayPage(screen, settings, font, game, score, getFps, exit):
    never = True
    score_text = font.render(
        f"Score: {int(score)}", True, settings["Background Font Colour"]
    )
    score_text_rect = score_text.get_rect()
    score_text_rect.midtop = (
        settings["Width"] // 2,
        settings["Height"] // 20 + game_over_text.get_height(),
    )
    current = start = pygame.time.get_ticks()
    while current - start < 2000:
        screen.fill(settings["Background Colour"])
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(score_text, score_text_rect)
        for button in buttons:
            pygame.draw.rect(
                screen,
                (button["Colour"]),
                button["Pygame Button"],
                border_radius=settings["Width"] // 40,
            )
            button_text = font.render(
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
        getFps(never)
        never = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        pygame.display.flip()
    
    while True:
        screen.fill(settings["Background Colour"])
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(score_text, score_text_rect)
        for button in buttons:
            pygame.draw.rect(
                screen,
                (button["Colour"]),
                button["Pygame Button"],
                border_radius=settings["Width"] // 40,
            )
            button_text = font.render(
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
        getFps(never)
        never = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button["Pygame Button"].collidepoint(event.pos):
                        return button["Meta"]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        pygame.display.flip()

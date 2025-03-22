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
            "Text": font.render("Leaderboards", settings["Antialiasing Text"], settings["Font Secondary Colour"]),
            "Pygame Button": pygame.Rect(
                settings["Width"] // 2 - text_width - settings["Width"] // 16,
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Meta": "Leaderboards",
        },
        # Main Menu
        {
            "Text": font.render("Main Menu", settings["Antialiasing Text"], settings["Font Primary Colour"]),
            "Pygame Button": pygame.Rect(
                settings["Width"] // 2 + text_width + settings["Width"] // 16,
                (settings["Height"] * 30) // 32 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Primary Colour"],
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


def displayPage(screen, settings, font, game, score, pb, adjustment, getFps, exit):
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
    while current - start < 400:
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
            screen.blit(
                button["Text"],
                (
                    button["Pygame Button"].centerx
                    - button["Text"].get_width() // 2,
                    button["Pygame Button"].centery
                    - button["Text"].get_height() // 2,
                ),
            )
        getFps(never)
        never = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Main Menu"
        pygame.display.flip()
        current = pygame.time.get_ticks()

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
            screen.blit(
                button["Text"],
                (
                    button["Pygame Button"].centerx
                    - button["Text"].get_width() // 2,
                    button["Pygame Button"].centery
                    - button["Text"].get_height() // 2,
                ),
            )
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

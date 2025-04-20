global rating
import pygame

rating = ["poorly...", "mediocre.", "good.", "great!", "excellent!!!"]


def init(settings, font):
    makeButtons(settings, font)


def makeButtons(settings, font):
    global buttons, text_height
    text_width, text_height = font.size("Leaderboards")
    buttons = [
        # Default
        {
            "Text": font.render(
                "Leaderboards",
                settings["Antialiasing Text"],
                settings["Font Secondary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                settings["Width"] // 2 - text_width - settings["Width"] // 16,
                (settings["Height"] * 15) // 16 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Secondary Colour"],
            "Meta": "Leaderboards",
        },
        # Main Menu
        {
            "Text": font.render(
                "Main Menu",
                settings["Antialiasing Text"],
                settings["Font Primary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                settings["Width"] // 2 + text_width + settings["Width"] // 16,
                (settings["Height"] * 15) // 16 - text_height,
                text_width + settings["Width"] // 32,
                text_height + settings["Height"] // 32,
            ),
            "Colour": settings["Button Primary Colour"],
            "Meta": "Main Menu",
        },
    ]


def displayPage(
    screen,
    settings,
    font,
    small_title_font,
    bold_font,
    game,
    new_score,
    old_score,
    adjustment,
    getFps,
    exit,
):
    game_over_text = small_title_font.render(
        f"{game}: Game Over", True, settings["Background Font Colour"]
    )
    never = True
    if new_score > old_score:
        score_text = bold_font.render(
            f"Score: {int(new_score):,.2f} New Best!",
            settings["Antialiasing Text"],
            settings["Bold Contrasting Font Colour"],
        )
    else:
        score_text = font.render(
            f"Score: {int(new_score):,.2f}",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
    old_score_text = font.render(
        f"Previous best: {int(old_score):,.2f}",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    adjustment = min(4, max(0, round(adjustment * 10) + 2))
    you_did = font.render(
        f"You did {rating[adjustment]}",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    y = (
        settings["Height"] * 15 // 16
        - text_height
        + (
            -game_over_text.get_height()
            - score_text.get_height()
            - old_score_text.get_height()
            - you_did.get_height()
        )
        * 1.1
    ) // 4
    game_over_coords = (
        (settings["Width"] - game_over_text.get_width()) // 2,
        y + game_over_text.get_height() // 40,
    )
    score_coords = (
        (settings["Width"] - score_text.get_width()) // 2,
        y + game_over_text.get_height() * 1.1 + score_text.get_height() // 40,
    )
    old_score_coords = (
        (settings["Width"] - old_score_text.get_width()) // 2,
        y
        + game_over_text.get_height() * 1.1
        + score_text.get_height() * 1.1
        + old_score_text.get_height() // 40,
    )
    you_did_coords = (
        (settings["Width"] - you_did.get_width()) // 2,
        y
        + game_over_text.get_height() * 1.1
        + score_text.get_height() * 1.1
        + old_score_text.get_height() * 1.1
        + you_did.get_height() // 40,
    )
    current = start = pygame.time.get_ticks()
    while current - start < 400:
        screen.fill(settings["Background Colour"])
        screen.blit(game_over_text, game_over_coords)
        screen.blit(score_text, score_coords)
        screen.blit(old_score_text, old_score_coords)
        screen.blit(you_did, you_did_coords)
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
                    button["Pygame Button"].centerx - button["Text"].get_width() // 2,
                    button["Pygame Button"].centery - button["Text"].get_height() // 2,
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
        screen.blit(game_over_text, game_over_coords)
        screen.blit(score_text, score_coords)
        screen.blit(old_score_text, old_score_coords)
        screen.blit(you_did, you_did_coords)
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
                    button["Pygame Button"].centerx - button["Text"].get_width() // 2,
                    button["Pygame Button"].centery - button["Text"].get_height() // 2,
                ),
            )
        getFps(False)
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

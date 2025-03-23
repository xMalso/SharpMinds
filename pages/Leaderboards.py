global pygame, logging, datetime
import pygame, logging
from datetime import datetime

logging.basicConfig(
    level=logging.WARNING,
    filename=f"logs/log{datetime.now().strftime('%d-%m_%Hh-%Mm-%Ss')}.txt",
    format="%(asctime)s - %(message)s",
)


def init(settings, small_font, font, title_font):
    global lb_text, for_text, width
    makeButtons(settings, small_font)
    width = max(
        settings["Width"] * 7 // 10,
        settings["Width"]
        - buttons[0]["Pygame Button"].width
        - settings["Width"] // 100,
    )
    lb_text = title_font.render(
        "Leaderboards",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    for_text = [
        font.render(
            "for Expose the Criminal",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        ),
        font.render(
            "for Memory Experiment",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        ),
        font.render(
            "for Pattern Rush",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        ),
    ]


def makeButtons(settings, small_font):
    global buttons
    game_text = small_font.size(
        max(
            [
                "Expose the Criminal",
                "Memory Experiment",
                "Pattern Rush",
                "Friends",
                "Main Menu",
            ],
            key=lambda x: small_font.size(x)[0],
        )
    )
    game_text = (
        game_text[0] + settings["Width"] // 64,
        game_text[1] + settings["Height"] // 90,
    )
    x = settings["Width"] - game_text[0] - settings["Width"] // 94
    y = game_text[1] + settings["Height"] // 90
    buttons = [
        {
            "Text": small_font.render(
                "Expose the Criminal",
                settings["Antialiasing Text"],
                settings["Font Secondary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                x,
                settings["Height"] // 16,
                game_text[0],
                game_text[1],
            ),
            "Colour": settings["Button Secondary Colour"],
            "Meta": "1",
        },
        {
            "Text": small_font.render(
                "Memory Experiment",
                settings["Antialiasing Text"],
                settings["Font Secondary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                x,
                settings["Height"] // 16 + y,
                game_text[0],
                game_text[1],
            ),
            "Colour": settings["Button Secondary Colour"],
            "Meta": "2",
        },
        {
            "Text": small_font.render(
                "Pattern Rush",
                settings["Antialiasing Text"],
                settings["Font Secondary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                x,
                settings["Height"] // 16 + y * 2,
                game_text[0],
                game_text[1],
            ),
            "Colour": settings["Button Secondary Colour"],
            "Meta": "3",
        },
        {
            "Text": small_font.render(
                "Friends",
                settings["Antialiasing Text"],
                settings["Font Primary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                x,
                settings["Height"] // 16 + y * 3,
                game_text[0],
                game_text[1],
            ),
            "Colour": settings["Button Primary Colour"],
            "Meta": "Friends",
        },
        {
            "Text": small_font.render(
                "Main Menu",
                settings["Antialiasing Text"],
                settings["Font Quinary Colour"],
            ),
            "Pygame Button": pygame.Rect(
                x,
                settings["Height"] // 16 + y * 4,
                game_text[0],
                game_text[1],
            ),
            "Colour": settings["Button Quinary Colour"],
            "Meta": "Main Menu",
        },
    ]
    # friends?
    # game 1/2/3 (their names)
    # main menu


def loadLB(game, user_id, getLB, bold_font, settings):
    global lb, player_score, x, game_text
    lb = list(getLB(game).values())
    player_score = bold_font.render(
        f"Your PB: {getLB(game, user_id)["fields"]["score"]["doubleValue"]:.2f}",
        settings["Antialiasing Text"],
        settings["Bold Contrasting Font Colour"],
    )
    lb.sort(key=lambda x: x["fields"]["score"]["doubleValue"], reverse=True)
    x = (width - for_text[game - 1].get_width()) // 2
    game_text = for_text[game - 1]


def displayPage(
    settings, screen, font, bold_font, small_font, game, user_id, getFps, exit, getLB
):
    loadLB(game, user_id, getLB, bold_font, settings)
    never = True
    friends = False
    right_panel = pygame.Surface(
        (width, settings["Height"]),
    )
    y_for = settings["Height"] * 0.02 + lb_text.get_height()
    while True:
        screen.fill(settings["Background Colour"])
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
        right_panel.fill(settings["Background Colour"])
        right_panel.blit(
            lb_text,
            (
                (width - lb_text.get_width()) // 2,
                settings["Height"] * 0.02,
            ),
        )
        right_panel.blit(
            game_text,
            (
                x,
                y_for,
            ),
        )

        y = settings["Height"] * 0.07 + lb_text.get_height() + settings["Height"] // 90
        height = font.size("A")[1]
        right_panel.blit(
            player_score,
            ((width - player_score.get_width()) // 2, y),
        )
        y += height * 1.2
        for entry in lb:
            if y >= settings["Height"] * 0.99 - height:
                break
            if entry["fields"]["id"]["stringValue"] == user_id:
                text = bold_font.render(
                    f"{entry['fields']['username']['stringValue']}: {entry['fields']['score']['doubleValue']:.2f}",
                    settings["Antialiasing Text"],
                    settings["Bold Contrasting Font Colour"],
                )
            else:
                text = font.render(
                    f"{entry['fields']['username']['stringValue']}: {entry['fields']['score']['doubleValue']:.2f}",
                    settings["Antialiasing Text"],
                    settings["Font Primary Colour"],
                )
            right_panel.blit(text, ((width - text.get_width()) // 2, y))
            y += height
        screen.blit(right_panel, (0, 0))
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
                        elif meta == "Friends":
                            if friends == False:
                                friends = True
                                buttons[3]["Text"] = small_font.render(
                                    "Global",
                                    settings["Antialiasing Text"],
                                    settings["Font Primary Colour"],
                                )
                            else:
                                friends = False
                                buttons[3]["Text"] = small_font.render(
                                    "Friends only",
                                    settings["Antialiasing Text"],
                                    settings["Font Primary Colour"],
                                )
                        else:
                                if meta == "1" or meta == "2":
                                    game = int(meta)
                                    loadLB(game, user_id, getLB, bold_font, settings)
                                elif meta != "3":
                                    logging.error(f"Invalid game/meta: {meta}")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Main Menu"

        pygame.display.flip()

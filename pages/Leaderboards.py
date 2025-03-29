global pygame, logging
import pygame, logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

log_filename = f"logs/log{datetime.now().strftime('%d-%m_%Hh-%Mm-%Ss')}.txt"
handler = RotatingFileHandler(log_filename, maxBytes=5 * 1024**2, backupCount=10)
logging.basicConfig(
    level=logging.WARNING,
    handlers=[handler],
    format="%(filename)s:%(lineno)d | %(asctime)s - %(message)s",
)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)


def init(settings, small_font, font, title_font):
    global lb_text, for_text, width, height
    height = font.size("A")[1]
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
    global lb, player_score, x, game_text, played_score_x
    lb = list(getLB(game).values())
    player_score = bold_font.render(
        f"Your PB: {getLB(game, user_id)["score"]:,.2f}",
        settings["Antialiasing Text"],
        settings["Bold Contrasting Font Colour"],
    )
    lb.sort(key=lambda x: x["score"], reverse=True)
    played_score_x = (width - player_score.get_width()) // 2
    x = (width - for_text[game - 1].get_width()) // 2
    game_text = for_text[game - 1]


def displayPage(
    settings, screen, font, bold_font, small_font, game, user_id, getFps, exit, getLB
):
    loadLB(game, user_id, getLB, bold_font, settings)
    never = True
    friends = False
    left_panel = pygame.Surface(
        (width, settings["Height"]),
    )
    y_for = settings["Height"] * 0.02 + lb_text.get_height()
    while True:
        top = False
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
        left_panel.fill(settings["Background Colour"])
        left_panel.blit(
            lb_text,
            (
                (width - lb_text.get_width()) // 2,
                settings["Height"] * 0.02,
            ),
        )
        left_panel.blit(
            game_text,
            (
                x,
                y_for,
            ),
        )

        y = settings["Height"] * 0.02 + lb_text.get_height() + height * 1.2
        for entry in lb:
            if y >= settings["Height"] * 0.99 - height - (height * (not top)):
                if not top:
                    left_panel.blit(
                        player_score,
                        (played_score_x, y),
                    )
                break
            if entry["id"] == user_id:
                left_panel.blit(player_score, (played_score_x, y))
                top = True
            else:
                text = font.render(
                    f"{entry['username']}: {entry['score']:,.2f}",
                    settings["Antialiasing Text"],
                    settings["Font Primary Colour"],
                )
                left_panel.blit(text, ((width - text.get_width()) // 2, y))
            y += height
        screen.blit(left_panel, (0, 0))
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
                            if meta in ["1", "2", "3"]:
                                game = int(meta)
                                loadLB(game, user_id, getLB, bold_font, settings)
                            else:
                                logging.error(f"Invalid game/meta: {meta}")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Main Menu"

        pygame.display.flip()

global random, pygame, math
import random, pygame, math


def init(settings, font, title_font):
    global buffer, return_text, pause_duration, answer_text
    answer_text = title_font.render(
        f"Answer: ",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    ready_text = makeButtons(settings, font)
    buffer = (
        settings["Width"] * 0.4,
        max(ready_text[1] * 2, ready_text[1] + settings["Height"] // 50)
        + settings["Height"] * 0.2,
    )
    return_text = splitText(
        font, settings["Width"] // 4, "Press ESC to return to games menu"
    )
    pause_duration = 0


def makeButtons(settings, font):
    global ready_button, next_button
    ready_text = font.size("Ready")
    next_text = font.size("Next Page")
    ready_button = {
        "Pygame Button": pygame.Rect(
            settings["Width"] // 2 - (ready_text[0] + settings["Width"] // 64) // 2,
            settings["Height"] - (ready_text[1] + settings["Height"] // 50),
            ready_text[0] + settings["Width"] // 64,
            ready_text[1],
        ),
        "Colour": settings["Button Primary Colour"],
        "Font Colour": settings["Font Primary Colour"],
        "Meta": "Ready",
    }
    next_button = {
        "Text": "Next Page",
        "Pygame Button": pygame.Rect(
            settings["Width"] // 2 - (next_text[0] + settings["Width"] // 64) // 2,
            settings["Height"] - (next_text[1] + settings["Height"] // 50),
            next_text[0] + settings["Width"] // 64,
            next_text[1],
        ),
        "Colour": settings["Button Primary Colour"],
        "Font Colour": settings["Font Primary Colour"],
        "Meta": "Next Page",
    }
    return ready_text


def makePickerButtons(settings, font):
    global picker_buttons, height, picker_text, width
    erase_text = font.size("Remove Guess")
    width = min(settings["Width"] // 5, margin_width // 1.3)
    height = erase_text[1] * 1.3
    side = min(width, height)
    width_diff = width - side
    height_diff = height - side
    picker_text = [
        {
            "Text": "Shape",
            "x": settings["Width"] - width * 1.95,
            "y": settings["Height"] * 0.95 - height * 2.7,
        },
        {
            "Text": "Colour",
            "x": settings["Width"] - width * 1.95,
            "y": settings["Height"] * 0.93 - height * 4.7,
        },
    ]
    picker_buttons = [
        {
            "Meta": "Triangle",
            "Pygame Button": pygame.Rect(
                settings["Width"] - width * 1.15 + width_diff // 2,
                settings["Height"] * 0.93 - height * 2 + height_diff // 2,
                side,
                side,
            ),
            "Type": "Shape",
        },
        {
            "Meta": "Circle",
            "Pygame Button": pygame.Rect(
                settings["Width"] - width * 2.45 + width_diff // 2,
                settings["Height"] * 0.93 - height * 2 + height_diff // 2,
                side,
                side,
            ),
            "Type": "Shape",
        },
        {
            "Meta": "Square",
            "Pygame Button": pygame.Rect(
                settings["Width"] - width * 3.75 + width_diff // 2,
                settings["Height"] * 0.93 - height * 2 + height_diff // 2,
                side,
                side,
            ),
            "Type": "Shape",
        },
        {
            "Meta": "Game Primary Colour",
            "Pygame Button": pygame.Rect(
                settings["Width"] - width * 3.75,
                settings["Height"] * 0.91 - height * 4,
                width,
                height,
            ),
            "Type": "Colour",
            "Text": "Colour 1",
            "Font Colour": settings["Game Primary Font Colour"],
        },
        {
            "Meta": "Game Secondary Colour",
            "Pygame Button": pygame.Rect(
                settings["Width"] - width * 2.45,
                settings["Height"] * 0.91 - height * 4,
                width,
                height,
            ),
            "Type": "Colour",
            "Text": "Colour 2",
            "Font Colour": settings["Game Secondary Font Colour"],
        },
        {
            "Meta": "Game Tertiary Colour",
            "Pygame Button": pygame.Rect(
                settings["Width"] - width * 1.15,
                settings["Height"] * 0.91 - height * 4,
                width,
                height,
            ),
            "Type": "Colour",
            "Text": "Colour 3",
            "Font Colour": settings["Game Tertiary Font Colour"],
        },
        {
            "Meta": "Erase",
            "Pygame Button": pygame.Rect(
                settings["Width"] - width * 3.75,
                settings["Height"] * 0.89 - height * 6,
                width * 3.6,
                height,
            ),
            "Colour": settings["Button Quinary Colour"],
            "Font Colour": settings["Font Quinary Colour"],
            "Text": "Remove Guess",
            "Type": "Button",
        },
        {
            "Meta": "Ready",
            "Pygame Button": pygame.Rect(
                settings["Width"] - width * 3.75,
                settings["Height"] * 0.97 - height,
                width * 3.6,
                height,
            ),
            "Colour": settings["Button Primary Colour"],
            "Font Colour": settings["Font Primary Colour"],
            "Text": "Ready",
            "Type": "Button",
        },
    ]


def drawGrid(screen, settings, buffer_width, patterns, shift):
    pygame.draw.rect(
        screen,
        settings["Grid Background Colour"],
        (
            buffer_width,
            margin_height,
            cols * (button_side + 2),
            rows * (button_side + 2),
        ),
    )
    for row in range(rows + 1):
        pygame.draw.line(
            screen,
            settings["Grid Line Colour"],
            (buffer_width, row * (button_side + 2) + margin_height),
            (
                buffer_width + (cols) * (button_side + 2),
                row * (button_side + 2) + margin_height,
            ),
            2
        )
    for col in range(cols + 1):
        pygame.draw.line(
            screen,
            settings["Grid Line Colour"],
            (col * (button_side + 2) + buffer_width, margin_height),
            (
                col * (button_side + 2) + buffer_width,
                (rows) * (button_side + 2) + margin_height,
            ),
            2
        )

    for r, c in patterns:
        details = patterns[(r, c)]
        button = buttons[r][c]
        if shift:
            button["Pygame Button"].left += margin_width
        if details["Shape"] == "Circle":
            pygame.draw.circle(
                screen, details["Colour"], button["Pygame Button"].center, radius
            )
        elif details["Shape"] == "Square":
            pygame.draw.rect(
                screen,
                details["Colour"],
                (
                    button["Pygame Button"].centerx - radius,
                    button["Pygame Button"].centery - radius,
                    radius * 2,
                    radius * 2,
                ),
            )
        else:
            height = (radius * (3**0.5)) // 2
            points = [
                (
                    button["Pygame Button"].centerx,
                    button["Pygame Button"].centery - height,
                ),
                (
                    button["Pygame Button"].centerx - radius,
                    button["Pygame Button"].centery + height,
                ),
                (
                    button["Pygame Button"].centerx + radius,
                    button["Pygame Button"].centery + height,
                ),
            ]
            pygame.draw.polygon(screen, details["Colour"], points)
        if shift:
            button["Pygame Button"].left -= margin_width


def drawPicker(screen, settings, font):
    for button in picker_buttons:
        button_type = button["Type"]
        if button_type == "Shape":
            meta = button["Meta"]
            if meta == "Triangle":
                triangle_width = button["Pygame Button"].width // 2
                triangle_height = (triangle_width * (3**0.5)) // 2
                points = [
                    (
                        button["Pygame Button"].centerx,
                        button["Pygame Button"].centery - triangle_height,
                    ),
                    (
                        button["Pygame Button"].centerx - triangle_width,
                        button["Pygame Button"].centery + triangle_height,
                    ),
                    (
                        button["Pygame Button"].centerx + triangle_width,
                        button["Pygame Button"].centery + triangle_height,
                    ),
                ]
                pygame.draw.polygon(screen, picker_colour, points)
            elif meta == "Square":
                pygame.draw.rect(screen, picker_colour, button["Pygame Button"])
            else:
                pygame.draw.circle(
                    screen,
                    picker_colour,
                    button["Pygame Button"].center,
                    button["Pygame Button"].width // 2,
                )
        elif button_type == "Colour":
            pygame.draw.rect(
                screen,
                settings[button["Meta"]],
                button["Pygame Button"],
                border_radius=settings["Width"] // 60,
            )
            text = font.render(
                button["Text"],
                settings["Antialiasing Text"],
                button["Font Colour"],
            )
            screen.blit(
                text,
                (
                    button["Pygame Button"].centerx - text.get_width() // 2,
                    button["Pygame Button"].centery - text.get_height() // 2,
                ),
            )
        else:
            pygame.draw.rect(
                screen,
                button["Colour"],
                button["Pygame Button"],
                border_radius=settings["Width"] // 60,
            )
            text = font.render(
                button["Text"],
                settings["Antialiasing Text"],
                button["Font Colour"],
            )
            screen.blit(
                text,
                (
                    button["Pygame Button"].centerx - text.get_width() // 2,
                    button["Pygame Button"].centery - text.get_height() // 2,
                ),
            )
    for data in picker_text:
        text = font.render(
            data["Text"],
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
        screen.blit(
            text,
            (
                data["x"] - text.get_width() // 2,
                data["y"] - text.get_height() // 2,
            ),
        )
    text_y = settings["Height"] * 0.89 - height * 7
    if remove:
        return_text = splitText(
            font, margin_width * 3 // 1.3, "Click a box to remove guess"
        )
        for line in return_text:
            text = font.render(
                line,
                settings["Antialiasing Text"],
                settings["Background Font Colour"],
            )
            text_y -= text.get_height()
            screen.blit(
                text,
                (
                    settings["Width"] - width * 1.95 - text.get_width() // 2,
                    text_y,
                ),
            )
        text = font.render(
            "Current Guess:",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
        text_height = text.get_height()
        text_y = min(
            settings["Height"] * 0.89 - height * 7 - text_height * 4.5,
            text_y - text_height * 1.5,
        )
        screen.blit(
            text,
            (
                settings["Width"] - width * 1.95 - text.get_width() // 2,
                text_y,
            ),
        )
    else:
        text = font.render(
            "Current Guess:",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
        text_height = text.get_height()
        screen.blit(
            text,
            (
                settings["Width"] - width * 1.95 - text.get_width() // 2,
                text_y - text_height * 4.5,
            ),
        )
        side = min(width, text_height)
        if picker_shape == "Triangle":
            triangle_height = side * 1.5
            triangle_width = triangle_height * 2 // (3**0.5)
            points = [
                (
                    settings["Width"] - width * 1.95,
                    text_y - triangle_height - text_height * 1.25,
                ),
                (
                    settings["Width"] - width * 1.95 - triangle_width,
                    text_y - text_height * 1.25 + triangle_height,
                ),
                (
                    settings["Width"] - width * 1.95 + triangle_width,
                    text_y - text_height * 1.25 + triangle_height,
                ),
            ]
            pygame.draw.polygon(screen, picker_colour, points)
        elif picker_shape == "Square":
            pygame.draw.rect(
                screen,
                picker_colour,
                (
                    settings["Width"] - width * 1.95 - (side * 3) // 2,
                    text_y - text_height * 1.25 - (side * 3) // 2,
                    side * 3,
                    side * 3,
                ),
            )
        else:
            pygame.draw.circle(
                screen,
                picker_colour,
                (settings["Width"] - width * 1.95, text_y - text_height * 1.25),
                (side * 3) // 2,
            )


def splitText(font, max_width, words):
    words = words.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        text_width, _ = font.size(test_line)

        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def calculateScore(score):
    for r, c in all_positions:
        if (r, c) not in answer and (r, c) not in guess:
            score += max_score / 20
        elif (r, c) in answer and (r, c) in guess:
            if pattern[(r, c)] == guess[(r, c)]:
                score += max_score
            elif (
                pattern[(r, c)]["Colour"] == guess[(r, c)]["Colour"]
                or pattern[(r, c)]["Shape"] == guess[(r, c)]["Shape"]
            ):
                score += max_score / 3
    return score


def game2(settings, screen, font, getFps, exit):
    global difficulty, buttons, rows, cols, button_side, radius, margin_width, margin_height, return_text, multiplier, pause_duration, avg
    score = 0
    difficulty = settings["Adaptive Difficulty"][1]
    multiplier = (difficulty - 1) / 10 + 1
    avg = difficulty**0.5 * 10
    cols = rows = math.ceil(avg**0.5)
    avg = int(avg // 3)
    button_width = (settings["Width"] - buffer[0]) // cols
    button_height = (settings["Height"] - buffer[1]) // rows
    button_side = int(min(button_width, button_height))
    radius = int(button_side * 0.3)
    margin_width, margin_height = (
        (settings["Width"] - (button_side * cols)) // 4,
        (settings["Height"] - (button_side * rows)) // 2,
    )
    makePickerButtons(settings, font)
    buttons = []
    y = margin_height + 2
    for row in range(rows):
        x = margin_width + 2
        button_row = []
        for col in range(cols):
            button = {
                "Pygame Button": pygame.Rect(x, y, button_side, button_side),
            }
            button_row.append(button)
            x += button_side + 2
        y += button_side + 2
        buttons.append(button_row)
    rounds = 1
    for i in range(rounds):
        round_score, meta = cycle(i, settings, getFps, screen, font, exit)
        if round_score is None:
            return (round_score, None, meta)
        score += round_score
    adjustment = ((score / rounds) - (540 * multiplier)) / 100
    if adjustment < 0: adjustment /= 10
    return (score, adjustment, meta)


def cycle(round_number, settings, getFps, screen, font, exit):
    global answer, pattern, picker_shape, picker_colour, remove, guess, max_score, all_positions
    round_text = font.render(
        f"Round {round_number + 1}",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    all_positions = [(r, c) for r in range(rows) for c in range(cols)]
    num_shapes = avg
    missing = rows * cols - num_shapes
    max_score = 600 * multiplier / (num_shapes + missing * 0.05)
    random.shuffle(all_positions)
    answer = set(all_positions[:num_shapes])
    pattern = {}
    for r, c in answer:
        pattern[(r, c)] = {
            "Shape": random.choice(["Circle", "Square", "Triangle"]),
            "Colour": random.choice(
                [
                    settings["Game Primary Colour"],
                    settings["Game Secondary Colour"],
                    settings["Game Tertiary Colour"],
                ]
            ),
        }
    ready = False
    while not ready:
        screen.fill(settings["Background Colour"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                return None, "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, "Game Menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if ready_button["Pygame Button"].collidepoint(event.pos):
                    ready = True
        drawGrid(screen, settings, margin_width * 2, pattern, True)
        height = settings["Height"] // 200
        pygame.draw.rect(
            screen,
            ready_button["Colour"],
            ready_button["Pygame Button"],
            border_radius=settings["Width"] // 60,
        )
        for line in return_text:
            text = font.render(
                line,
                settings["Antialiasing Text"],
                settings["Background Font Colour"],
            )
            screen.blit(
                text,
                (
                    settings["Width"] * 7 // 8
                    - text.get_width() // 2
                    - settings["Width"] // 200,
                    height,
                ),
            )
            height += text.get_height()
        screen.blit(
            round_text,
            (
                (settings["Width"] - round_text.get_width()) // 2,
                settings["Height"] // 200,
            ),
        )
        # score_text = font.render(
        #     f"Score: {int(score)}",
        #     settings["Antialiasing Text"],
        #     settings["Background Font Colour"],
        # )
        # screen.blit(
        #     score_text,
        #     (
        #         (settings["Width"] - score_text.get_width()) // 2,
        #         settings["Height"] // 200 + round_text.get_height(),
        #     ),
        # )
        ready_text = font.render(
            "Ready",
            settings["Antialiasing Text"],
            ready_button["Font Colour"],
        )
        screen.blit(
            ready_text,
            (
                ready_button["Pygame Button"].left + settings["Width"] // 128,
                ready_button["Pygame Button"].top,
            ),
        )
        getFps()
        pygame.display.flip()
    current = start = pygame.time.get_ticks()
    remaining_time = int((pause_duration - (current - start)) / 100) / 10
    while remaining_time > 0:
        screen.fill(settings["Background Colour"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                return None, "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, "Game Menu"
        current = pygame.time.get_ticks()
        remaining_time = int((pause_duration - (current - start)) / 100) / 10
        time_text = font.render(
            f"Time: {remaining_time}s",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
        screen.blit(
            time_text,
            (
                (settings["Width"] - time_text.get_width()) // 2,
                (settings["Height"] - time_text.get_height()) // 2,
            ),
        )
        height = settings["Height"] // 200
        for line in return_text:
            text = font.render(
                line,
                settings["Antialiasing Text"],
                settings["Background Font Colour"],
            )
            screen.blit(
                text,
                (
                    settings["Width"] * 7 // 8
                    - text.get_width() // 2
                    - settings["Width"] // 200,
                    height,
                ),
            )
            height += text.get_height()
        screen.blit(
            round_text,
            (
                (settings["Width"] - round_text.get_width()) // 2,
                settings["Height"] // 200,
            ),
        )
        score_text = font.render(
            f"Score: {int(score)}",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
        screen.blit(
            score_text,
            (
                (settings["Width"] - score_text.get_width()) // 2,
                settings["Height"] // 200 + round_text.get_height(),
            ),
        )
        getFps()
        pygame.display.flip()
    picker_shape = "Circle"
    picker_colour = settings["Game Primary Colour"]
    guess = {}
    remove = False
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                return None, "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, "Game Menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in picker_buttons:
                    if button["Pygame Button"].collidepoint(event.pos):
                        meta = button["Meta"]
                        if meta in ["Triangle", "Circle", "Square"]:
                            picker_shape = meta
                            remove = False
                        elif meta in [
                            "Game Primary Colour",
                            "Game Secondary Colour",
                            "Game Tertiary Colour",
                        ]:
                            picker_colour = settings[meta]
                            remove = False
                        elif meta == "Erase":
                            remove = not remove
                        elif meta == "Ready":
                            score = calculateScore(0)
                            finished = True
                        else:
                            print(
                                f"Unknown meta: {meta}, \n\n\nButton: {button}, \n\n\n{picker_buttons} \n\n"
                            )
                for r, c in all_positions:
                    button = buttons[r][c]
                    if button["Pygame Button"].collidepoint(event.pos):
                        if remove:
                            if (r, c) in guess:
                                del guess[(r, c)]
                        else:
                            guess[(r, c)] = {
                                "Colour": picker_colour,
                                "Shape": picker_shape,
                            }
        screen.fill(settings["Background Colour"])
        drawGrid(screen, settings, margin_width, guess, False)
        drawPicker(screen, settings, font)
        height = settings["Height"] // 200
        for line in return_text:
            text = font.render(
                line,
                settings["Antialiasing Text"],
                settings["Background Font Colour"],
            )
            screen.blit(
                text,
                (
                    settings["Width"] * 7 // 8
                    - text.get_width() // 2
                    - settings["Width"] // 200,
                    height,
                ),
            )
            height += text.get_height()
        # score_text = font.render(
        #     f"Score: {int(score)}",
        #     settings["Antialiasing Text"],
        #     settings["Background Font Colour"],
        # )
        # screen.blit(
        #     score_text,
        #     (
        #         (settings["Width"] - score_text.get_width()) // 2,
        #         settings["Height"] // 200,
        #     ),
        # )
        screen.blit(
            round_text,
            (
                (settings["Width"] - round_text.get_width()) // 2,
                settings["Height"] // 200,
            ),
        )

        getFps()
        pygame.display.flip()
    next = False
    round_text = font.render(
        f"Round {round_number + 1}, Score: {int(score)}",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    while not next:
        screen.fill(settings["Background Colour"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return score, "Game Menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if next_button["Pygame Button"].collidepoint(event.pos):
                    return score, "Game Over"
        drawGrid(screen, settings, margin_width * 2, pattern, True)
        height = settings["Height"] // 200
        pygame.draw.rect(
            screen,
            next_button["Colour"],
            next_button["Pygame Button"],
            border_radius=settings["Width"] // 60,
        )
        screen.blit(
            round_text,
            (
                (settings["Width"] - round_text.get_width()) // 2,
                settings["Height"] // 200,
            ),
        )
        # score_text = font.render(
        #     f"Score: {int(score)}",
        #     settings["Antialiasing Text"],
        #     settings["Background Font Colour"],
        # )
        # screen.blit(
        #     score_text,
        #     (
        #         (settings["Width"] - score_text.get_width()) // 2,
        #         settings["Height"] // 200 + round_text.get_height(),
        #     ),
        # )
        next_text = font.render(
            "Next Page",
            settings["Antialiasing Text"],
            next_button["Font Colour"],
        )
        screen.blit(
            next_text,
            (
                next_button["Pygame Button"].left + settings["Width"] // 128,
                next_button["Pygame Button"].top,
            ),
        )
        screen.blit(
            answer_text,
            (
                (settings["Width"] - answer_text.get_width()) // 2,
                settings["Height"] // 200,
            ),
        )
        getFps()
        pygame.display.flip()
    return score, "Game Over"

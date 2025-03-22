global random, pygame, math, np
import random, pygame, math, numpy as np


def init(settings, font, title_font):
    global return_text, pause_duration, answer_text, guess_text, help_lines
    return_lines = splitText(
        font,
        settings["Width"] // 5,
        "Memorise the grid and replicate it on the next page",
    )
    help_lines = []
    for line in return_lines:
        help_lines.append(
            font.render(
                line,
                settings["Antialiasing Text"],
                settings["Background Font Colour"],
            )
        )
    answer_text = title_font.render(
        "Answer: ",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    guess_text = title_font.render(
        "Guess: ",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    makeButtons(settings, font)
    for i in range(2):
        page1_buttons[i]["Text"] = font.render(
            page1_buttons[i]["Meta"],
            settings["Antialiasing Text"],
            page1_buttons[i]["Font Colour"],
        )
    return_text = []
    temp = splitText(font, settings["Width"] // 4, "Press ESC to return to games menu")
    for text in temp:
        return_text.append(
            font.render(
                text,
                settings["Antialiasing Text"],
                settings["Background Font Colour"],
            )
        )
    pause_duration = 0


def makeButtons(settings, font):
    global page1_buttons, next_button
    ready_text = font.size("Ready")
    help_text = font.size("Help")
    next_text = font.size("Next Page")
    page1_buttons = [
        {
            "Pygame Button": pygame.Rect(
                settings["Width"] // 3 - (ready_text[0] + settings["Width"] // 64) // 2,
                settings["Height"] - (ready_text[1] + settings["Height"] // 50),
                ready_text[0] + settings["Width"] // 64,
                ready_text[1],
            ),
            "Colour": settings["Button Primary Colour"],
            "Font Colour": settings["Font Primary Colour"],
            "Meta": "Ready",
        },
        {
            "Pygame Button": pygame.Rect(
                settings["Width"] * 2 // 3
                - (help_text[0] + settings["Width"] // 64) // 2,
                settings["Height"] - (help_text[1] + settings["Height"] // 50),
                help_text[0] + settings["Width"] // 64,
                help_text[1],
            ),
            "Colour": settings["Button Secondary Colour"],
            "Font Colour": settings["Font Secondary Colour"],
            "Meta": "Help",
        },
    ]
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


def makePickerButtons(settings, font):
    global picker_buttons, height, picker_text, width
    erase_text = font.size("Remove Guess")
    width = min(settings["Width"] // 5, margin_width // 2.6)
    height = min(erase_text[1] * 1.3, settings["Height"] * 0.8)
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


def drawGrid(screen, settings, patterns, shift=0):
    buffer_width = margin_width // 2 + shift
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
            2,
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
            2,
        )

    for r, c in patterns:
        details = patterns[(r, c)]
        button = buttons[r][c]
        button["Pygame Button"].left += shift
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
        button["Pygame Button"].left -= shift


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
        for line in remove_text[::-1]:
            text_y -= line.get_height()
            screen.blit(
                line,
                (
                    settings["Width"] - width * 1.95 - line.get_width() // 2,
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
            lb["empty"] += 1
        elif (r, c) in answer and (r, c) in guess:
            if pattern[(r, c)] == guess[(r, c)]:
                score += max_score
                lb["right"] += 1
            elif (
                pattern[(r, c)]["Colour"] == guess[(r, c)]["Colour"]
                or pattern[(r, c)]["Shape"] == guess[(r, c)]["Shape"]
            ):
                score += max_score / 3
                lb["kinda"] += 1
    print(
        "floating pres diff",
        score - (((lb["empty"] * 0.05) + (lb["kinda"] / 3) + lb["right"]) * lb["max"]),
    )
    return score


def game2(settings, screen, font, getFps, exit, getID, updateLB):
    global difficulty, buffer, buttons, rows, cols, button_side, radius, margin_width, margin_height, multiplier, pause_duration, avg, lb, remove_text
    val = getID()
    lb = {
        "empty": 0,
        "right": 0,
        "kinda": 0,
        "game": int(2),
        "id": str(val[0]),
        "username": str(val[1]),
        "score": 0,
        "max": 0,
    }
    score = 0
    buffer = (
        settings["Width"] * 0.6,
        max(
            page1_buttons[0]["Text"].get_height() * 2,
            page1_buttons[0]["Text"].get_height() + settings["Height"] // 50,
        )
        + settings["Height"] * 0.2,
    )
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
        (settings["Width"] - (button_side * cols)) // 2,
        (settings["Height"] - (button_side * rows)) // 2,
    )
    temp = splitText(font, margin_width * 3 // 2.6, "Click a box to remove guess")
    remove_text = []
    for text in temp:
        remove_text.append(
            font.render(
                text,
                settings["Antialiasing Text"],
                settings["Background Font Colour"],
            )
        )
    makePickerButtons(settings, font)
    buttons = []
    y = margin_height + 2
    for row in range(rows):
        x = margin_width // 2 + 2
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
    rounds_played = None
    for i in range(rounds):
        round_score, meta = cycle(i, settings, getFps, screen, font, exit)
        if round_score is None:
            return None, None, meta, None
        score += round_score
        if meta != "Game Over":
            rounds_played = i + 1
            break
    if not rounds_played:
        rounds_played = rounds
    adjustment = ((score / rounds_played) - (540 * multiplier)) / 1600
    adjustment = float(
        np.piecewise(
            adjustment, [x < 0, x >= 0], [lambda x: (x**3 + x) / 2, lambda x: x * 16]
        )
    )
    lb["max"] = float(lb["max"])
    lb["score"] = float(score)
    lb["empty"] = int(lb["empty"])
    lb["right"] = int(lb["right"])
    lb["kinda"] = int(lb["kinda"])
    pb = updateLB(2, lb)
    return score, adjustment, meta, pb


def cycle(round_number, settings, getFps, screen, font, exit):
    global answer, pattern, picker_shape, picker_colour, remove, guess, max_score, all_positions
    never = True
    round_text = font.render(
        f"Round {round_number + 1}",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    all_positions = [(r, c) for r in range(rows) for c in range(cols)]
    num_shapes = avg
    missing = rows * cols - num_shapes
    max_score = 600 * multiplier / (num_shapes + missing * 0.05)
    lb["max"] = max_score
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
    meta = None
    while meta != "Ready":
        screen.fill(settings["Background Colour"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                return None, "Quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, "Game Menu"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                meta = None
                for button in page1_buttons:
                    if button["Pygame Button"].collidepoint(event.pos):
                        meta = button["Meta"]
        drawGrid(
            screen,
            settings,
            pattern,
            margin_width // 2,
        )
        height = settings["Height"] // 200
        for button in page1_buttons:
            pygame.draw.rect(
                screen,
                button["Colour"],
                button["Pygame Button"],
                border_radius=settings["Width"] // 60,
            )
            screen.blit(
                button["Text"],
                (
                    button["Pygame Button"].left + settings["Width"] // 128,
                    button["Pygame Button"].top,
                ),
            )
        for line in return_text:
            screen.blit(
                line,
                (
                    settings["Width"] * 7 // 8
                    - line.get_width() // 2
                    - settings["Width"] // 200,
                    height,
                ),
            )
            height += line.get_height()
        screen.blit(
            round_text,
            (
                (settings["Width"] - round_text.get_width()) // 2,
                settings["Height"] // 200,
            ),
        )
        if meta == "Help":
            height = settings["Height"] - page1_buttons[1]["Pygame Button"].top
            for line in help_lines[::-1]:
                screen.blit(
                    line,
                    (
                        settings["Width"] * 7 // 8
                        - line.get_width() // 2
                        - settings["Width"] // 200,
                        height,
                    ),
                )
                height -= line.get_height()
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
        getFps(never)
        never = False
        pygame.display.flip()
    current = start = pygame.time.get_ticks()
    remaining_time = int((pause_duration - (current - start)) / 100) / 10
    while remaining_time > 0:
        screen.fill(settings["Background Colour"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                return None, "Quit"
            elif event.type == pygame.KEYDOWN:
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
            screen.blit(
                line,
                (
                    settings["Width"] * 7 // 8
                    - line.get_width() // 2
                    - settings["Width"] // 200,
                    height,
                ),
            )
            height += line.get_height()
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
        getFps(never)
        never = False
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, "Game Menu"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
        drawGrid(screen, settings, guess)
        drawPicker(screen, settings, font)
        height = settings["Height"] // 200
        for line in return_text:
            screen.blit(
                line,
                (
                    settings["Width"] * 7 // 8
                    - line.get_width() // 2
                    - settings["Width"] // 200,
                    height,
                ),
            )
            height += line.get_height()
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

        getFps(never)
        never = False
        pygame.display.flip()
    next = False
    score = min(score + 0.000001, 600 * multiplier)
    round_text = font.render(
        f"Round {round_number + 1}, Score: {int(score)}/{int(600*multiplier)}",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    while not next:
        screen.fill(settings["Background Colour"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, "Quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return score, "Game Menu"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if next_button["Pygame Button"].collidepoint(event.pos):
                    return score, "Game Over"
        drawGrid(
            screen,
            settings,
            pattern,
            -(settings["Width"] // 4) + margin_width // 2,
        )
        drawGrid(
            screen,
            settings,
            guess,
            (settings["Width"] // 4) + margin_width // 2,
        )
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
                (settings["Width"] // 2 - answer_text.get_width()) // 2,
                settings["Height"] // 200,
            ),
        )
        screen.blit(
            guess_text,
            (
                (settings["Width"] * 1.5 - guess_text.get_width()) // 2,
                settings["Height"] // 200,
            ),
        )
        getFps(never)
        never = False
        pygame.display.flip()

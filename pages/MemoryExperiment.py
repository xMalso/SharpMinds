global random, pygame, math
import random, pygame, math


def init(settings, font):
    global buffer, return_text, pause_duration
    makeButtons(settings, font)
    buffer = (
        settings["Width"] * 0.4,
        max(ready_text[1] * 2, ready_text[1] + settings["Height"] // 50)
        + settings["Height"] * 0.2,
    )
    return_text = splitText(font, settings["Width"] // 4)
    pause_duration = 10000


def makeButtons(settings, font):
    global ready_button, ready_text
    ready_text = font.size("Ready")
    ready_button = {
        "Text": "Ready",
        "Pygame Button": pygame.Rect(
            settings["Width"] // 2 - (ready_text[0] + settings["Width"] // 64) // 2,
            int(settings["Height"]) - (ready_text[1] + settings["Height"] // 50),
            ready_text[0] + settings["Width"] // 64,
            ready_text[1],
        ),
        "Colour": settings["Button Primary Colour"],
        "Font Colour": settings["Font Primary Colour"],
        "Meta": "Ready",
    }


def makePickerButtons(settings, font):
    global picker_buttons, erase_text
    erase_text = font.size("Remove Guess")
    width = min(settings["Height"] // 10, margin_width // 1.3) // 2
    picker_buttons = [
        {
            "Meta": "Triangle",
            "Pygame Button": pygame.Rect(
                settings["Width"] - (margin_width * 1.15) // 1.3,
                settings["Height"] * 0.95 - width,
                width * 2,
                width * 2,
            ),
            # "x": settings["Width"] - (margin_width * 1.15) // 1.3,
            # "y": settings["Height"] * 0.95 - width,
            # "Width": width * 2,
            # "Height": width * 2,
            "Type": "Shape",
        },
        {
            "Meta": "Circle",
            "Pygame Button": pygame.Rect(
                settings["Width"] - (margin_width * 2.45) // 1.3,
                settings["Height"] * 0.95 - width,
                width * 2,
                width * 2,
            ),
            "Type": "Shape",
        },
        {
            "Meta": "Square",
            "Pygame Button": pygame.Rect(
                settings["Width"] - (margin_width * 3.75) // 1.3,
                settings["Height"] * 0.95 - width,
                width * 2,
                width * 2,
            ),
            "Type": "Shape",
        },
        {
            "Meta": "Game Primary Colour",
            "Pygame Button": pygame.Rect(
                settings["Width"] - (margin_width * 1.15) // 1.3,
                settings["Height"] * 0.8 - width,
                width * 2,
                width * 2,
            ),
            "Type": "Colour",
        },
        {
            "Meta": "Game Secondary Colour",
            "Pygame Button": pygame.Rect(
                settings["Width"] - (margin_width * 2.45) // 1.3,
                settings["Height"] * 0.8 - width,
                width * 2,
                width * 2,
            ),
            "Type": "Colour",
        },
        {
            "Meta": "Game Tertiary Colour",
            "Pygame Button": pygame.Rect(
                settings["Width"] - (margin_width * 3.75) // 1.3,
                settings["Height"] * 0.8 - width,
                width * 2,
                width * 2,
            ),
            "Type": "Colour",
        },
        {
            "Meta": "Erase",
            "Pygame Button": pygame.Rect(
                settings["Width"] - (margin_width * 3.75) // 1.3,
                settings["Height"] * 0.65 - width,
                width * 2,
                (margin_width * 3) // 1.3,
            ),
            "Colour": settings["Button Quaternary Colour"],
            "Font Colour": settings["Font Quaternary Colour"],
            "Text": "Remove Guess",
            "Type": "Eraser",
        },
    ]


def findBestGrid():
    # target = avg
    # target = round(target)

    # best_diff = target
    # best_pair = (None, None)
    # for i in range(1, target + 1):
    #     for j in range(i, min(target + 1, i + 6)):
    #         product = i * j
    #         diff = abs(product - target)
    #         if diff < best_diff:
    #             best_diff = diff
    #             best_pair = (i, j)
    #         elif diff == best_diff:
    #             if abs(i - j) < abs(best_pair[0] - best_pair[1]):
    #                 best_pair = (i, j)
    #     if best_pair[0] < best_pair[1]:
    #         best_pair = (best_pair[1], best_pair[0])
    # return best_pair
    return math.ceil(avg**0.5), math.ceil(avg**0.5)


def drawGrid(screen, settings, buffer_width, patterns, shift):
    # drawEmptyGrid(screen, settings, buffer_width)
    pygame.draw.rect(
        screen,
        settings["Grid Background Colour"],
        (
            buffer_width,
            margin_height,
            cols * (button_side + 1),
            rows * (button_side + 1),
        ),
    )
    for row in range(rows + 1):
        pygame.draw.line(
            screen,
            settings["Grid Line Colour"],
            (buffer_width, row * (button_side + 1) + margin_height),
            (
                buffer_width + (cols) * (button_side + 1),
                row * (button_side + 1) + margin_height,
            ),
        )
    for col in range(cols + 1):
        pygame.draw.line(
            screen,
            settings["Grid Line Colour"],
            (col * (button_side + 1) + buffer_width, margin_height),
            (
                col * (button_side + 1) + buffer_width,
                (rows) * (button_side + 1) + margin_height,
            ),
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


# def drawEmptyGrid(screen, settings, buffer_width):
#     pygame.draw.rect(
#         screen,
#         settings["Grid Background Colour"],
#         (
#             buffer_width,
#             margin_height,
#             cols * (button_side + 1),
#             rows * (button_side + 1),
#         ),
#     )
#     for row in range(rows + 1):
#         pygame.draw.line(
#             screen,
#             settings["Grid Line Colour"],
#             (buffer_width, row * (button_side + 1) + margin_height),
#             (
#                 buffer_width + (cols) * (button_side + 1),
#                 row * (button_side + 1) + margin_height,
#             ),
#         )
#     for col in range(cols + 1):
#         pygame.draw.line(
#             screen,
#             settings["Grid Line Colour"],
#             (col * (button_side + 1) + buffer_width, margin_height),
#             (
#                 col * (button_side + 1) + buffer_width,
#                 (rows) * (button_side + 1) + margin_height,
#             ),
#         )


def drawPicker(screen, settings, font):
    for button in picker_buttons:
        button_type = button["Type"]
        if button_type == "Shape":
            meta = button["Meta"]
            if meta == "Triangle":
                width = button["Pygame Button"].width // 2
                height = (width * (3**0.5)) // 2
                points = [
                    (
                        button["Pygame Button"].centerx,
                        button["Pygame Button"].centery - height,
                    ),
                    (
                        button["Pygame Button"].centerx - width,
                        button["Pygame Button"].centery + height,
                    ),
                    (
                        button["Pygame Button"].centerx + width,
                        button["Pygame Button"].centery + height,
                    ),
                ]
                pygame.draw.polygon(screen, picker_colour, points)
            elif meta == "Square":
                pygame.draw.rect(screen, picker_colour, button["Pygame Button"])
            else:
                pygame.draw.circle(screen, picker_colour, button["Pygame Button"].center, button["Pygame Button"].width)
        elif button_type == "Colour":
            pygame.draw.rect(screen, settings[button["Meta"]], button["Pygame Button"])
        else:
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
            pygame.draw.rect(screen, button["Colour"], button["Pygame Button"])


def splitText(font, max_width):
    words = ["Press", "ESC", "to", "return", "to", "games", "menu"]
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


def Game2(settings, screen, font, getFps, exit):
    global difficulty, buttons, rows, cols, button_side, radius, margin_width, margin_height, score, return_text, multiplier, pause_duration, avg
    difficulty = settings["Adaptive Difficulty"][1]
    multiplier = (difficulty - 1) / 10 + 1
    score = 0
    avg = difficulty**0.5 * 10
    cols, rows = findBestGrid()
    avg = int(avg // 2)
    button_width = (settings["Width"] - buffer[0]) // cols
    button_height = (settings["Height"] - buffer[1]) // rows
    button_side = int(min(button_width, button_height)) - 1
    radius = int(button_side * 0.3)
    margin_width, margin_height = (
        (settings["Width"] - (button_side * cols)) // 4,
        (settings["Height"] - (button_side * rows)) // 2,
    )
    makePickerButtons(settings, font)
    buttons = []
    y = margin_height
    for row in range(rows):
        x = margin_width
        button_row = []
        for col in range(cols):
            button = {
                "Pygame Button": pygame.Rect(x, y, button_side, button_side),
            }
            button_row.append(button)
            x += button_side
        y += button_side
        buttons.append(button_row)
    rounds = 3
    for i in range(rounds):
        score, adjustment, meta = cycle(i, settings, getFps, screen, font, exit)
        if score is None:
            return (score, adjustment, meta)
    adjustment = ((score / rounds) - (540 * multiplier)) / 100
    return (score, adjustment, meta)


def cycle(round_number, settings, getFps, screen, font, exit):
    global answer, pattern, picker_shape, picker_colour
    round_text = font.render(
        f"Round {round_number + 1}",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    all_positions = [(r, c) for r in range(rows) for c in range(cols)]
    num_shapes = avg + random.randint(-1, 1)
    # num_shapes = avg
    missing = rows * cols - num_shapes
    max_score = 100 / (num_shapes + missing * 0.05)
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
        # button = buttons[r][c]
        # button["Shape"] = random.choice(["Circle", "Square", "Triangle"])
        # button["Colour"] = random.choice(
        #     [
        #         settings["Game Primary Colour"],
        #         settings["Game Secondary Colour"],
        #         settings["Game Tertiary Colour"],
        #     ]
        # )
        # pattern[(r,c)] = {"Colour": button["Colour"], "Shape": button["Shape"]}

    # --- Game States ---
    # 'memorize' : pattern is visible for 10 seconds
    # 'replicate': pattern is hidden and the player clicks buttons to reproduce it
    # 'result'   : display the outcome
    ready = False
    while not ready:
        screen.fill(settings["Background Colour"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                return None, None, "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None, "Game Menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if ready_button["Pygame Button"].collidepoint(event.pos):
                    if ready_button["Meta"] == "Ready":
                        ready = True

            # if state == "replicate":
            #     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #         pos = pygame.mouse.get_pos()
            #         # Check which button (if any) was clicked.
            #         for r in range(rows):
            #             for c in range(cols):
            #                 btn = buttons[r][c]
            #                 if (
            #                     btn["Pygame Button"].collidepoint(pos)
            #                     and (r, c) not in player_selection
            #                 ):
            #                     # Mark the player's selection by changing its colour to Game Secondary Colour.
            #                     btn["Colour"] = settings["Game Secondary Colour"]
            #                     player_selection.append((r, c))

            #                     # When the player has selected enough buttons, check if they match the pattern.
            #                     if len(player_selection) == len(pattern):
            #                         # For this example, the order does not matter.
            #                         if sorted(player_selection) == sorted(pattern):
            #                             result_message = "Success!"
            #                         else:
            #                             result_message = "Failure!"
            #                         state = "result"

        drawGrid(screen, settings, margin_width * 2, pattern, True)
        height = settings["Height"] // 200
        pygame.draw.rect(screen, ready_button["Colour"], ready_button["Pygame Button"])
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
        ready_text = font.render(
            ready_button["Text"],
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
    # while remaining_time > 0:
    #     screen.fill(settings["Background Colour"])
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             exit()
    #             return None, None, "Quit"
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 return None, None, "Game Menu"
    #     current = pygame.time.get_ticks()
    #     remaining_time = int((pause_duration - (current - start)) / 100) / 10
    #     time_text = font.render(
    #         f"Time: {remaining_time}s",
    #         settings["Antialiasing Text"],
    #         settings["Background Font Colour"],
    #     )
    #     screen.blit(
    #         time_text,
    #         (
    #             (settings["Width"] - time_text.get_width()) // 2,
    #             (settings["Height"] - time_text.get_height()) // 2,
    #         ),
    #     )
    #     height = settings["Height"] // 200
    #     for line in return_text:
    #         text = font.render(
    #             line,
    #             settings["Antialiasing Text"],
    #             settings["Background Font Colour"],
    #         )
    #         screen.blit(
    #             text,
    #             (
    #                 settings["Width"] * 7 // 8
    #                 - text.get_width() // 2
    #                 - settings["Width"] // 200,
    #                 height,
    #             ),
    #         )
    #         height += text.get_height()
    #     screen.blit(
    #         round_text,
    #         (
    #             (settings["Width"] - round_text.get_width()) // 2,
    #             settings["Height"] // 200,
    #         ),
    #     )
    #     score_text = font.render(
    #         f"Score: {int(score)}",
    #         settings["Antialiasing Text"],
    #         settings["Background Font Colour"],
    #     )
    #     screen.blit(
    #         score_text,
    #         (
    #             (settings["Width"] - score_text.get_width()) // 2,
    #             settings["Height"] // 200 + round_text.get_height(),
    #         ),
    #     )
    #     getFps()
    #     pygame.display.flip()
    picker_shape = "Circle"
    picker_colour = settings["Game Primary Colour"]
    guess = {}
    remove = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                return None, None, "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None, "Game Menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in picker_buttons:
                    if button["Pygame Button"].collidepoint(event.pos):
                        meta = button["Meta"]
                        if meta in ["Triangle", "Circle", "Square"]:
                            picker_shape = meta
                        elif meta in [
                            "Game Primary Colour",
                            "Game Secondary Colour",
                            "Game Tertiary Colour",
                        ]:
                            picker_colour = settings[meta]
                        elif meta == "Erase":
                            remove = not remove
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
        score_text = font.render(
            f"Score: {int(score)}",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
        screen.blit(
            score_text,
            (
                (settings["Width"] - score_text.get_width()) // 2,
                settings["Height"] // 200,
            ),
        )
        round_text = font.render(
            f"Round {round_number + 1}",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
        screen.blit(
            round_text,
            (
                (settings["Width"] - round_text.get_width()) // 2,
                settings["Height"] // 200 + score_text.get_height(),
            ),
        )

        getFps()
        pygame.display.flip()
        if round_number == -1:
            break

        # state = 'memorize'
        # memorize_duration = 10 * 1000  # 10 seconds (in milliseconds)
        # memorize_start_time = pygame.time.get_ticks()

        # Player's clicks will be stored here (as (row, col) tuples)
        # player_selection = []
        # result_message = ""

        # running = True
        # while running:
        # dt = clock.tick(60)  # Limit to 60 FPS

        # --- State Transitions ---
        # if state == "memorize":
        #     # After 10 seconds, hide the pattern by resetting all buttons to Button Primary Colour.
        #     current_time = pygame.time.get_ticks()
        #     if current_time - memorize_start_time >= memorize_duration:
        #         for r in range(rows):
        #             for c in range(cols):
        #                 buttons[r][c]["Colour"] = settings["Button Primary Colour"]
        #         state = "replicate"

        # # --- Drawing ---
        # screen.fill(settings["Background Colour"])

        # # Draw all buttons on the grid.
        # for row in buttons:
        #     for btn in row:
        #         draw_button(screen, btn, font)

        # # Display text based on the current state.
        # if state == "memorize":
        #     remaining_time = max(
        #         0,
        #         (memorize_duration - (pygame.time.get_ticks() - memorize_start_time))
        #         // 1000,
        #     )
        #     timer_text = font.render(
        #         f"Memorize: {remaining_time}",
        #         settings["Antialiasing Text"],
        #         settings["Background Font Colour"],
        #     )
        #     screen.blit(
        #         timer_text,
        #         (
        #             settings["Width"] // 2 - timer_text.get_width() // 2,
        #             settings["Height"] - timer_text.get_height() - 20,
        #         ),
        #     )
        # elif state == "replicate":
        #     instruct_text = font.render(
        #         "Replicate the pattern by clicking the buttons",
        #         settings["Antialiasing Text"],
        #         settings["Background Font Colour"],
        #     )
        #     screen.blit(
        #         instruct_text,
        #         (
        #             settings["Width"] // 2 - instruct_text.get_width() // 2,
        #             settings["Height"] - instruct_text.get_height() - 20,
        #         ),
        #     )
        # elif state == "result":
        #     result_text = font.render(
        #         result_message,
        #         settings["Antialiasing Text"],
        #         settings["Background Font Colour"],
        #     )
        #     screen.blit(
        #         result_text,
        #         (
        #             settings["Width"] // 2 - result_text.get_width() // 2,
        #             settings["Height"] - result_text.get_height() - 20,
        #         ),
        #     )

        # getFps()
        # pygame.display.flip()
    # common = answer & guess  # Elements in both sets
    # missing = answer - guess  # Elements in pattern but not in guess
    # extra = guess - answer  # Elements in guess but not in pattern

    # print(f"Common elements: {len(common)} -> {common}")
    # print(f"Missing elements: {len(missing)} -> {missing}")
    # print(f"Extra elements: {len(extra)} -> {extra}")


# while True:
#     Example usage:
#     Assuming you have already called pygame.init() and set up your display:
#     screen = pygame.display.set_mode((settings["Width"], settings["Height"]))
#     game_loop(screen)

#     remaining_time = 30 - (current_frame - start) / 1000
#     if remaining_time >= 10:
#         remaining_time = int(remaining_time)
#     elif remaining_time >= 0:
#         remaining_time = math.trunc(remaining_time * 10) / 10
#     # else:
#     #     remaining_time = math.trunc(remaining_time * 100) / 100
#     time_text = font.render(
#         f"Time: {remaining_time}s",
#         settings["Antialiasing Text"],
#         settings["Background Font Colour"],
#     )
#     screen.blit(
#         time_text,
#         (
#             (settings["Width"] - time_text.get_width()) // 2,
#             settings["Height"] // 200 + score_text.get_height(),
#         ),
#     )

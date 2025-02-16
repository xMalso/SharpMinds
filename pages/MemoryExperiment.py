global random, pygame
import random, pygame


def init(settings, small_font, font):
    makeButtons(settings, small_font, font)


def makeButtons(settings, small_font, font):
    # global buttons
    # text = small_font.size("Back to Main Menu")
    global ready_button
    ready_text = font.size("Ready")
    # buttons = [
    # {
    #     "Text": "Back to Main Menu",
    #     "Pygame Button": pygame.Rect(
    #         settings["Width"] // 94,
    #         settings["Height"] // 16,
    #         text[0] + settings["Width"] // 64,
    #         text[1] + settings["Height"] // 90,
    #     ),
    #     "Colour": settings["Button Quinary Colour"],
    #     "Font Colour": settings["Font Quinary Colour"],
    #     "Meta": "Main Menu",
    # },

    # {
    ready_button = {
        "Text": "Ready",
        "Pygame Button": pygame.Rect(
            settings["Width"] // 2 - (ready_text[0] + settings["Width"] // 64) // 2,
            int(settings["Height"] * 0.9)
            - (ready_text[1] + settings["Height"] // 90) // 2,
            ready_text[0] + settings["Width"] // 64,
            ready_text[1] + settings["Height"] // 90,
        ),
        "Colour": settings["Button Primary Colour"],
        "Font Colour": settings["Font Primary Colour"],
        "Meta": "Ready",
    }


def findBestGrid():
    target = avg
    target = round(target)

    best_diff = target
    best_pair = (None, None)
    for i in range(1, target + 1):
        for j in range(i, min(target + 1, i + 6)):
            product = i * j
            diff = abs(product - target)
            if diff < best_diff:
                best_diff = diff
                best_pair = (i, j)
            elif diff == best_diff:
                if abs(i - j) < abs(best_pair[0] - best_pair[1]):
                    best_pair = (i, j)
        if best_pair[0] < best_pair[1]:
            best_pair = (best_pair[1], best_pair[0])
    return best_pair


def draw_grid(screen, settings):
    draw_empty_grid(screen, settings)
    for loc in pattern:
        r, c = loc
        button = buttons[r][c]
        if button["Shape"] == "Circle":
            pygame.draw.circle(screen, button["Colour"], button["rect"].center, radius)
        elif button["Shape"] == "Square":
            pygame.draw.rect(screen, settings["Grid Background Colour"], button["rect"])
            pygame.draw.rect(
                screen,
                button["Colour"],
                (
                    button["rect"].centerx - radius,
                    button["rect"].centery - radius,
                    radius * 2,
                    radius * 2,
                ),
            )
        else:
            side_length = min(button["rect"].width, button["rect"].height)
            height = (side_length * (3**0.5)) / 2
            points = [
                (button["rect"].centerx, button["rect"].centery - height / 2),
                (
                    button["rect"].centerx - side_length / 2,
                    button["rect"].centery + height / 2,
                ),
                (
                    button["rect"].centerx + side_length / 2,
                    button["rect"].centery + height / 2,
                ),
            ]
            pygame.draw.polygon(screen, button["Colour"], points)


def draw_empty_grid(screen, settings):
    for row in range(rows + 1):
        pygame.draw.line(
            screen,
            settings["Grid Line Colour"],
            (margin_width, row * (button_side + 1) + margin_height + 1),
            (1 - margin_width, row * (button_side + 1) + margin_height + 1),
        )
    for col in range(cols + 1):
        pygame.draw.line(
            screen,
            settings["Grid Line Colour"],
            (col * (button_side + 1) + margin_width + 1, margin_height),
            (col * (button_side + 1) + margin_width + 1, 1 - margin_height),
        )


def split_text(font, max_width):
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
    pause_duration = 10000
    multiplier = (difficulty - 1) / 10 + 1
    score = 0
    return_text = split_text(font, settings["Width"] // 4)
    avg = difficulty**0.5 * 10
    cols, rows = findBestGrid()
    avg = int(avg // 2)
    button_width = (settings["Width"] * 0.8 + 1) // cols - 1
    button_height = (settings["Height"] * 0.8 + 1) // rows - 1
    button_side = min(button_width, button_height)
    radius = int(min(button_side, button_side) * 0.45)
    margin_width, margin_height = (1 - (button_side * cols)) // 2, (
        1 - (settings["Height"] * cols)
    ) // 2
    button_margin = settings["Width"] // 100, settings["Height"] // 100
    shape_size = button_side - button_margin[0], button_side - button_margin[1]
    buttons = []
    for row in range(rows):
        button_row = []
        for col in range(cols):
            x = margin_width + col * (button_side)
            y = margin_height + row * (button_side)
            button = {
                "rect": pygame.Rect(x, y, *shape_size),
            }
            button_row.append(button)
            buttons.append(button_row)
    rounds = 3
    for i in range(rounds):
        score, adjustment, meta = cycle(i, settings, getFps, screen, font, exit)
        if score is None:
            return (score, adjustment, meta)
    adjustment = ((score / rounds) - (540 * multiplier)) / 100
    return (score, adjustment, meta)


def cycle(round_number, settings, getFps, screen, font, exit):
    global pattern
    round_text = font.render(
        f"Round {round_number + 1}",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    all_positions = [(r, c) for r in range(rows) for c in range(cols)]
    num_shapes = avg + random.randint(-2, 2)
    random.shuffle(all_positions)
    pattern = set(all_positions[:num_shapes])
    for r, c in pattern:
        button = buttons[r][c]
        button["Shape"] = random.choice(["Circle", "Square", "Triangle"])
        button["Colour"] = random.choice(
            [
                settings["Game Primary Colour"],
                settings["Game Secondary Colour"],
                settings["Game Tertiary Colour"],
            ]
        )
    # not_pattern = all_positions[num_shapes:]
    # for (r, c) in not_pattern:
    #     buttons[r][c]['Colour'] = settings["Grid Background Colour"]

    # --- Game States ---
    # 'memorize' : pattern is visible for 10 seconds
    # 'replicate': pattern is hidden and the player clicks buttons to reproduce it
    # 'result'   : display the outcome
    ready = False
    while not ready:
        screen.fill(settings["Background Colour"])
        # for button in buttons:
        #     pygame.draw.rect(screen,
        #         button["Colour"],
        #         button["Pygame Button"]
        #         )
        pygame.draw.rect(screen, ready_button["Colour"], ready_button["Pygame Button"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                return None, None, "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None, "Game Menu"
            # Only allow clicking during the replication phase.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # for button in buttons:
                #     if button["Pygame Button"].collidepoint(event.pos):
                #         meta = button["Meta"]
                #         if meta == "Ready":
                #             ready = True
                if ready_button["Pygame Button"].collidepoint(event.pos):
                    if ready_button["Meta"] == "Ready":
                        ready = True
                        # elif meta == "Main Menu":
                        #     return None, None, "Main Menu"

            # if state == "replicate":
            #     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #         pos = pygame.mouse.get_pos()
            #         # Check which button (if any) was clicked.
            #         for r in range(rows):
            #             for c in range(cols):
            #                 btn = buttons[r][c]
            #                 if (
            #                     btn["rect"].collidepoint(pos)
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

        draw_grid(screen, settings)
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
    current = start = pygame.time.get_ticks()
    remaining_time = int((pause_duration - (current - start)) / 100) / 10
    while remaining_time > 0:
        screen.fill(settings["Background Colour"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                return None, None, "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None, "Game Menu"
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
    while True:
        screen.fill(settings["Background Colour"])
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
    common = pattern & guess  # Elements in both sets
    missing = pattern - guess  # Elements in pattern but not in guess
    extra = guess - pattern  # Elements in guess but not in pattern

    print(f"Common elements: {len(common)} -> {common}")
    print(f"Missing elements: {len(missing)} -> {missing}")
    print(f"Extra elements: {len(extra)} -> {extra}")


# Example usage:
# Assuming you have already called pygame.init() and set up your display:
# screen = pygame.display.set_mode((settings["Width"], settings["Height"]))
# game_loop(screen)

# remaining_time = 30 - (current_frame - start) / 1000
# if remaining_time >= 10:
#     remaining_time = int(remaining_time)
# elif remaining_time >= 0:
#     remaining_time = math.trunc(remaining_time * 10) / 10
# # else:
# #     remaining_time = math.trunc(remaining_time * 100) / 100
# time_text = font.render(
#     f"Time: {remaining_time}s",
#     settings["Antialiasing Text"],
#     settings["Background Font Colour"],
# )
# screen.blit(
#     time_text,
#     (
#         (settings["Width"] - time_text.get_width()) // 2,
#         settings["Height"] // 200 + score_text.get_height(),
#     ),
# )

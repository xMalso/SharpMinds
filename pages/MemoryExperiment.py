import random, math
global rounds
rounds = 0


def init(settings):
    pass


def findBestGrid():
    target = 15 * difficulty**0.5
    target = int(round(target))

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


def draw_grid(pygame, screen, settings):
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
    for button in patterns:
        if button["Shape"] == "circle":
            pygame.draw.circle(screen, button['Colour'], button['rect'].center,
                               radius)
        elif button["Shape"] == "square":
            pygame.draw.rect(screen, settings["Grid Background Colour"],
                             button['rect'])
            pygame.draw.rect(screen, button['Colour'],
                             (button['rect'].centerx - radius,
                              button['rect'].centery - radius), radius * 2)
        else:
            side_length = min(button["rect"].width, button["rect"].height)
            height = (side_length * (3**0.5)) / 2
            points = [(button["rect"].centerx,
                       button["rect"].centery - height / 2),
                      (button["rect"].centerx - side_length / 2,
                       button["rect"].centery + height / 2),
                      (button["rect"].centerx + side_length / 2,
                       button["rect"].centery + height / 2)]
            pygame.draw.polygon(screen, button["colour"], points)

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

def Game2(pygame, sys, settings, screen, font, getFps):
    global difficulty, buttons, rows, cols, button_side, radius, margin_width, margin_height, score, return_text
    score = 0
    return_text = split_text(font, settings["Width"] // 4)
    difficulty = settings["Adaptive Difficulty"][1]
    cols, rows = findBestGrid()
    button_width = (settings["Width"] * .8 + 1) // cols - 1
    button_height = (settings["Height"] * .8 + 1) // rows - 1
    button_side = min(button_width, button_height)
    radius = min(button_side, button_side) * .45
    margin_width, margin_height = (1 - (button_side * cols)) // 2, (
        1 - (settings["Height"] * cols)) // 2
    button_margin = settings["Width"] // 100, settings["Height"] // 100
    shape_size = button_side - button_margin[0], button_side - button_margin[1]
    buttons = []
    for row in range(rows):
        button_row = []
        for col in range(cols):
            x = margin_width + col * (button_side)
            y = margin_height + row * (button_side)
            button = {
                'rect': pygame.Rect(x, y, shape_size),
            }
            button_row.append(button)
            buttons.append(button_row)
    for round in range(rounds):
        round(settings, getFps, screen, sys, pygame, font)


def round(settings, getFps, screen, sys, pygame, font):
    global patterns
    for row in buttons:
        for button in row:
            button["Shape"] = random.choice(["circle", "square", "triangle"])
            button['Colour'] = random.choice([
                settings["Game Primary Colour"],
                settings["Game Secondary Colour"],
                settings["Game Tertiary Colour"]
            ])
    all_positions = [(r, c) for r in range(rows) for c in range(cols)]
    num_shapes = int(difficulty**0.5 * 7.5) + random.randint(-2, 2)
    random.shuffle(all_positions)
    pattern = all_positions[:num_shapes]
    ready = False
    while not ready:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return None, None, "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None, "Game Menu"


        screen.fill(settings["Background Colour"])
        draw_grid(pygame, screen, settings)
        for line in return_text:
            text = font.render(
                line,
                settings["Antialiasing Text"],
                settings["Background Font Colour"],
            )
            screen.blit(
                text,
                (
                    settings["Width"] * 7 // 8 - text.get_width() // 2 -
                    settings["Width"] // 200,
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
        

        getFps()
        pygame.display.flip()



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
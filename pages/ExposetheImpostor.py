import math, random


def overlap(new_x, new_y):
    for x, y, _, _ in circles:
        if math.dist((new_x, new_y), (x, y)) < 2 * radius:
            return True
    return False


def removeCircle(pos, current):
    global circles, max_score
    for i, (x, y, colour, tick) in enumerate(circles):
        if math.dist(pos, (x, y)) < radius:
            circles.pop(i)
            if colour == "Green":
                return -50
            else:
                score = (
                    max_score
                    * min((0.012 * (despawn_time * 5 / (current - tick))) - 0.06, 1)
                    ** 0.2
                )
                return score
    return 0


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


def Game1(pygame, settings, screen, font):
    global radius, circles, despawn_time, max_score
    difficulty = settings["Adaptive Difficulty"][0]
    return_text = split_text(font, settings["Width"] // 4)
    circle_colour = {
        "Green": settings["Game Primary Colour"],
        "Red": settings["Game Secondary Colour"],
    }
    radius = int(settings["Width"] // (40 * difficulty**0.15))
    max_score = 30/difficulty**0.65
    height = max(font.size(str(char))[1] for char in "0123456789")
    score = 0
    red_count = 0
    circles = []
    last_tick = 0
    frame = 0
    i = 1
    text_surface = None
    start = current_frame = pygame.time.get_ticks()
    despawn_time = 9000 / (difficulty**0.15)
    spawn_gap = 800 / (difficulty**0.7)
    coords = random.randint(
        settings["Width"] // 100 + radius * 2,
        (settings["Width"] * 99) // 100 - radius * 2,
    ), random.randint(
        settings["Height"] // 100 + height + radius * 2,
        (settings["Height"] * 99) // 100 - radius * 2,
    )
    if not overlap(*coords):
        colour = random.randint(0, 1)
        if colour == 0:
            colour = "Green"
        else:
            colour = "Red"
            red_count += 1
        circles.append(coords + (colour, current_frame))
        last_tick = current_frame
    while start + 30000 > current_frame:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                score = max(removeCircle(event.pos, current_frame) + score, 0)
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None, "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None, "Games Menu"
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
        text = font.render(
            f"Score: {int(score)}",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
        screen.blit(
            text,
            (
                (settings["Width"] - text.get_width()) // 2,
                settings["Height"] // 200,
            ),
        )
        if current_frame - last_tick > spawn_gap:
            coords = random.randint(
                settings["Width"] // 100 + radius * 2,
                (settings["Width"] * 99) // 100 - radius * 2,
            ), random.randint(
                settings["Height"] // 100 + height + radius * 2,
                (settings["Height"] * 99) // 100 - radius * 2,
            )
            if not overlap(*coords):
                colour = random.randint(0, 1)
                if colour == 0:
                    colour = "Green"
                else:
                    colour = "Red"
                circles.append(coords + (colour, current_frame))
                last_tick = current_frame
        expired = True
        circle_number = 0
        while circle_number < len(circles):
            x, y, colour, tick = circles[circle_number]
            if expired:
                if current_frame - tick > despawn_time:
                    circles.pop(0)
                    if colour == "Green":
                        score += 5
                    else:
                        score = max(0, score - 10)
                    continue
                else:
                    expired = False
            circle_number += 1
            pygame.draw.circle(screen, circle_colour[colour], (x, y), radius)
        if (pygame.time.get_ticks() - frame) > 100:
            fps = 1 / (pygame.time.get_ticks() - frame) * i * 1000
            if settings["Show FPS"] == True:
                text_surface = font.render(
                    f"FPS: {fps:.2f}",
                    settings["Antialiasing Text"],
                    settings["Background Font Colour"],
                )
                screen.blit(text_surface, (0, 0))
            frame = pygame.time.get_ticks()
            i = 1
        else:
            i += 1
            if text_surface and settings["Show FPS"]:
                screen.blit(text_surface, (0, 0))
        pygame.display.flip()
        current_frame = pygame.time.get_ticks()
    red_count = max(1, red_count)
    adjustment = score - 0.8*red_count*max_score
    # adjustment *= 10
    return score, adjustment, "Game 1 Over"

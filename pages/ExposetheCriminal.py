global pygame, math, random, correct_sound, wrong_sound
import pygame, math, random

pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=512)
pygame.mixer.init()
correct_sound = pygame.mixer.Sound("assets/sounds/correct.wav")
wrong_sound = pygame.mixer.Sound("assets/sounds/wrong.wav")
correct_sound.set_volume(1.2)

def init(settings, font):
    makeButtons(settings, font)


def makeButtons(settings, font):
    global tutorial_button
    text = font.size("Start")
    # tutorial_button = [{
    tutorial_button = {
        "Text": "Start",
        "Pygame Button": pygame.Rect(
            (settings["Width"] - text[0]) // 2,
            (settings["Height"] * 95) // 100 - text[1],
            text[0] + settings["Width"] // 100,
            text[1] + settings["Height"] // 100,
        ),
        "Colour": settings["Button Primary Colour"],
        "Font Colour": settings["Font Primary Colour"],
    }
    # ]


def overlap(new_x, new_y):
    for x, y, _, _ in circles:
        if math.dist((new_x, new_y), (x, y)) < 2 * radius:
            return True
    return False


def removeCircle(pos, current):
    global circles, max_score, red_score, loss
    for i, (x, y, colour, tick) in enumerate(circles):
        if math.dist(pos, (x, y)) < radius:
            circles.pop(i)
            if colour == "Green":
                wrong_sound.play()
                loss += 50
                return -50
            else:
                correct_sound.play()
                time = current - tick if current - tick != 0 else 1
                score = (
                    max_score
                    * min((0.012 * (despawn_time * 5 / (time))) - 0.06, 1) ** 0.2
                )
                red_score += score
                return score
    return 0


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


def tutorial(screen, settings, font, getFps, exit):
    never = True
    while True:
        screen.fill(settings["Background Colour"])
        pygame.draw.rect(
            screen,
            tutorial_button["Colour"],
            tutorial_button["Pygame Button"],
            border_radius=settings["Width"] // 60,
        )
        text = font.render(
            tutorial_button["Text"],
            settings["Antialiasing Text"],
            tutorial_button["Font Colour"],
        )
        screen.blit(
            text,
            (
                tutorial_button["Pygame Button"].centerx - text.get_width() // 2,
                tutorial_button["Pygame Button"].centery - text.get_height() // 2,
            ),
        )
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if tutorial_button["Pygame Button"].collidepoint(event.pos):
                    return "Ready"
            elif event.type == pygame.QUIT:
                exit()
                return "Quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Game Menu"
        getFps(never)
        never = False
        pygame.display.flip()


def game1(settings, screen, font, getFps, exit, getID, updateLB):
    global radius, circles, despawn_time, max_score, loss, red_score
    red_score = 0
    loss = 0
    val = getID()
    never = True
    difficulty = settings["Adaptive Difficulty"][0]
    return_text = splitText(font, settings["Width"] // 4)
    circle_colour = {
        "Green": settings["Game Primary Colour"],
        "Red": settings["Game Secondary Colour"],
    }
    radius = int(settings["Width"] // (40 * difficulty**0.15))
    max_score = 30 / difficulty**0.65 * ((difficulty - 1) / 10 + 1)
    height = max(font.size(str(char))[1] for char in "0123456789")
    score = 0
    red_count = 0
    green_count = 0
    circles = []
    last_tick = 0
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
    duration = 30000
    while start + duration > current_frame:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                score += removeCircle(event.pos, current_frame)
                if score < 0:
                    loss += score
                    score = 0
            elif event.type == pygame.QUIT:
                exit()
                return None, None, "Quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None, "Game Menu"
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
        remaining_time = (duration - (current_frame - start)) / 1000
        if remaining_time >= 10:
            remaining_time = int(remaining_time)
        else:
            remaining_time = int(remaining_time * 10) / 10
        time_text = font.render(
            f"Time: {remaining_time}s",
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
        screen.blit(
            time_text,
            (
                (settings["Width"] - time_text.get_width()) // 2,
                settings["Height"] // 200 + score_text.get_height(),
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
                    red_count += 1
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
                        score += max_score / 6
                        green_count += 1
                    else:
                        penalty = max_score / 3
                        score -= penalty
                        loss += penalty
                        if score < 0:
                            loss += score
                            score = 0
                        wrong_sound.play()
                    continue
                else:
                    expired = False
            circle_number += 1
            pygame.draw.circle(screen, circle_colour[colour], (x, y), radius)
        getFps(never)
        never = False
        pygame.display.flip()
        current_frame = pygame.time.get_ticks()
    adjustment = score - (0.8 * red_count + green_count / 6) * max_score
    adjustment /= 100
    lb = {'loss': loss, 'green': green_count, 'red': red_score, 'game': 2, 'id': val[0], 'username': val[1], 'score': score, 'max': max_score}
    updateLB(1, lb)
    return score, adjustment, "Game Over"

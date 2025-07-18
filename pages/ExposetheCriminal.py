global first_attempt, sounds
import pygame, math, random, logging, threading

sounds = False
first_attempt = True

logging.basicConfig(
    level=logging.WARNING,
    filename="latestlog.txt",
    filemode="w",
    format="%(filename)s:%(lineno)d | %(asctime)s - %(message)s",
)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)


def loadSounds():
    global correct_sound, wrong_sound, sounds, attempting, first_attempt
    attempting = True
    try:
        pygame.mixer.pre_init(frequency=22050, channels=1)
        pygame.mixer.init()
        correct_sound = pygame.mixer.Sound("assets/sounds/correct.wav")
        wrong_sound = pygame.mixer.Sound("assets/sounds/wrong.wav")
        sounds = True
        correct_sound.set_volume(1.2)
    except pygame.error as e:
        if first_attempt:
            logging.warning(
                f"Sounds failed to load, most likely due to lack of audio output: {e}"
            )
            first_attempt = False
    attempting = False


def init(settings, font, small_font, splitText):
    global tutorial_text, text_height, return_text
    text_height = max(font.size(str(char))[1] for char in "0123456789")
    makeButtons(settings, font, small_font)
    tutorial_text = makeTutText(
        font,
        int(settings["Width"] * 0.85),
        "Click these circles SECONDARY and avoid clicking these circles PRIMARY or the background, you gain more points when clicking these circles SECONDARY in a shorter space of time and you gain points when these circles PRIMARY despawn",
    )
    return_text = splitText(
        font,
        settings["Width"] // 4,
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    #
    #
    #
    #
    # TEMP WHILE I WORK ON SOUNDS
    #
    #
    loadSounds()
    # thread = threading.Thread(target=loadSounds, daemon=True)
    # thread.start()
    # thread.join(0.2)
    # if thread.is_alive():
    #     # thread.kill()
    #     pass


def makeTutText(font, max_width, text):
    lines = []
    current_line = ""
    curr_width = 0
    for word in text.split():
        if word == "PRIMARY" or word == "SECONDARY":
            word_width = font.size(" ")[0] + 100 if current_line else 100
            test_line = current_line + " " + word if current_line else word
        else:
            test_line = current_line + " " + word if current_line else word
            word_width = (
                font.size(word + " ")[0] if current_line else font.size(word)[0]
            )
        if curr_width + word_width <= max_width:
            current_line = test_line
            curr_width += word_width
        else:
            lines.append(current_line)
            current_line = word
            curr_width = word_width
    lines.append(current_line)
    return lines


def makeButtons(settings, font, small_font):
    global ready_button, tut_text_size, return_button
    tut_text_size = font.size("Start")
    text = small_font.size("Back to Game Menu")
    # tutorial_button = [{
    ready_button = {
        "Text": font.render(
            "Start", settings["Antialiasing Text"], settings["Font Primary Colour"]
        ),
        "Pygame Button": pygame.Rect(
            (settings["Width"] - tut_text_size[0]) // 2,
            (settings["Height"] * 95) // 100 - tut_text_size[1],
            tut_text_size[0] + settings["Width"] // 100,
            tut_text_size[1] + settings["Height"] // 100,
        ),
        "Colour": settings["Button Primary Colour"],
    }
    return_button = {
        "Text": small_font.render(
            "Back to Game Menu",
            settings["Antialiasing Text"],
            settings["Font Primary Colour"],
        ),
        "Pygame Button": pygame.Rect(
            settings["Width"] // 94,
            settings["Height"] // 16,
            text[0] + settings["Width"] // 64,
            text[1] + settings["Height"] // 90,
        ),
        "Colour": settings["Button Quinary Colour"],
    }

    # ]


def overlap(new_x, new_y):
    for x, y, _, _ in circles:
        if math.dist((new_x, new_y), (x, y)) < 2 * radius:
            return True
    return False


def spawnCircle():
    global last_tick, circles, red_count
    coords = random.randint(*spawn_width), random.randint(*spawn_height)
    while overlap(*coords):
        coords = random.randint(*spawn_width), random.randint(*spawn_height)
    colour = random.randint(0, 1)
    if colour == 0:
        colour = "Green"
    else:
        colour = "Red"
        red_count += 1
    circles.append(coords + (colour, current_frame))
    last_tick = current_frame


def removeCircle(pos, current):
    global circles, red_score, loss
    for i, (x, y, colour, tick) in enumerate(circles):
        if math.dist(pos, (x, y)) < radius:
            circles.pop(i)
            if colour == "Green":
                if sounds:
                    wrong_sound.play()
                loss += 50
                return (-50, (x + radius, y - radius))
            else:
                if sounds:
                    correct_sound.play()
                time = current - tick
                if time == 0:
                    time = 1
                if despawn_time < time:
                    score = 0
                else:
                    score = (
                        max_score
                        * min((0.012 * (despawn_time * 5 / (time))) - 0.06, 1) ** 0.2
                    )
                red_score += score
                return (score, (x + radius, y - radius))
    wrong_sound.play()
    loss += max_score
    return (-max_score, pos)


def tutorial(screen, settings, font, getFps, exitGame):
    never = True
    while True:
        # if not sounds and not attempting:
        # thread = threading.Thread(target=loadSounds, daemon=True)
        # thread.start()
        screen.fill(settings["Background Colour"])
        line_height = max(font.size(tutorial_text[0])[1], 100)
        y = (
            settings["Height"] * 0.95
            - tut_text_size[1]
            - (line_height * len(tutorial_text))
        ) // 2
        for line in tutorial_text:
            parts = []
            remaining = line
            while remaining:
                primary_pos = remaining.find("PRIMARY")
                secondary_pos = remaining.find("SECONDARY")

                if primary_pos == -1 and secondary_pos == -1:
                    parts.append(("text", remaining))
                    break

                if primary_pos == -1 or (
                    secondary_pos != -1 and secondary_pos < primary_pos
                ):
                    if secondary_pos != 0:
                        parts.append(("text", remaining[:secondary_pos]))
                    parts.append(("secondary", ""))
                    remaining = remaining[secondary_pos + 9 :]
                elif secondary_pos == -1 or (
                    primary_pos != -1 and primary_pos < secondary_pos
                ):
                    if primary_pos != 0:
                        parts.append(("text", remaining[:primary_pos]))
                    parts.append(("primary", ""))
                    remaining = remaining[primary_pos + 7 :]
            line_width = 0
            for type, text in parts:
                if type == "primary" or type == "secondary":
                    line_width += 100
                else:
                    line_width += font.size(text)[0]
            x = settings["Width"] // 2 - line_width // 2
            for type, line_text in parts:
                if type == "text":
                    text = font.render(
                        line_text,
                        settings["Antialiasing Text"],
                        settings["Background Font Colour"],
                    )
                    screen.blit(
                        text,
                        (
                            x,
                            y + (line_height - text.get_height()) // 2,
                        ),
                    )
                    x += text.get_width()
                elif type == "primary":
                    pygame.draw.circle(
                        screen,
                        settings["Game Primary Colour"],
                        (x + 50, y + line_height // 2),
                        50,
                    )
                    x += 100
                elif type == "secondary":
                    pygame.draw.circle(
                        screen,
                        settings["Game Secondary Colour"],
                        (x + 50, y + line_height // 2),
                        50,
                    )
                    x += 100
                else:
                    logging.warning(f"Unknown type: {type}, text: {text}")
            y += line_height
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
        pygame.draw.rect(
            screen,
            return_button["Colour"],
            return_button["Pygame Button"],
            border_radius=settings["Width"] // 40,
        )
        screen.blit(
            return_button["Text"],
            (
                return_button["Pygame Button"].centerx
                - return_button["Text"].get_width() // 2,
                return_button["Pygame Button"].centery
                - return_button["Text"].get_height() // 2,
            ),
        )
        pygame.draw.rect(
            screen,
            ready_button["Colour"],
            ready_button["Pygame Button"],
            border_radius=settings["Width"] // 60,
        )
        screen.blit(
            ready_button["Text"],
            (
                ready_button["Pygame Button"].centerx
                - ready_button["Text"].get_width() // 2,
                ready_button["Pygame Button"].centery
                - ready_button["Text"].get_height() // 2,
            ),
        )
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if ready_button["Pygame Button"].collidepoint(event.pos):
                    return "Ready"
                if return_button["Pygame Button"].collidepoint(event.pos):
                    return "Game Menu"
            elif event.type == pygame.QUIT:
                exitGame()
                return "Quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Game Menu"
        getFps(never)
        never = False
        pygame.display.flip()


def game1(settings, screen, font, getFps, exitGame, getID, updateLB):
    global radius, circles, despawn_time, max_score, loss, red_score, current_frame, spawn_width, spawn_height, red_count, last_tick
    m = tutorial(screen, settings, font, getFps, exitGame)
    if m == "Quit" or m == "Game Menu":
        return None, None, m, None
    del m
    visual_text = []
    red_score = 0
    loss = 0
    user_id, user_key, username = getID()
    never = True
    difficulty = settings["Adaptive Difficulty"][0]
    circle_colour = {
        "Green": settings["Game Primary Colour"],
        "Red": settings["Game Secondary Colour"],
    }
    radius = int(settings["Width"] // (40 * difficulty**0.15))
    spawn_width = (
        settings["Width"] // 100 + radius * 2,
        (settings["Width"] * 99) // 100 - radius * 2,
    )
    spawn_height = (
        settings["Height"] // 100 + text_height + radius * 2,
        (settings["Height"] * 99) // 100 - radius * 2,
    )
    max_score = 30 / difficulty**0.65 * (difficulty * 0.1 + 0.9)
    score = 0
    red_count = 0
    green_count = 0
    circles = []
    last_tick = 0
    start = current_frame = pygame.time.get_ticks()
    despawn_time = 9000 / (difficulty**0.15)
    spawn_gap = 800 / (difficulty**0.7)
    spawnCircle()
    duration = 30000
    score_text = font.render(
        "Score: 0",
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    score_text_coords = (
        (settings["Width"] - score_text.get_width()) // 2,
        settings["Height"] // 200,
    )
    while start + duration > current_frame:
        # if not sounds and not attempting:
        # thread = threading.Thread(target=loadSounds, daemon=True)
        # thread.start()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                result, edge = removeCircle(event.pos, current_frame)
                if result != 0:
                    score += result
                    visual_text.append(
                        (
                            font.render(
                                f"{result:+,.1f}",
                                settings["Antialiasing Text"],
                                settings["Background Font Colour"],
                            ),
                            edge,
                            current_frame,
                        )
                    )
                if score < 0:
                    loss += score
                    score = 0
                score_text = font.render(
                    f"Score: {int(score):,}",
                    settings["Antialiasing Text"],
                    settings["Background Font Colour"],
                )
                score_text_coords = (
                    (settings["Width"] - score_text.get_width()) // 2,
                    settings["Height"] // 200,
                )
            elif event.type == pygame.QUIT:
                exitGame()
                return None, None, "Quit", None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None, "Game Menu", None
        screen.fill(settings["Background Colour"])
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
            score_text_coords,
        )
        screen.blit(
            time_text,
            (
                (settings["Width"] - time_text.get_width()) // 2,
                settings["Height"] // 200 + score_text.get_height(),
            ),
        )
        if current_frame - last_tick > spawn_gap:
            spawnCircle()
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
                        if sounds:
                            wrong_sound.play()
                    score_text = font.render(
                        f"Score: {int(score):,}",
                        settings["Antialiasing Text"],
                        settings["Background Font Colour"],
                    )
                    score_text_coords = (
                        (settings["Width"] - score_text.get_width()) // 2,
                        settings["Height"] // 200,
                    )
                else:
                    expired = False
            else:
                circle_number += 1
                pygame.draw.circle(screen, circle_colour[colour], (x, y), radius)
        for visual_text_score, pos, tick in visual_text:
            if current_frame - tick > 1000:
                visual_text.pop(0)
            else:
                # visual_text_score = int(visual_text_score*10)/10
                screen.blit(
                    visual_text_score,
                    (
                        pos[0],
                        pos[1] - visual_text_score.get_height() // 2,
                    ),
                )
        getFps(never)
        never = False
        pygame.display.flip()
        current_frame = pygame.time.get_ticks()
    adjustment = score - (0.8 * red_count + green_count / 6) * max_score
    adjustment /= 100
    lb = {
        "loss": float(loss),
        "green": int(green_count),
        "red": float(red_score),
        "game": int(1),
        "id": str(user_id),
        "username": str(username),
        "score": float(score),
        "max": float(max_score),
    }
    pb = updateLB(1, lb)
    return score, adjustment, "Game Over", pb

import math, pygame, random, logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
spawns = 1
log_filename = f"logs/log{datetime.now().strftime('%d-%m_%Hh-%Mm-%Ss')}.txt"
handler = RotatingFileHandler(log_filename, maxBytes=5 * 1024**2, backupCount=10)
logging.basicConfig(
    level=logging.WARNING,
    handlers=[handler],
    format="%(filename)s:%(lineno)d | %(asctime)s - %(message)s",
)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)


def init(settings, font):
    global return_lines, colours
    colours = [
        settings["Game Primary Colour"],
        settings["Game Secondary Colour"],
        settings["Game Tertiary Colour"],
    ]
    lines = splitText(font, settings["Width"] // 4)
    return_lines = []
    for line in lines:
        return_lines.append(
            font.render(
                line, settings["Antialiasing Text"], settings["Background Font Colour"]
            )
        )


def splitText(font, max_width):
    words = ["Press", "ESC", "to", "return", "to", "games", "menu"]
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        text_width = font.size(test_line)[0]

        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    return lines


def generateInnerObjects(loc, trim):
    random.shuffle(loc)
    shuffloc = loc[:]
    for i in range(len(shuffloc)):
        shuffloc[i] = [
            shuffloc[i],
            random.choice(["Square", "Circle", "Triangle"]),
            random.choice([0, 1, 2]),
        ]
    shuffloc[0] = shuffloc[0][0], "Triangle", shuffloc[0][2]
    return shuffloc


def drawRect(screen, rotation, colour, big):
    x = big[0]
    y = big[1]
    rect = pygame.draw.polygon(
        screen,
        colour,
        [
            rotate_point(x + move_x / 2, y + move_y / 2, x, y, rotation)
            for move_x, move_y in [
                (-square_size, -square_size),
                (square_size, -square_size),
                (square_size, square_size),
                (-square_size, square_size),
            ]
        ],
    )
    logging.debug(f"returned big rect: {rect}")
    return rect


def generateObjects(settings, difficulty):
    global objects, shape_size, buffer, square_size  # buffer for moving the shapes too
    sqrt2 = math.sqrt(2)
    num_shapes = int((difficulty / 2) ** 2) + 1
    loc = [(x, y) for x in range(num_shapes) for y in range(num_shapes)]
    shape_size = (((settings["Width"] // 10.8) - 1) // num_shapes) - 1
    square_size = (shape_size + 1) * num_shapes + 1
    screen_size = (
        settings["Width"] * 0.9 - (square_size * sqrt2),
        settings["Height"] * 0.95
        - len(return_lines) * return_lines[0].get_height()
        - (square_size * sqrt2),
    )
    buffer = (
        settings["Width"] * 0.05 + (square_size / sqrt2),
        settings["Height"] * 0.025
        + len(return_lines) * return_lines[0].get_height()
        + (square_size / sqrt2),
    )
    spawn = []
    for x in range(int(buffer[0]), int(buffer[0] + screen_size[0]), 120):
        for y in range(int(buffer[1]), int(buffer[1] + screen_size[1]), 120):
            spawn.append((x, y))
    random.shuffle(spawn)
    spawn = spawn[:spawns]
    objects = []
    trim = (num_shapes**2) // 2.4
    for i in range(spawns):
        shuffloc = generateInnerObjects(loc, trim)
        duplicate = pair = i % 2 == 0
        while duplicate:
            for obj in objects[::2]:
                while obj["Inner Shapes"] == shuffloc:
                    shuffloc = generateInnerObjects(loc, trim)
            duplicate = False
            for obj in objects[::2]:
                if obj["Inner Shapes"] == shuffloc:
                    duplicate = True
                    break
        objects.append(
            {
                "Number": i,
                "Pair": i // 2,
                "Centre": (
                    spawn[i][0] + square_size / 2,
                    spawn[i][1] + square_size / 2,
                ),
                "Inner Shapes": [],
            }
        )
        if pair:
            for location in shuffloc:
                x, y = location[0]
                objects[-1]["Inner Shapes"].append(
                    (
                        [
                            (x + 0.5) * (shape_size + 1) + 1 + spawn[i][0],
                            (y + 0.5) * (shape_size + 1) + 1 + spawn[i][1],
                        ],
                        location[1],
                        colours[location[2]],
                    )
                )
        else:
            objects[-1]["Inner Shapes"] = objects[-2]["Inner Shapes"]


def game3(settings, screen, font, getFps, exit, getID, updateLB):
    logging.info(
        "Page 'Pattern Rush' is currently in development, sending back to main menu."
    )
    return None, None, "Game Menu", None

    user_id, user_key, username = getID()
    score_text = font.render(
        "Score: 0", settings["Antialiasing Text"], settings["Background Font Colour"]
    )
    score_text_coords = (
        (settings["Width"] - score_text.get_width()) // 2,
        settings["Height"] * 0.01,
    )
    score = 0
    never = True
    playing = True
    current = start = pygame.time.get_ticks()
    left = 3
    pairs = 0
    selected = []
    difficulty = settings["Adaptive Difficulty"][2]
    rotation_multiplier = 0.1 * difficulty**1.7
    duration = 20000 / difficulty**0.5
    multiplier = difficulty * 0.1 + 0.9
    generateObjects(settings, difficulty)
    time_left = current - start
    max = multiplier * 100
    lb = (
        {
            "duration": duration,
            "game": 3,
            "id": user_id,
            "username": username,
            "max": float(max),
        },
    )
    while time_left < duration and playing:
        rects = []
        rotation = math.radians(time_left * rotation_multiplier)
        screen.fill(settings["Background Colour"])
        for obj in objects:
            centre = obj["Centre"]
            rects.append(
                [
                    drawRect(
                        screen,
                        rotation,
                        settings["Grid Background Colour"],
                        centre,
                    ),
                    (obj["Number"], obj["Pair"]),
                ]
            )
            for shape in obj["Inner Shapes"]:
                drawSmallRect(screen, centre, rotation, shape[0], shape[1], shape[2])
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect in rects:
                    if rect[0].collidepoint(event.pos):
                        if rect[1] in selected:
                            selected.remove(rect[1])
                        else:
                            selected.append(rect[1])
                            while len(selected) > 2:
                                selected.pop(0)
                            if len(selected) == 2:
                                if selected[0][1] == selected[1][1]:
                                    score += left * max
                                    score_text = font.render(
                                        f"Score: {score:,}",
                                        settings["Antialiasing Text"],
                                        settings["Background Font Colour"],
                                    )
                                    score_text_coords = (
                                        (settings["Width"] - score_text.get_width())
                                        // 2,
                                        settings["Height"] * 0.01,
                                    )
                                    selected = []
                                    pairs += left
                                    left -= 1
                                    if left == 0:
                                        playing = False
                                        score += (max(time_left, 0) / 100) * multiplier
                                else:
                                    result = left * max / 2
                                    score -= result
                                    loss += result
                                    score_text = font.render(
                                        f"Score: {score:,}",
                                        settings["Antialiasing Text"],
                                        settings["Background Font Colour"],
                                    )
                                    score_text_coords = (
                                        (settings["Width"] - score_text.get_width())
                                        // 2,
                                        settings["Height"] * 0.01,
                                    )
                                    selected = []
            elif event.type == pygame.QUIT:
                exit()
                return None, None, "Quit", None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None, "Game Menu", None
        time_text = font.render(
            f"Time: {(time_left/1000):.1f}",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
        time_text_coords = (
            (settings["Width"] - time_text.get_width()) // 2,
            settings["Height"] * 0.01 + score_text.get_height(),
        )
        screen.blit(score_text, score_text_coords)
        screen.blit(time_text, time_text_coords)
        getFps(never)
        never = False
        pygame.display.flip()
    lb["time"] = duration - max(time_left, 0)
    lb["pairs"] = pairs
    lb["score"] = score
    adjustment = (score - max * 6 + duration / 400) / 200
    old_score = updateLB(3, lb)
    return score, adjustment, "Game Over", old_score


def rotate_point(x, y, centre_x, centre_y, rotation):
    difference_x, difference_y = x - centre_x, y - centre_y
    new_x = (
        centre_x + difference_x * math.cos(rotation) - difference_y * math.sin(rotation)
    )
    new_y = (
        centre_y + difference_x * math.sin(rotation) + difference_y * math.cos(rotation)
    )
    return new_x, new_y


def drawSmallRect(screen, centre, rotation, coords, shape, colour):
    x, y = coords
    centre_x, centre_y = centre
    if shape == "Square":
        corners = [
            (x - shape_size / 2, y - shape_size / 2),
            (x + shape_size / 2, y - shape_size / 2),
            (x - shape_size / 2, y + shape_size / 2),
            (x + shape_size / 2, y + shape_size / 2),
        ]
    elif shape == "Circle":
        pygame.draw.circle(
            screen,
            colour,
            rotate_point(centre_x, centre_y, x, y, rotation),
            shape_size / 2,
        )
        return
    elif shape == "Triangle":
        half_height = (math.sqrt(3) / 2) * shape_size / 2
        corners = [
            (x, y - half_height),
            (x - shape_size / 2, y + half_height),
            (x + shape_size / 2, y + half_height),
        ]
    else:
        logging.error(f"Invalid shape: {shape}")
    rotated_corners = []
    for cornerx, cornery in corners:
        rotated_corners.append(
            rotate_point(centre_x, centre_y, cornerx, cornery, rotation)
        )
    pygame.draw.polygon(screen, colour, rotated_corners)

    return

import math, pygame, random, logging
from datetime import datetime

spawns = 7
logging.basicConfig(
    level=logging.WARNING,
    filename = "latestlog.txt",
    filemode='w',
    format="%(filename)s:%(lineno)d | %(asctime)s - %(message)s",
)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)


def init(settings, font, small_font, splitText):
    global return_lines, colours, tutorial_text, gl_text
    colours = [
        settings["Game Primary Colour"],
        settings["Game Secondary Colour"],
        settings["Game Tertiary Colour"],
    ]
    return_lines = splitText(
        font,
        settings["Width"] // 4,
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
    )
    tutorial_text = splitText(
        font,
        (settings["Width"] * 3) // 4,
        settings["Antialiasing Text"],
        settings["Background Font Colour"],
        "In this game you must match the rotating grids with another grid that is the exact same. But act swiftly while maintaining precision, you get more points the faster you are and lose points for incorrect pairs.",
    )
    gl_text = font.render("Good Luck!", settings["Antialiasing Text"], settings["Background Font Colour"])
    makeButtons(settings, font, small_font)


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


def generateInnerObjects(loc, trim):
    # print("generating inner objects")
    random.shuffle(loc)
    shuffloc = loc[:trim]
    for i in range(trim):
        shuffloc[i] = [
            shuffloc[i],
            random.choice(["Square", "Circle", "Triangle"]),
            random.choice([0, 1, 2]),
        ]
    shuffloc[0] = shuffloc[0][0], "Triangle", shuffloc[0][2]
    return shuffloc


def drawRect(screen, rotation, colour, line_colour, big):
    x = big[0]
    y = big[1]
    points = [
        rotate_point(x + move_x / 2, y + move_y / 2, x, y, rotation)
        for move_x, move_y in [
            (-square_size, -square_size),
            (square_size, -square_size),
            (square_size, square_size),
            (-square_size, square_size),
        ]
    ]
    rect = pygame.draw.polygon(screen, colour, points)
    spacing = (square_size - shape_buffer * 2) / num_shapes
    for i in range(1, num_shapes):
        offset = i * spacing - square_size / 2
        pygame.draw.line(
            screen,
            line_colour,
            rotate_point(x + offset, y - square_size / 2, x, y, rotation),
            rotate_point(x + offset, y + square_size / 2, x, y, rotation),
        )
        pygame.draw.line(
            screen,
            line_colour,
            rotate_point(x - square_size / 2, y + offset, x, y, rotation),
            rotate_point(x + square_size / 2, y + offset, x, y, rotation),
        )
    logging.debug(f"returned big rect: {rect}")
    return rect


def generateObjects(settings, difficulty):
    global objects, shape_size, buffer, square_size, num_shapes, shape_buffer, spawns
    sqrt2 = math.sqrt(2)
    num_shapes = max(int(6 - 5 / (difficulty**0.3)), 1)
    trim = int(max(num_shapes**2 // 2, 1))
    if trim == 1:
        spawns = 5
    loc = [(x, y) for x in range(num_shapes) for y in range(num_shapes)]
    shape_size = (((settings["Width"] // 10) - 2) // num_shapes) - 2
    shape_buffer = shape_size // 25
    square_size = (shape_size + shape_buffer * 2) * num_shapes + shape_buffer * 2
    screen_size = (
        settings["Width"] * 0.9 - (square_size * sqrt2),
        settings["Height"] * 0.95
        - len(return_lines) * return_lines[0].get_height()
        - (square_size * sqrt2),
    )
    buffer = (
        settings["Width"] * 0.05,
        settings["Height"] * 0.025 + len(return_lines) * return_lines[0].get_height(),
    )
    spawn = []
    for x in range(
        int(buffer[0]), int(buffer[0] + screen_size[0]), int(square_size * sqrt2 + 20)
    ):
        for y in range(
            int(buffer[1]),
            int(buffer[1] + screen_size[1]),
            int(square_size * sqrt2 + 20),
        ):
            spawn.append((x, y))
    random.shuffle(spawn)
    spawn = spawn[:spawns]
    objects = []
    initial_spin_max = int(30 * difficulty**1.7)
    for i in range(spawns):
        shuffloc = generateInnerObjects(loc, trim)
        duplicate = pair = i % 2 == 0
        while duplicate:
            for obj in objects[::2]:
                while obj["Identifier"] == shuffloc:
                    shuffloc = generateInnerObjects(loc, trim)
            duplicate = False
            for obj in objects[::2]:
                if obj["Identifier"] == shuffloc:
                    duplicate = True
        objects.append(
            {
                "Number": i,
                "Pair": i // 2,
                "Centre": (
                    spawn[i][0] + square_size / 2,
                    spawn[i][1] + square_size / 2,
                ),
                "Inner Shapes": [],
                "Initial Spin": math.radians(
                    random.randint(-initial_spin_max, initial_spin_max)
                ),
                "Spin Multiplier": random.randint(700, 1300)
                / 1000
                * random.choice([-1, 1]),
                "Identifier": [],
                "Colour": settings["Grid Background Colour"],
                "Line Colour": settings["Grid Line Colour"],
            }
        )
        # print("shuffloc", shuffloc)
        if pair:
            for location in shuffloc:
                # print("location", location[0])
                x, y = location[0]
                objects[-1]["Inner Shapes"].append(
                    (
                        (
                            (x + 0.5) * (shape_size + shape_buffer * 2)
                            + shape_buffer
                            + spawn[i][0],
                            (y + 0.5) * (shape_size + shape_buffer * 2)
                            + shape_buffer
                            + spawn[i][1],
                        ),
                        (
                            location[0],
                            location[1],
                            colours[location[2]],
                        ),
                        location,
                    )
                )
            objects[-1]["Identifier"].append(objects[-1]["Inner Shapes"][0][2])
        else:
            diff_x, diff_y = (
                spawn[i][0] - spawn[i - 1][0],
                spawn[i][1] - spawn[i - 1][1],
            )
            for j in range(trim):
                original_shape = objects[-2]["Inner Shapes"][j]
                shape_coords = original_shape[0]
                original_details = original_shape[1]
                objects[-1]["Inner Shapes"].append(
                    (
                        (
                            (shape_coords[0] + diff_x),
                            (shape_coords[1] + diff_y),
                        ),
                        (
                            original_details[0],
                            original_details[1],
                            original_details[2],
                        ),
                        original_shape[2],
                    )
                )
    # for i in range(len(objects)):
    #     objectstring = f"Pair: {objects[i]['Pair']} "
    #     for j in range(len(objects[i]["Inner Shapes"])):
    #         objectstring += f'{objects[i]["Inner Shapes"][j][1]}'
    #     print(objectstring)
    return


def tutorial(screen, settings, font, getFps, exitGame):
    never = True
    while True:
        # if not sounds and not attempting:
        # thread = threading.Thread(target=loadSounds, daemon=True)
        # thread.start()
        screen.fill(settings["Background Colour"])
        line_height = tutorial_text[0].get_height()
        y = (
            settings["Height"] * 0.95
            - tut_text_size[1]
            - (line_height * len(tutorial_text))
        ) // 2
        for line in tutorial_text:
            screen.blit(
                line,
                (
                    (settings["Width"] - line.get_width()) // 2,
                    y,
                ),
            )
            y += line_height
        height = settings["Height"] // 200
        for line in return_lines:
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
        y += line_height
        screen.blit(gl_text, (settings["Width"] // 2 - gl_text.get_width() // 2, y))
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


def game3(settings, screen, font, getFps, exitGame, getID, updateLB):
    m = tutorial(screen, settings, font, getFps, exitGame)
    if m == "Quit" or m == "Game Menu":
        return None, None, m, None
    del m
    loss = 0
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
    pairs = 0
    selected = []
    difficulty = settings["Adaptive Difficulty"][2]
    rotation_multiplier = 0.012 * difficulty**0.6
    duration = 10000 / difficulty**0.2
    multiplier = difficulty * 0.1 + 0.9
    generateObjects(settings, difficulty)
    left = spawns // 2
    time_left = duration
    max_score = multiplier * 100
    lb = {
        "duration": duration,
        "game": 3,
        "id": user_id,
        "username": username,
        "max": float(max_score),
        "difficulty": difficulty,
    }
    while time_left > 0 and playing:
        current = pygame.time.get_ticks()
        time_left = duration - current + start
        # print("frame")
        rects = []
        init_rotation = math.radians(time_left * rotation_multiplier)
        screen.fill(settings["Background Colour"])
        for obj in objects:
            rotation = (init_rotation + obj["Initial Spin"]) * obj["Spin Multiplier"]
            centre = obj["Centre"]
            rects.append(
                [
                    drawRect(
                        screen,
                        rotation,
                        obj["Colour"],
                        obj["Line Colour"],
                        centre,
                    ),
                    (obj["Number"], obj["Pair"]),
                ]
            )
            # print(f"centre {centre} square size {square_size}")
            for shape in obj["Inner Shapes"]:
                # print(shape)
                drawSmallRect(
                    screen, centre, rotation, shape[0], shape[1][1], shape[1][2]
                )
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect in rects:
                    # print("rect", rect)
                    if rect[0].collidepoint(event.pos):
                        if rect[1] in selected:
                            for i in range(len(objects)):
                                if rects[i][1] in selected:
                                    objects[i]["Colour"] = settings[
                                        "Grid Background Colour"
                                    ]
                                    objects[i]["Line Colour"] = settings[
                                        "Grid Line Colour"
                                    ]
                                    break
                                if i == len(objects) - 1:
                                    logging.warning(
                                        f"Could not change colour of shape to original, rect[1]: {rects[i][1]}, i: {i}, selected: {selected} objects: {objects}"
                                    )
                            selected.remove(rect[1])
                        else:
                            selected.append(rect[1])
                            for i in range(len(objects)):
                                if rects[i][1] in selected:
                                    objects[i]["Colour"] = settings[
                                        "Grid Selected Colour"
                                    ]
                                    objects[i]["Line Colour"] = settings[
                                        "Grid Selected Line Colour"
                                    ]
                                    break
                                if i == len(objects) - 1:
                                    logging.warning(
                                        f"Could not change colour of shape to selected, rect[1]: {rects[i][1]}, i: {i}, selected: {selected} objects: {objects}"
                                    )

                            while len(selected) > 2:
                                selected.pop(0)
                            if len(selected) == 2:
                                if selected[0][1] == selected[1][1]:
                                    score += left * max_score
                                    pairs += left
                                    left -= 1
                                    if left == 0:
                                        playing = False
                                        score += (max(time_left, 0) / 100) * multiplier
                                    else:
                                        for i in range(0, len(objects) - 2, 2):
                                            if rects[i][1] in selected:
                                                objects.pop(i)
                                                objects.pop(i)
                                                break
                                else:
                                    result = left * max_score / 2
                                    score -= result
                                    loss += result
                                    count = 0
                                    for i in range(len(objects)):
                                        if rects[i][1] in selected:
                                            objects[i]["Colour"] = settings[
                                                "Grid Background Colour"
                                            ]
                                            objects[i]["Line Colour"] = settings[
                                                "Grid Line Colour"
                                            ]
                                            count += 1
                                            if count == 2:
                                                break
                                    if count != 2:
                                        logging.error(
                                            f"Only one shape was unselected, selected after: {selected}, objects: {objects}, rects: {rects}"
                                        )

                                selected = []
                                score_text = font.render(
                                    f"Score: {int(score):,}",
                                    settings["Antialiasing Text"],
                                    settings["Background Font Colour"],
                                )
                                score_text_coords = (
                                    (settings["Width"] - score_text.get_width()) // 2,
                                    settings["Height"] * 0.01,
                                )
            elif event.type == pygame.QUIT:
                exitGame()
                return None, None, "Quit", None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None, "Game Menu", None
        time_text = font.render(
            f"Time left: {(time_left/1000):.1f}",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
        time_text_coords = (
            (settings["Width"] - time_text.get_width()) // 2,
            settings["Height"] * 0.01 + score_text.get_height(),
        )
        screen.blit(score_text, score_text_coords)
        screen.blit(time_text, time_text_coords)
        height = settings["Height"] // 200
        for line in return_lines:
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
        getFps(never)
        never = False
        pygame.display.flip()
    lb["loss"] = loss
    lb["time"] = duration - max(time_left, 0)
    lb["pairs"] = pairs
    lb["score"] = score
    adjustment = (score - max_score * 6 - (duration / 200) * multiplier) / 200
    old_score = updateLB(3, lb)
    return score, adjustment, "Game Over", old_score


def rotate_point(shape_x, shape_y, rotation_centre_x, rotation_centre_y, rotation):
    difference_x, difference_y = (
        shape_x - rotation_centre_x,
        shape_y - rotation_centre_y,
    )
    new_x = (
        rotation_centre_x
        + difference_x * math.cos(rotation)
        - difference_y * math.sin(rotation)
    )
    new_y = (
        rotation_centre_y
        + difference_x * math.sin(rotation)
        + difference_y * math.cos(rotation)
    )
    return new_x, new_y


def drawSmallRect(screen, centre, rotation, coords, shape, colour):
    x, y = coords
    centre_x, centre_y = centre
    # print(
    #     f"x {x}, y {y}, centre x {centre_x}, centre y {centre_y}, shape {shape}, shape size {shape_size}, rotation {rotation}, square size {square_size}"
    # )
    if shape == "Square":
        corners = [
            (x - shape_size / 2, y - shape_size / 2),
            (x + shape_size / 2, y - shape_size / 2),
            (x + shape_size / 2, y + shape_size / 2),
            (x - shape_size / 2, y + shape_size / 2),
        ]
    elif shape == "Circle":
        pygame.draw.circle(
            screen,
            colour,
            rotate_point(x, y, centre_x, centre_y, rotation),
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
        raise ValueError(f"Invalid shape: {shape}")
    rotated_corners = []
    for cornerx, cornery in corners:
        rotated_corners.append(
            rotate_point(cornerx, cornery, centre_x, centre_y, rotation)
        )
    pygame.draw.polygon(screen, colour, rotated_corners)

    return

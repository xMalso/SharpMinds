import math, random


def overlap(new_x, new_y):
    for x, y, _, _ in circles:
        if math.dist((new_x, new_y), (x, y)) < 2 * radius:
            return True
    return False


def removeCircle(pos):
    global circles
    for i, (x, y, colour, _) in enumerate(circles):
        if math.dist(pos, (x, y)) < radius:
            circles.pop(i)
            if colour == "Green":
                return -50
            else:
                return 25
    return 0

def Game1(pygame, settings, screen, font):
    global radius, circles
    circle_colour = {"Green": settings["Game Primary Colour"], "Red": settings["Game Secondary Colour"]}
    radius = settings["Width"] // 75
    height = max(font.size(str(char))[1] for char in "0123456789")
    score = 0
    circles = []
    last_tick = 0
    frame = 0
    i = 1
    text_surface = None
    start = pygame.time.get_ticks()
    while start + 30000 > pygame.time.get_ticks():
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                score = max(removeCircle(event.pos) + score, 0)
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, "Main Menu"
        screen.fill(settings["Background Colour"])
        text = font.render(
            "Press ESC to return to the main menu",
            settings["Antialiasing Text"],
            settings["Background Font Colour"],
        )
        screen.blit(
            text,
            (
                settings["Width"] - text.get_width(),
                settings["Height"] - settings["Height"] // 200,
            ),
        )
        current_frame = pygame.time.get_ticks()
        if current_frame - last_tick > 1200 // (settings["Adaptive Difficulty"] ** 0.7):
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
                if tick + (25000 // (settings["Adaptive Difficulty"] ** 1.3)) < current_frame:
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
    print(score)
    return score, "Game 1 Over"

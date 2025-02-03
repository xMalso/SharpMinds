import math, random

circles = []
last_tick = 0
frame = 0
i = 1
text_surface = None

def setRadius(settings):
    global radius
    radius = settings["Width"] // 50
    print(radius)


def bufferHeight(font):
    global height
    height = max(font.size(str(char))[1] for char in "0123456789")
    return height


def overlap(new_x, new_y):
    for x, y, colour in circles:
        if math.dist((new_x, new_y), (x, y)) < 2 * radius:
            return True
    return False

def removeCircle(pos):
    global circles
    for i, (x, y, colour) in enumerate(circles):
        if math.dist(pos, (x, y)) < radius:
            circles.pop(i)
            break

def Game1(pygame, settings, screen, font):
    global last_tick, frame, i, circles, text_surface
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print(event.pos)
                removeCircle(event.pos)
            if event.type == pygame.QUIT:
                pygame.quit()
                return "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Main Menu"
        screen.fill(settings["Background Colour"])
        text = font.render("Press ESC to return to the main menu", settings["Antialiasing Text"], settings["Background Font Colour"])
        screen.blit(text, (settings["Width"] - text.get_width(), settings["Height"] - settings["Height"] // 200))
        current_frame = pygame.time.get_ticks()
        if current_frame - last_tick > 600 // (settings["Adaptive Difficulty"] ** 0.5):
            coords = random.randint(
                settings["Width"] // 100 + radius * 2, (settings["Width"] * 99) // 100 - radius * 2
            ), random.randint(settings["Height"] // 100 + height + radius * 2, (settings["Height"] * 99) // 100 - radius * 2)
            if not overlap(*coords):
                colour = random.randint(0,1)
                print(coords)
                if colour == 0:
                    colour = settings["Game Primary Colour"]
                else:
                    colour = settings["Game Secondary Colour"]
                circles.append(coords + (colour,))
                last_tick = current_frame
        for x, y, colour in circles:
            pygame.draw.circle(screen, colour, (x, y), radius)
        
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

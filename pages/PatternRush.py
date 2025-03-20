global math, pygame
import math
import pygame


def rotate_point(point_x, point_y, centre_x, centre_y, angle):
    difference_x, difference_y = point_x - centre_x, point_y - centre_y
    new_x = centre_x + difference_x * math.cos(angle) - difference_y * math.sin(angle)
    new_y = centre_y + difference_x * math.sin(angle) + difference_y * math.cos(angle)
    return new_x, new_y


def draw_rotated_rect(screen, x, y, width, height, angle, colour):
    angle_rad = math.radians(angle)

    # Centre of the rectangle (rotation point)
    cx, cy = x + width / 2, y + height / 2

    # Define original rectangle corners relative to the top-left
    corners = [
        (-width / 2, -height / 2),  # Top-left
        (width / 2, -height / 2),  # Top-right
        (width / 2, height / 2),  # Bottom-right
        (-width / 2, height / 2),  # Bottom-left
    ]

    # Rotate the rectangle corners around its centre
    rotated_corners = [
        rotate_point(px + cx, py + cy, cx, cy, angle_rad) for px, py in corners
    ]

    # Draw the main rotated rectangle
    pygame.draw.polygon(screen, colour, rotated_corners, 2)

    # === Draw smaller rotated shapes inside ===
    inner_shapes = [
        (-width / 4, -height / 4, width / 4, height / 4),  # Top-left small box
        (width / 8, height / 8, width / 3, height / 3),  # Bottom-right larger box
    ]

    for sx, sy, sw, sh in inner_shapes:
        draw_inner_rotated_rect(
            screen, cx + sx, cy + sy, sw, sh, angle + 45, (0, 255, 255)
        )

    # === Create invisible bounding rect ===
    bounding_rect = pygame.Rect(x, y, width, height)  # This is not drawn

    return bounding_rect  # Can be used for collision detection


def draw_inner_rotated_rect(screen, x, y, width, height, angle, colour=(0, 255, 255)):
    """Draws a smaller rotated rectangle inside another rotated rectangle."""
    angle_rad = math.radians(angle)

    # Centre of the small rectangle
    cx, cy = x + width / 2, y + height / 2

    # Define small rectangle corners relative to its centre
    corners = [
        (-width / 2, -height / 2),
        (width / 2, -height / 2),
        (width / 2, height / 2),
        (-width / 2, height / 2),
    ]

    # Rotate and position the small rectangle
    rotated_corners = [
        rotate_point(px + cx, py + cy, cx, cy, angle_rad) for px, py in corners
    ]

    # Draw the rotated small rectangle
    pygame.draw.polygon(screen, colour, rotated_corners, 2)


def game3(settings, screen, font, getFps, exit):
    return None, None, "Game Menu", None

global math, pygame
import math
import pygame
def rotate_point(point_x, point_y, centre_x, centre_y, angle):
    difference_x, difference_y = point_x - centre_x, point_y - centre_y
    new_x = centre_x + difference_x * math.cos(angle) - difference_y * math.sin(angle)
    new_y = centre_y + difference_x * math.sin(angle) + difference_y * math.cos(angle)
    return new_x, new_y

def draw_rotated_rect(screen, x, y, width, height, angle, color):
    angle_rad = math.radians(angle) # deg to radians

    centre_x, centre_y = x + width / 2, y + height / 2

    corners = [
        (-width / 2, -height / 2),  # Top-left
        (width / 2, -height / 2),   # Top-right
        (width / 2, height / 2),    # Bottom-right
        (-width / 2, height / 2)    # Bottom-left
    ]

    rotated_corners = [rotate_point(point_x + centre_x, point_y + centre_y, centre_x, centre_y, angle_rad) for point_x, point_y in corners]

    pygame.draw.polygon(screen, rotated_corners, 2)
    return # incopmlete

def Game3(settings, screen, font, getFps, exit):
    return None, None, "Game Menu"

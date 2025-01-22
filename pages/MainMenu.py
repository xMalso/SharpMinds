def display_page(settings, screen, font, pygame, buttons):
    for button in buttons.values():
        pygame.draw.rect(screen, button['Colour'], button['Pygame Button'])
        button_text = font.render(button['Name'], settings['Antialiasing Text'], button['Font Colour'])
        screen.blit(button_text, (button['Pygame Button'].x + button['Pygame Button'].width//2 - button_text.get_width()//2, button['Pygame Button'].y + button['Pygame Button'].height//2 - button_text.get_height()//2))
        del button_text
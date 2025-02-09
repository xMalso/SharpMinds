def makeButtons():
    pass


def displayPage(pygame, sys, screen, settings, font, title_font, small_font,
                game, score, getFps):
    game_over_text = title_font.render("Game Over", True,
                                       settings["Background Font Colour"])
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.midtop = (settings["Width"] // 2,
                                  settings["Height"] // 30)
    score_text = font.render(f"Score: {int(score)}", True,
                             settings["Background Font Colour"])
    score_text_rect = score_text.get_rect()
    score_text_rect.midtop = (settings["Width"] // 2,
                              settings["Height"] // 20 +
                              game_over_text.get_height())

    while True:
        screen.fill(settings["Background Colour"])
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(score_text, score_text_rect)
        getFps()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        pygame.display.flip()

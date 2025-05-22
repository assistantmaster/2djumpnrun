import pygame
import random
import time
from positions import positions

pygame.init()

width = 1280
height = 720

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("2D Jump'n'Run")
pygame.display.set_icon(pygame.image.load("./images/favicon.png"))

font = pygame.font.Font(None,20)
font2 = pygame.font.Font(None,100)
copyright = font.render('© 2025 by Jannis und Timo', True, (150,150,150))
gewonnen = font2.render('GEWONNEN!', True, (255,255,255))

background = pygame.image.load("./images/background.jpg")

player = pygame.image.load("./images/player.png")
p1 = pygame.image.load("./images/platform200.png")
p2 = pygame.image.load("./images/platform200.png")
p3 = pygame.image.load("./images/platform200.png")
p4 = pygame.image.load("./images/platform200.png")
p5 = pygame.image.load("./images/platform200.png")
p6 = pygame.image.load("./images/platform200.png")

p1x, p1y = 0, 397
p2x, p2y = 400, 500
p3x, p3y = 800, 300
p4x, p4y = 200, 200
p5x, p5y = 600, 600
p6x, p6y = 1000, 400

font = pygame.font.Font(None,50)

schliessen = False
schliessenindex = 0

level = 9
durchgespielt = False

playerx = 20
playery = 300
playerjump = False
playerjumpindex = 0
playerspeedx = 0.3
playerspeedy = 0.5
jumphight = 200

def is_on_top(player_rect, platform_rect):
    # Prüft, ob der Spieler mit den Füßen auf der Plattform steht
    return (
        player_rect.bottom <= platform_rect.top + 10 and  # max. 10px Toleranz
        player_rect.bottom >= platform_rect.top - 10 and
        player_rect.right > platform_rect.left + 5 and
        player_rect.left < platform_rect.right - 5
    )

def fade_to_black_and_back():
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))
    # Fade in (schwarz wird eingeblendet)
    for alpha in range(0, 256, 16):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(500 // (256 // 16))  # ca. 500ms gesamt
    # 500ms komplett schwarz
    fade_surface.set_alpha(255)
    screen.blit(fade_surface, (0, 0))
    pygame.display.flip()
    pygame.time.delay(500)
    # Fade out (schwarz wird ausgeblendet)
    for alpha in range(255, -1, -16):
        fade_surface.set_alpha(alpha)
        screen.blit(background, (0, 0))
        # Plattformen und Spieler nochmal zeichnen, damit sie sichtbar werden
        screen.blit(p1, (positions[level][0][0], positions[level][0][1]))
        screen.blit(p2, (positions[level][1][0], positions[level][1][1]))
        screen.blit(p3, (positions[level][2][0], positions[level][2][1]))
        screen.blit(p4, (positions[level][3][0], positions[level][3][1]))
        screen.blit(p5, (positions[level][4][0], positions[level][4][1]))
        screen.blit(p6, (positions[level][5][0], positions[level][5][1]))
        screen.blit(player, (playerx, playery))
        screen.blit(copyright, (0, 700))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(500 // (256 // 16))  # ca. 500ms gesamt

running = True
while running:
    #screen.fill((0,0,255))
    screen.blit(background, (0, 0))

    screen.blit(p1, (positions[level][0][0], positions[level][0][1]))
    screen.blit(p2, (positions[level][1][0], positions[level][1][1]))
    screen.blit(p3, (positions[level][2][0], positions[level][2][1]))
    screen.blit(p4, (positions[level][3][0], positions[level][3][1]))
    screen.blit(p5, (positions[level][4][0], positions[level][4][1]))
    screen.blit(p6, (positions[level][5][0], positions[level][5][1]))
    screen.blit(player, (playerx, playery))
    screen.blit(copyright, (0, 700))

    # Rects für Collision Detection erstellen
    player_rect = player.get_rect(topleft=(playerx, playery))
    p1_rect = p1.get_rect(topleft=(positions[level][0][0], positions[level][0][1]))
    p2_rect = p2.get_rect(topleft=(positions[level][1][0], positions[level][1][1]))
    p3_rect = p3.get_rect(topleft=(positions[level][2][0], positions[level][2][1]))
    p4_rect = p4.get_rect(topleft=(positions[level][3][0], positions[level][3][1]))
    p5_rect = p5.get_rect(topleft=(positions[level][4][0], positions[level][4][1]))
    p6_rect = p6.get_rect(topleft=(positions[level][5][0], positions[level][5][1]))

    # Tasteneingaben außerhalb der Event-Schleife abfragen
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and falling == False:
        playerjump = True

    if keys[pygame.K_a] and playerx > 0:
        playerx -= playerspeedx

    if keys[pygame.K_d] and playerx < 1207:
        playerx += playerspeedx
    
    #if keys[pygame.K_ESCAPE]:
    #    running = False

    if playerjump:
        if playerjumpindex < (jumphight/playerspeedy):
            playery -= playerspeedy
        if playerjumpindex > (jumphight/playerspeedy) and not (
            is_on_top(player_rect, p1_rect) or
            is_on_top(player_rect, p2_rect) or
            is_on_top(player_rect, p3_rect) or
            is_on_top(player_rect, p4_rect) or
            is_on_top(player_rect, p5_rect) or
            is_on_top(player_rect, p6_rect)):
            playery += playerspeedy
        playerjumpindex += 1
        if playerjumpindex >= 2*(jumphight/playerspeedy):
            playerjump = False
            playerjumpindex = 0
    else:
        if (is_on_top(player_rect, p1_rect) or
            is_on_top(player_rect, p2_rect) or
            is_on_top(player_rect, p3_rect) or
            is_on_top(player_rect, p4_rect) or
            is_on_top(player_rect, p5_rect) or
            is_on_top(player_rect, p6_rect)):
            falling = False
            for plat_rect in [p1_rect, p2_rect, p3_rect, p4_rect, p5_rect, p6_rect]:
                if is_on_top(player_rect, plat_rect):
                    playery = plat_rect.top - player_rect.height
        else:
            falling = True
            playery += 1
    if playery > height:
        playerx = 20
        playery = 300

    if playerx >= 1207:
        fade_to_black_and_back()
        if level < 9:
            level += 1
        else:
            screen.blit(background, (0,0))
            screen.blit(gewonnen, (400,100))
            screen.blit(player, (600, 300))
            screen.blit(copyright, (0, 700))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
        playerx = 20
        playery = 300



    for event in pygame.event.get():
        if schliessen:
            if event.type == pygame.QUIT:
                running = False
            if time.time() - schliessen_time > 3:
                schliessen = False
                schliessenindex = 0

        if event.type == pygame.QUIT:
            if not schliessen:
                schliessen = True
                schliessen_time = time.time()
            else:
                if time.time() - schliessen_time <= 1:
                    running = False

    pygame.display.flip()

pygame.quit()
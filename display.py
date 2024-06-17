import pygame
import main
import sys, os
from pygame import display

def resource_path(relative_path): # NOT MY CODE <-- Function copied from https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Use on rectangles
def getCenter(rw, rh):
    ws = display.get_window_size()
    w = ws[0]
    h = ws[1]
    return [w / 2 - (rw / 2), h / 2 - (rh / 2)]


def game(teams, score, time, group, offset, winningTeamIndex, gameOn):
    teamColors = [(0, 0, 0), (0, 0, 0)]
    gameRectCenter = getCenter(325, 75)
    if gameOn:
        rectBg = (131, 211, 207)
        print("ON")
    elif gameOn is False:
        rectBg = (214, 214, 214)
        print("Played")
    else:
        rectBg = (255, 255, 255)
        print("To be played")

    gameRect = pygame.Rect(gameRectCenter[0], rect.centery + 100 + offset, 325, 75)
    pygame.draw.rect(surface, rectBg, gameRect, 0, 20)

    team1 = GAME_FONT.render(f"{teams[0]}", True, teamColors[0], rectBg)
    team2 = GAME_FONT.render(f"{teams[1]}", True, teamColors[1], rectBg)

    if winningTeamIndex is not None:
        if winningTeamIndex == 0:
            team1 = GAME_FONT_BOLD.render(f"{teams[0]}", True, (131, 240, 119), rectBg)
        elif winningTeamIndex == 1:
            team2 = GAME_FONT_BOLD.render(f"{teams[1]}", True, (131, 240, 119), rectBg)

    surface.blit(team1, team1.get_rect(center=(gameRect.left + team1.get_width() / 2 + 20, gameRect.centery)))
    surface.blit(team2, team2.get_rect(center=(gameRect.right - team2.get_width() / 2 - 20, gameRect.centery)))
    # team1.get_width()/2 is the text width

    score = GAME_FONT.render(f"{score[0]} - {score[1]}", True, (0, 0, 0), rectBg)
    surface.blit(score, score.get_rect(center=gameRect.center))

    sideRect = pygame.Rect(0, gameRect.centery, 75, 75)
    sideRect.centery = gameRect.centery
    # For left offset, you take the width of the circle and add 5
    l = pygame.draw.rect(surface, rectBg, sideRect.move(gameRect.left - 80, 0), 0, 50)
    r = pygame.draw.rect(surface, rectBg, sideRect.move(gameRect.right + 5, 0), 0, 50)

    time = TIME_FONT.render(time, True, (0, 0, 0), rectBg)
    surface.blit(time, time.get_rect(center=(l.centerx, gameRect.centery)))

    group = GAME_FONT.render(f"NA", True, (0, 0, 0), rectBg)
    surface.blit(group, group.get_rect(center=(r.centerx, gameRect.centery)))


bg = (132, 178, 218)
running = True

pygame.init()

display.set_mode((500, 500))
display.set_caption("Euros 2024")
display.get_surface().fill(bg)

surface = display.get_surface()
centerX = display.get_window_size()[0] / 2

TITLE_FONT = pygame.font.Font(resource_path("Roboto-Bold.ttf"), 25)
HEADING_FONT = pygame.font.Font(resource_path("Roboto-Regular.ttf"), 22)

GAME_FONT = pygame.font.Font(resource_path("Roboto-Regular.ttf"), 18)
GAME_FONT_BOLD = pygame.font.Font(resource_path("Roboto-Bold.ttf"), 18)
TIME_FONT = pygame.font.Font(resource_path("Roboto-Regular.ttf"), 15)

rc = getCenter(300, 50)
rect = pygame.Rect(rc[0], 10, 300, 50)
pygame.draw.rect(surface, (255, 0, 0), rect)

img = TITLE_FONT.render("Euros 2024 Games", True, (0, 0, 0), (255, 0, 0))
surface.blit(img, img.get_rect(center=(centerX, rect.centery)))

returnList = main.currentDay("pygame")
if len(returnList) > 1:
    heading = HEADING_FONT.render(returnList[-1], True, (0, 0, 0), bg)
    surface.blit(heading, heading.get_rect(center=(centerX, rect.centery + 60)))

for i in returnList[:-1]:
    game(i[0], i[1], i[2], i[3], i[4], i[5], i[6])


display.flip()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

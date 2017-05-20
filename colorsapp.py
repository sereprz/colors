import sys
import math
import random
import pygame

from pygame.locals import *

# define colours
GRAY = (245, 245, 245)
LIGHTCYAN = (204, 229, 255)
NAVYBLUE = (60, 60, 100)

BGCOLOR = LIGHTCYAN
BACKSQUARECOLOR = GRAY

WINWIDTH = 500  # main window's width
WINHEIGHT = 560  # main window's height
MARGINX = 40  # left/right margin
MARGINY = 100  # distance from the top of the window
GAPSIZE = 4  # gap between boxes
BACKSQUARESIZE = WINWIDTH - (MARGINX * 2)

TIME = 60

TEXTCOLOR = NAVYBLUE


## Game loop
def main():
    global DISPLAY
    pygame.init()
    FONT = pygame.font.Font('freesansbold.ttf', 24)
    DISPLAY = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption("Colors Game")

    mousex = 0  # mouse x coord
    mousey = 0  # mouse y coord

    gameLevel = 1
    col1, col2 = getColorPair(gameLevel)
    secs = TIME

    mainBoard = getRandomBoard(gameLevel)

    pygame.time.set_timer(USEREVENT, 1000)

    # main loop
    while True:
        DISPLAY.fill(BGCOLOR)

        drawBoard(mainBoard, gameLevel, col1, col2)

        timeLeftText = FONT.render(str(secs) + ' seconds left', True, TEXTCOLOR)
        gameOver = FONT.render("Time's up", True, TEXTCOLOR)
        gameOverRect = gameOver.get_rect()
        gameOverRect.center = (WINWIDTH/2, WINHEIGHT/2 - 50)
        score = FONT.render("Your final score is " + str(gameLevel - 1), True, TEXTCOLOR)
        scoreRect = score.get_rect()
        scoreRect.center = (WINWIDTH/2, WINHEIGHT/2)
        startAgain = FONT.render("Press Enter to play again", True, TEXTCOLOR)
        startAgainRect = startAgain.get_rect()
        startAgainRect.center = (WINWIDTH/2, WINHEIGHT/2 + 50)

        DISPLAY.blit(timeLeftText, (20, 20))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and secs > 0:
                mousex, mousey = event.pos
            elif event.type == USEREVENT and secs > 0:
                secs -= 1
            elif event.type == KEYDOWN and event.key == K_RETURN:
                gameLevel = 1
                secs = TIME
                mainBoard = getRandomBoard(gameLevel)
                drawBoard(mainBoard, gameLevel, col1, col2)
                boxx, boxy = None, None

        boxx, boxy = getBoxAtPixel(mainBoard, mousex, mousey)

        if boxx is not None and boxy is not None and secs > 0:
            if mainBoard[boxx][boxy] == 0:
                gameLevel += 1
                mainBoard = getRandomBoard(gameLevel)
                col1, col2 = getColorPair(gameLevel)
                drawBoard(mainBoard, gameLevel, col1, col2)
        elif secs == 0:
            DISPLAY.fill(BGCOLOR)
            DISPLAY.blit(gameOver, gameOverRect)
            DISPLAY.blit(score, scoreRect)
            DISPLAY.blit(startAgain, startAgainRect)

        pygame.display.update()


def getRandomBoard(level):
    dim = getBoardDim(level)
    boxes = [1] * (dim**2)
    boxes[random.randrange(len(boxes))] = 0

    board = []
    for i in range(dim):
        column = []
        for j in range(dim):
            column.append(boxes[0])
            del boxes[0]
        board.append(column)
    return(board)


def getBoardDim(level):
    if level >= 9:
        dim = 10
    else:
        dim = level + 1
    return dim


def getBoxSize(board):
    return (BACKSQUARESIZE - (GAPSIZE * (len(board) + 1)))/len(board)


def leftTopCoordsOfBox(boxx, boxy, boxsize):
    # convert board coordinates into pixel coordinates
    left = boxy * (boxsize + GAPSIZE) + MARGINX + GAPSIZE
    top = boxx * (boxsize + GAPSIZE) + MARGINY + GAPSIZE
    return(left, top)


def drawBoard(board, level, col1, col2):
    dim = getBoardDim(level)
    boxsize = getBoxSize(board)
    pygame.draw.rect(DISPLAY, BACKSQUARECOLOR, (MARGINX, MARGINY, BACKSQUARESIZE, BACKSQUARESIZE))

    for boxx in range(dim):
        for boxy in range(dim):
            left, top = leftTopCoordsOfBox(boxx, boxy, boxsize)
            if board[boxx][boxy] == 1:
                pygame.draw.rect(DISPLAY, col1, (left, top, boxsize, boxsize))
            else:
                pygame.draw.rect(DISPLAY, col2, (left, top, boxsize, boxsize))


def getBoxAtPixel(board, x, y):
    dim = len(board)
    boxsize = getBoxSize(board)
    for boxx in range(dim):
        for boxy in range(dim):
            left, top = leftTopCoordsOfBox(boxx, boxy, boxsize)
            boxRect = pygame.Rect(left, top, boxsize, boxsize)
            if boxRect.collidepoint(x,y):
                return(boxx, boxy)
    return(None, None)


def hsv_to_rgb(h, s, v):
# see wikipedia for conversion
# https://en.wikipedia.org/wiki/HSL_and_HSV#Converting_to_RGB
    c = v * s
    hhat = h/60
    x = c*(1-math.fabs(hhat % 2 - 1))

    r1, b1, g1 = 0, 0, 0

    if hhat >= 0 and hhat < 1:
        r1, b1, g1 = c, x, 0
    elif hhat >= 1 and hhat < 2:
        r1, b1, g1 = x, c, 0
    elif hhat >= 2 and hhat < 3:
        r1, b1, g1 = 0, c, x
    elif hhat >= 3 and hhat < 4:
        r1, b1, g1 = 0, x, c
    elif hhat >= 4 and hhat < 5:
        r1, b1, g1 = x, 0, c
    elif hhat >= 5 and hhat < 6:
        r1, b1, g1 = c, 0, x

    m = v - c
    return int(255*(r1+m)), int(255*(b1+m)), int(255*(g1+m))


def getColorPair(level):
    h = random.randrange(0, 360)
    v1 = random.uniform(0.6, 0.9)
    s1 = random.uniform(0.75, 1)

    if level <= 5:
        s2 = s1 - 0.5
        v2 = v1 + 0.1
    elif level > 5 and level <= 12:
        s2 = s1 - 0.4
        v2 = v1 + 0.05
    else:
        s2 = s1 - 0.3
        v2 = v1

    col1 = hsv_to_rgb(h, s1, v1)
    col2 = hsv_to_rgb(h, s2, v2)

    return col1, col2


if __name__ == '__main__':
    main()

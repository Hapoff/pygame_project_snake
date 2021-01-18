import random, pygame, sys
from pygame.locals import *
import sqlite3

FPS = 15
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
CELLSIZE = 20
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (127, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
LEMONCHIFFON = (255, 250, 205)
LIGHTYELLOW = (255, 255, 224)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, STANDARTFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('19317.ttf', 25)
    STANDARTFONT = pygame.font.Font('20219.ttf', 21)
    pygame.display.set_caption('Змейка (v.1.0)')

    showStartScreen()

    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Установка случайной начальной точки
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Появление яблока в случайном месте
    apple = getRandomLocation()

    while True: # основной игровой цикл
        for event in pygame.event.get(): # цикл обработки событий
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # Проверка того, попал ли червь в себя или в границу окна
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] ==\
                -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # Игра завершена
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # Игра завершена

        # Проврка съела ли змейка яблоко
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation() # поставить яблоко в случайное место
        else:
            del wormCoords[-1] # удаление хвостового сегмента змейки

        # Перемещение змейки, добавив сегмент в направлении, в котором он движется
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        global sc
        sc = len(wormCoords) - 3
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def record(score): # функция, связанная с рекордом
    con = sqlite3.connect("Рекорд.db")
    cur = con.cursor()
    result = cur.execute("""SELECT Рекорд FROM Рекорд WHERE ID = 1""")
    for elems in result:
        for elem in elems:
            if score > elem:
                sql = """UPDATE Рекорд SET Рекорд = ? WHERE ID = '1'"""
                cur.execute(sql, (str(score),))
                con.commit()
                return score
            else:
                return elem


def showStartScreen(): # функция начального экрана
    titleFont = pygame.font.Font('19317.ttf', 55)

    text = titleFont.render("Добро пожаловать в игру", True, WHITE)
    DISPLAYSURF.blit(text, (50, 20))
    text1 = titleFont.render("'Змейка'", True, GREEN)
    DISPLAYSURF.blit(text1, (210, 70))

    text2 = titleFont.render("Ваш рекорд: {}".format(record(0)), True, LIGHTYELLOW)
    DISPLAYSURF.blit(text2, (160, 250))

    text3 = STANDARTFONT.render("Чтобы выбрать лёгкий уровень сложности, нажмите [E]", True, WHITE)
    DISPLAYSURF.blit(text3, (50, 420))
    text4 = STANDARTFONT.render("Чтобы выбрать средний уровень сложности, нажмите [M]", True, WHITE)
    DISPLAYSURF.blit(text4, (50, 460))
    text5 = STANDARTFONT.render("Чтобы выбрать тяжёлый уровень сложности, нажмите [H]", True, WHITE)
    DISPLAYSURF.blit(text5, (50, 500))

    while True: # цикл, отвечающий за выбор игрового режима
        for event in pygame.event.get():
            global FPS
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == K_e:
                FPS = 7
                return
            elif event.type == pygame.KEYDOWN and event.key == K_m:
                FPS = 15
                return
            elif event.type == pygame.KEYDOWN and event.key == K_h:
                FPS = 20
                return
        pygame.display.flip()
        FPSCLOCK.tick(FPS)


def terminate(): # функция, отвечающая за закрытие игры
    pygame.quit()
    sys.exit()


def getRandomLocation(): # функция, отвечающая за случайное местоположение
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen(): # функция конечного экрана
    DISPLAYSURF.fill(BLACK)

    gameOverFont = pygame.font.Font('19317.ttf', 55)
    gameSurf = gameOverFont.render('Игра окончена', True, LEMONCHIFFON)

    DISPLAYSURF.blit(gameSurf, (160, 30))

    text2 = gameOverFont.render("Ваш рекорд: {}".format(record(sc)), True, LIGHTYELLOW)
    DISPLAYSURF.blit(text2, (160, 250))

    text3 = STANDARTFONT.render("Чтобы выбрать лёгкий уровень сложности, нажмите [E]", True, WHITE)
    DISPLAYSURF.blit(text3, (50, 420))
    text4 = STANDARTFONT.render("Чтобы выбрать средний уровень сложности, нажмите [M]", True, WHITE)
    DISPLAYSURF.blit(text4, (50, 460))
    text5 = STANDARTFONT.render("Чтобы выбрать тяжёлый уровень сложности, нажмите [H]", True, WHITE)
    DISPLAYSURF.blit(text5, (50, 500))

    score = gameOverFont.render("Набрано очков: {}".format(sc), True, WHITE)
    DISPLAYSURF.blit(score, (135, 180))

    while True: # цикл, отвечающий за выбор игрового режима
        for event in pygame.event.get():
            global FPS
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == K_e:
                FPS = 7
                return
            elif event.type == pygame.KEYDOWN and event.key == K_m:
                FPS = 15
                return
            elif event.type == pygame.KEYDOWN and event.key == K_h:
                FPS = 20
                return
        pygame.display.flip()
        FPSCLOCK.tick(FPS)


def drawScore(score): # функция, отвечающая за отрисовку очков
    scoreSurf = BASICFONT.render('Очки: {}'.format(score), True, WHITE)
    DISPLAYSURF.blit(scoreSurf, (520, 10))


def drawWorm(wormCoords): # функция, отвечающая за отрисовку змейки
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord): # функция, отвечающая за отрисовку яблока
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # отрисовка вертикальных линий игрового поля
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # отрисовка горизонтальных линий игрового поля
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
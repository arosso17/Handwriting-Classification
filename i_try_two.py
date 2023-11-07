import tensorflow as tf
import numpy as np
import pygame as pg

#3: 80

new_model = tf.keras.models.load_model("num_read_one")

pg.init()
height = 560
width = 840
win = pg.display.set_mode((width, height))
pg.display.set_caption("Classify")
font1 = pg.font.SysFont('comicsans', 75)

board = [[0 for _ in range(84)] for _ in range(56)]
l_pressed = False
pressed = False
run = True
while run:
    if pressed:
        pos = pg.mouse.get_pos()
        txp = pos[0] // 10
        typ = pos[1] // 10
        if txp != xp or typ != yp:
            xp = txp
            yp = typ
            board[yp][xp] = 1
            board[yp + 1][xp] = 1
            board[yp][xp + 1] = 1
            board[yp + 1][xp + 1] = 1
            board[yp][xp - 1] = 1
            board[yp + 1][xp - 1] = 1
    if l_pressed:
        pos = pg.mouse.get_pos()
        txp = pos[0] // 10
        typ = pos[1] // 10
        if txp != xp or typ != yp:
            xp = txp
            yp = typ
            board[yp][xp] = 0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pg.mouse.get_pos()
                xp = pos[0] // 10
                yp = pos[1] // 10
                board[yp][xp] = 1
                board[yp + 1][xp] = 1
                board[yp][xp + 1] = 1
                board[yp + 1][xp + 1] = 1
                board[yp][xp - 1] = 1
                board[yp + 1][xp - 1] = 1
                pressed = True
            if event.button == 3:
                pos = pg.mouse.get_pos()
                xp = pos[0] // 10
                yp = pos[1] // 10
                board[yp][xp] = 0
                l_pressed = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                pressed = False
            if event.button == 3:
                l_pressed = False
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                lr_board = [[0 for _ in range(28)] for _ in range(28)]
                for i in range(28):
                    for j in range(28):
                        lr_board[i][j] = (board[i * 2][j * 3 - 1] + board[i * 2 + 1][j * 3 - 1] + board[i * 2][j * 3] + board[i * 2][j * 3 + 1] + board[i * 2 + 1][j * 3] + board[i + 1][j * 3 + 1]) / 6
                prediction = new_model.predict([lr_board])
                print(np.argmax(prediction[0]), np.max(prediction[0]))
            if event.key == pg.K_c:
                board = [[0 for _ in range(84)] for _ in range(56)]
    for i in range(56):
        for j in range(84):
            color = board[i][j] * 255
            pg.draw.rect(win, [color, color, color], [10 * j, 10 * i, 10, 10])
    pg.display.update()


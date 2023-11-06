import tensorflow as tf
import numpy as np
import pygame as pg


def train(board, n, m):
    r = n
    lr_board = [[0 for _ in range(28)] for _ in range(28)]
    for i in range(28):
        for j in range(28):
            lr_board[i][j] = (board[i * 2][j * 2] + board[i * 2][j * 2 + 1] + board[i * 2 + 1][j * 2] +
                              board[i * 2 + 1][j * 2 + 1]) / 6
    m.train_on_batch(np.array([lr_board]), np.array([r]), reset_metrics=False)
    prediction = m.predict([lr_board])
    while np.argmax(prediction[0]) != r:
        m.train_on_batch(np.array([lr_board]), np.array([r]), reset_metrics=False)
        prediction = m.predict([lr_board])
    print(np.argmax(prediction[0]), np.max(prediction[0]))
    print("I've been told this is a", r)


def main(m):
    new_model = tf.keras.models.load_model(m)
    print("Using model:", m)

    pg.init()
    height = 360
    width = 440
    win = pg.display.set_mode((width, height), pg.RESIZABLE)
    pg.display.set_caption("Classify digits")
    board = [[0 for _ in range(56)] for _ in range(56)]
    l_pressed = False
    pressed = False
    run = True
    while run:
        width = win.get_width()
        height = win.get_height()
        if pressed:
            pos = pg.mouse.get_pos()
            txp = int(pos[0] / (width / 56))
            typ = int(pos[1] / (height / 56))
            if txp != xp or typ != yp:
                xp = txp
                yp = typ
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= xp + j < 56 and 0 <= yp + i < 56:
                            board[yp + i][xp + j] = 1
        if l_pressed:
            pos = pg.mouse.get_pos()
            txp = int(pos[0] / (width / 56))
            typ = int(pos[1] / (height / 56))
            if txp != xp or typ != yp:
                xp = txp
                yp = typ
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= xp + j < 56 and 0 <= yp + i < 56:
                            board[yp + i][xp + j] = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                new_model.save(m)
                print("Saved as:", m)
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pg.mouse.get_pos()
                    xp = int(pos[0] / (width / 56))
                    yp = int(pos[1] / (height / 56))
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if 0 <= xp + j < 56 and 0 <= yp + i < 56:
                                board[yp + i][xp + j] = 1
                    pressed = True
                if event.button == 3:
                    pos = pg.mouse.get_pos()
                    xp = int(pos[0] / (width / 56))
                    yp = int(pos[1] / (height / 56))
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if 0 <= xp + j < 56 and 0 <= yp + i < 56:
                                board[yp + i][xp + j] = 0
                    l_pressed = True
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    pressed = False
                if event.button == 3:
                    l_pressed = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_0:
                    train(board, 0, new_model)
                if event.key == pg.K_1:
                    train(board, 1, new_model)
                if event.key == pg.K_2:
                    train(board, 2, new_model)
                if event.key == pg.K_3:
                    train(board, 3, new_model)
                if event.key == pg.K_4:
                    train(board, 4, new_model)
                if event.key == pg.K_5:
                    train(board, 5, new_model)
                if event.key == pg.K_6:
                    train(board, 6, new_model)
                if event.key == pg.K_7:
                    train(board, 7, new_model)
                if event.key == pg.K_8:
                    train(board, 8, new_model)
                if event.key == pg.K_9:
                    train(board, 9, new_model)
                if event.key == pg.K_s:
                    new_model.save(m)
                    print("Saved as:", m)
                if event.key == pg.K_SPACE:
                    lr_board = [[0 for _ in range(28)] for _ in range(28)]
                    for i in range(28):
                        for j in range(28):
                            lr_board[i][j] = (board[i * 2][j * 2] + board[i * 2][j * 2 + 1] + board[i * 2 + 1][j * 2] + board[i * 2 + 1][j * 2 + 1]) / 6
                    prediction = new_model.predict([lr_board])
                    print(np.argmax(prediction[0]), np.max(prediction[0]))
                if event.key == pg.K_c:
                    board = [[0 for _ in range(56)] for _ in range(56)]
        for i in range(56):
            for j in range(56):
                color = board[i][j] * 255
                pg.draw.rect(win, [color, color, color], [int((width / 56) * j) - 1, int((height / 56) * i) - 1, int(width / 56) + 1, int(height / 56) + 1])
        pg.display.update()

if __name__ == "__main__":
    model = "num_read_one"  # missed none
    # model = "num_read_model_op"  # missed 56
    main(model)


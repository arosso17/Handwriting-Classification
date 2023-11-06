import tensorflow as tf
import numpy as np
import pygame as pg

letters = {}
for i in range(26):
    letters[i] = chr(ord('a') + i)

buttons = {pg.K_a: 0, pg.K_b: 1, pg.K_c: 2, pg.K_d: 3, pg.K_e: 4, pg.K_f: 5, pg.K_g: 6, pg.K_h: 7, pg.K_i: 8, pg.K_j: 9,
           pg.K_k: 10, pg.K_l: 11, pg.K_m: 12, pg.K_n: 13, pg.K_o: 14, pg.K_p: 15, pg.K_q: 16, pg.K_r: 17, pg.K_s: 18,
           pg.K_t: 19, pg.K_u: 20, pg.K_v: 21, pg.K_w: 22, pg.K_x: 23, pg.K_y: 24, pg.K_z: 25}

def save(x, y):
    with open("alphax", "a") as file:
        for n in x[0]:
            file.writelines(str(n)+"\n")
    with open("alphay", "a") as file:
        file.writelines(str(y[0])+"\n")


def main():
    pg.init()
    height = 360
    width = 440
    win = pg.display.set_mode((width, height), pg.RESIZABLE)
    pg.display.set_caption("Classify letters")
    datax = []
    datay = []
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
                if event.key in buttons.keys():
                    datax.append(board)
                    datay.append(buttons[event.key])
                    save(datax, datay)
                    datax = []
                    datay = []
                    board = [[0 for _ in range(56)] for _ in range(56)]
        for i in range(56):
            for j in range(56):
                color = board[i][j] * 255
                pg.draw.rect(win, [color, color, color],
                             [int((width / 56) * j) - 1, int((height / 56) * i) - 1, int(width / 56) + 1,
                              int(height / 56) + 1])
        pg.display.update()

def read(x, y):
    with open(x, 'r') as file:
        lines = file.readlines()
    count = 0
    line = []
    dx = []
    for i in range(len(lines)):
        line.append(eval(lines[i].strip()))
        count += 1
        if count == 56:
            count = 0
            dx.append(line)
            line = []
    dy = []
    with open(y, 'r') as file:
        lines = file.readlines()
    for line in lines:
        dy.append(int(line.strip()))
    return dx, dy

def train(m):
    model = tf.keras.models.load_model(m)
    print("Using model:", m)
    trainx, trainy = read("alphax", "alphay")
    model.fit(trainx, trainy, epochs=100)
    model.save(m)
    print("Saved as:", m)


if __name__ == "__main__":
    # model = "scratch_one"
    model = "alpha_one_alpha"
    # main()
    train(model)

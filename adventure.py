import pygame
from pygame.locals import *
import sys
from maps import *


def load_map(map):
    vsv = []
    for y, i in enumerate(map):
        for x, j in enumerate(i):
            if j == 1:
                vsv.append(f"(w * {x}, h * {y}, w, h)")
    return vsv


open_1 = False
open_10 = False

walk_w = False
walk_a = False
walk_s = False
walk_d = False

fps = 120
clock = pygame.time.Clock()

pygame.init()
# screen = pygame.display.set_mode((100, 100), pygame.RESIZABLE)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1900, 1000), pygame.RESIZABLE)
pygame.display.set_caption('Adventure')


class Trigger:
    def __init__(self, rect):
        print(rect)
        self.rect = rect


class GR(pygame.sprite.Sprite):
    def __init__(self, grp, rct, clr):
        super().__init__(grp)
        self.image = pygame.Surface((rct[2], rct[3]))
        self.image.fill(clr)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = rct[0], rct[1]

    def update(self, mm1, mm2, borders):
        self.rect = self.rect.move(mm1, mm2)
        if any([pygame.sprite.collide_rect(self, i) for i in
                borders]):  # если пересекается потом граница
            self.rect = self.rect.move(-mm1, -mm2)


class start:
    def __init__(self, screen):
        self.screen = screen

        self.st()
        self.run()

    def st(self):
        w, h = pygame.display.get_surface().get_size()
        screen.fill((161, 71, 221))
        pygame.draw.rect(self.screen, (184, 182, 184),
                         ((w // 20), (h // 20), ((w // 20) * 18), ((h // 20) * 18)))
        pygame.draw.rect(self.screen, (184, 182, 184),
                         (((w // 20) * 8), ((h // 20) * 18), ((w // 20) * 4), ((h // 20) * 3)))

        font = pygame.font.Font(None, 72)
        t_cont = font.render("Нажмите любую кнопку для начала", True, (66, 187, 79))
        self.screen.blit(t_cont,
                         (w // 2 - t_cont.get_width() // 2, h // 2 - t_cont.get_height() // 2))
        t_esc = font.render("Для выхода нажмите ESC", True, (66, 187, 79))
        self.screen.blit(t_esc,
                         (w // 2 - t_cont.get_width() // 2, h // 2 + t_esc.get_height() // 2))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                print(event)
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    kk = pygame.key.get_pressed()
                    if kk[K_ESCAPE]:
                        running = False
                    else:
                        running = False
                        map_1(self.screen, "(w * 19, h * 28, w, h * 2)")
                        break

                else:
                    self.st()
                    pygame.display.flip()


class play:
    def __init__(self, screen, spawn):
        self.spawn = spawn
        self.screen = screen
        self.step = 2  # кол-во шагов за один раз
        self.init()
        self.initSU()
        self.run()

    def run(self):
        running = True
        global walk_w, walk_a, walk_s, walk_d
        while running:
            # обработка событий
            eventnow = {}
            for i in pygame.event.get():
                if i.type == KEYDOWN or i.type == KEYUP:
                    eventnow.update([(i.type, i.key)])
                else:
                    eventnow.update([(i.type, None)])

            if QUIT in eventnow:  # завершение работы
                running = False
                pygame.quit()
                break

            if KEYDOWN in eventnow:
                if eventnow[KEYDOWN] == K_w:  # шаг вверх
                    walk_w = True
                if eventnow[KEYDOWN] == K_a:  # влево
                    walk_a = True
                if eventnow[KEYDOWN] == K_s:  # вниз
                    walk_s = True
                if eventnow[KEYDOWN] == K_d:  # вправо
                    walk_d = True
            if KEYUP in eventnow:
                if eventnow[KEYUP] == K_w:  # шаг вверх
                    walk_w = False
                if eventnow[KEYUP] == K_a:  # влево
                    walk_a = False
                if eventnow[KEYUP] == K_s:  # вниз
                    walk_s = False
                if eventnow[KEYUP] == K_d:  # вправо
                    walk_d = False


            if walk_w:
                self.player.update(0, -self.step, self.borders)
            if walk_a:
                self.player.update(-self.step, 0, self.borders)
            if walk_s:  # вниз
                self.player.update(0, self.step, self.borders)
            if walk_d:  # вправо
                self.player.update(self.step, 0, self.borders)

            for i in self.trigger.keys():  # не пришел ли пользователь в триггер
                if pygame.sprite.collide_rect(self.player, i):
                    running = False
                    a = self.trigger[i][0]
                    a(self.screen, self.trigger[i][1])
                    break

            if KEYDOWN in eventnow:
                kk = pygame.key.get_pressed()
                if kk[K_ESCAPE]:  # завершение работы при ESC
                    running = False
                    break

            if WINDOWRESIZED in eventnow:  # перерисовка при изменении размеров окна
                running = False
                self.init()
                self.initSU()
                self.run()


        # отрисовка
            if running:
                screen.fill(self.c_main)
                self.all_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(fps)
    def initSU(self):
        screen.fill(self.c_main)  # залить основным цветом
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.all_sprites = pygame.sprite.Group()  # все спрайты
        self.borders = pygame.sprite.Group()  # границы (прямоугольники)

        for rr in self.gran:
            if len(rr) == 2:  # если передан цвет
                a = GR(self.all_sprites, rr[0], rr[1])  # то отрисовываем этим цветом
            else:  # если нет
                a = GR(self.all_sprites, rr, self.c_sec)  # цвет, заданный в классе карты
            self.borders.add(a)

        self.player = GR(self.all_sprites, eval(self.spawn), self.c_sec)  # игрок
        self.all_sprites.add(self.player)
        self.all_sprites.draw(screen)  # отрисовываем спрайты
        pygame.display.flip()


class map_zero(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 15, h * 38, w * 10, h * 2)): [map_1, "(w * 19, h * 33, w, h * 2)"]}
        self.c_main = (184, 182, 184)
        self.c_sec = (239, 223, 37)
        self.gran = []
        for i in load_map(mas_map_26[::]):
            self.gran.append(eval(i))


class map_1(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()  # получаем размеры окна сейчас
        w, h = w_n // 40, h_n // 40  # делим (потом будем размещать объекты исходя из этих размеров (пропорционально))
        self.trigger = {
            Trigger((w * 15, h * 39, w * 10, h * 2)): [map_2, "(w * 19, h * 3, w, h * 2)"],
            Trigger((w * 16, h * 24, w * 6, h * 2)): [map_zero, "(w * 20, h * 33, w, h * 2)"]}
        # если игрок попадает в прямоугольник, записанный в trigger, то переносится на другую карту
        self.c_main = (184, 182, 184)  # цвет_основной, фон
        self.c_sec = (239, 223, 37)  # цвет_второй
        # gran - все границы на карте
        # чуть позже они отрисуются и запишутся в группы спрайтов
        self.gran = [(0, 0, w * 2, h * 40),  # левая полоса
                     (0, 0, w * 10, h * 4),  # верхняя левая
                     (0, h * 38, w * 15, h * 4),  # нижняя левая
                     (w * 11, 0, w, h * 6),  # столбик 1
                     (w * 13, 0, w, h * 6),  # столбик 2
                     (w * 15, 0, w, h * 6),  # столбик 3
                     (w * 25, h * 38, w * 15, h * 4),  # правая нижняя
                     (w * 30, 0, w * 10, h * 4),  # правая верхняя
                     (w * 24, 0, w, h * 6),  # столбик 4
                     (w * 26, 0, w, h * 6),  # столбик 5
                     (w * 28, 0, w, h * 6),  # столбик 6
                     (w * 9, h * 4, w * 7, h * 13),  # квадрат левый верхний
                     (w * 24, h * 4, w * 7, h * 13),  # квадрат правый верхний
                     (w * 38, 0, w * 2, h * 40),  # правая полоса
                     (w * 21, h * 9, w * 7, h * 15),
                     (w * 11, h * 9, w * 7, h * 15),
                     (w * 11, h * 24, w * 7, h * 7),  # квадрат левый нижний
                     (w * 21, h * 24, w * 7, h * 7),  # квадрат правый нижний
                     ]
        if not open_1:
            self.gran.append((w * 11, h * 9, w * 17, h * 15))  # прямоугольник посередине


class map_2(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((w * 15, 0, w * 10, h * 2)): [map_1, "(w * 19, h * 37, w, h * 2)"],
                        Trigger((w * 38, 0, w * 2, h_n)): [map_3, "(w * 3, h * 20, w, h * 2)"],
                        Trigger((0, 0, w * 2, h_n)): [map_4, "(w * 37, h * 19, w, h * 2)"]}
        self.c_main = (184, 182, 184)  # цвет_основной
        self.c_sec = (72, 185, 81)  # цвет_второй
        self.gran = [(0, 0, w * 15, h * 2),  # верхняя левая
                     (0, h * 38, w_n, h * 4),  # нижняя
                     (w * 25, 0, w * 15, h * 2),  # правая верхняя
                     ]


class map_3(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((0, 0, w * 2, h_n)): [map_2, "(w * 37, h * 19, w, h * 2)"],
                        Trigger((w * 15, h * 38, w * 10, h * 2)): [map_16,
                                                                   "(w * 18, h * 6, w, h * 2)"],
                        Trigger((w * 38, h * 2, w * 2, h * 35)): [map_3, "(w * 33, h * 24, w, h * 2)"]}
        self.c_main = (184, 182, 184)  # цвет_основной
        self.c_sec = (171, 176, 60)  # цвет_второй
        self.gran = [(0, h * 38, w * 15, h * 2),  # нижняя левая
                     (0, 0, w_n, h * 2),  # верхняя
                     (w * 25, h * 38, w * 15, h * 2),  # нижняя правая
                     ]


class map_4(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((w * 38, 0, w * 2, h_n)): [map_2, "(w * 3, h * 19, w, h * 2)"],
                        Trigger((w * 15, 0, w * 10, h * 2)): [map_5, "(w * 37, h * 19, w, h * 2)"],
                        Trigger((w * 0, 2, w * 1, h * 25)): [map_4, "(w * 10, h * 20, w, h * 2)"]
                        }
        self.c_main = (184, 182, 184)  # цвет_основной
        self.c_sec = (138, 170, 84)  # цвет_второй
        self.gran = [(0, 0, w * 15, h * 2),  # верхняя левая
                     (0, h * 38, w_n, h * 4),  # нижняя
                     (w * 25, 0, w * 15, h * 2),  # правая верхняя
                     ]
class map_5(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((w * 38, h * 15, w * 1, h * 9)): [map_4, "(w * 20, h * 6, w, h * 2)"],
                        Trigger((w * 0, h * 26, w * 1, h * 9)): [map_6, "(w * 36, h * 29, w, h * 2)"]}
        self.c_main = (184, 182, 184)
        self.c_sec = (18, 10, 143)
        self.gran = []
        for i in load_map(mas_map_5[::]):
            self.gran.append(eval(i))


class map_6(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((w * 39, h * 24, w * 1, h * 9)): [map_5, "(w * 4, h * 27, w, h * 2)"],
                        Trigger((w * 13, h * 1, w * 9, h * 1)): [map_7, "(w * 20, h * 35, w, h * 2)"]}
        self.c_main = (184, 182, 184)
        self.c_sec = (18, 10, 143)
        self.gran = []
        for i in load_map(mas_map_6[::]):
            self.gran.append(eval(i))


class map_7(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((w * 15, h * 38, w * 9, h * 1)): [map_6, "(w * 15, h * 5, w, h * 2)"],
                        Trigger((w * 15, h * 1, w * 10, h * 1)): [map_8, "(w * 20, h * 33, w, h * 2)"]}
        self.c_main = (184, 182, 184)
        self.c_sec = (18, 10, 143)
        self.gran = []
        for i in load_map(mas_map_7[::]):
            self.gran.append(eval(i))

class map_8(play):  # черный замок
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 16, h * 38, w * 9, h * 2)): [map_7, "(w * 22, h * 5, w, h * 2)"],
            Trigger((w * 16, h * 24, w * 6, h * 2)): [map_9, "(w * 20, h * 33, w, h * 2)"]}
        self.c_main = (184, 182, 184)
        self.c_sec = (0, 1, 1)
        self.gran = [(0, 0, w * 2, h * 40),  # левая полоса
                     (0, 0, w * 10, h * 4),  # верхняя левая
                     (0, h * 38, w * 15, h * 4),  # нижняя левая
                     (w * 11, 0, w, h * 6),  # столбик 1
                     (w * 13, 0, w, h * 6),  # столбик 2
                     (w * 15, 0, w, h * 6),  # столбик 3
                     (w * 25, h * 38, w * 15, h * 4),  # правая нижняя
                     (w * 30, 0, w * 10, h * 4),  # правая верхняя
                     (w * 24, 0, w, h * 6),  # столбик 4
                     (w * 26, 0, w, h * 6),  # столбик 5
                     (w * 28, 0, w, h * 6),  # столбик 6
                     (w * 9, h * 4, w * 7, h * 13),  # квадрат левый верхний
                     (w * 24, h * 4, w * 7, h * 13),  # квадрат правый верхний
                     (w * 38, 0, w * 2, h * 40),  # правая полоса
                     (w * 21, h * 9, w * 7, h * 15),
                     (w * 11, h * 9, w * 7, h * 15),
                     (w * 11, h * 24, w * 7, h * 7),  # квадрат левый нижний
                     (w * 21, h * 24, w * 7, h * 7),  # квадрат правый нижний
                     ]

        if not open_1:
            self.gran.append((w * 11, h * 9, w * 17, h * 15))  # прямоугольник посередине

class map_9(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 15, h * 38, w * 8, h * 2)): [map_8, "(w * 20, h * 34, w, h * 2)"]}
        self.c_main = (184, 182, 184)
        self.c_sec = (0, 0, 0)
        self.gran = []
        for i in load_map(mas_map_26[::]):
            self.gran.append(eval(i))




class map_16(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 9, h * 38, w * 3, h * 2)): [map_17, "(w * 8, h * 3, w, h * 2)"],
            Trigger((w * 15, h * 2, w * 10, h * 2)): [map_3, "(w * 17, h * 36, w, h * 2)"],
            Trigger((w * 14, h * 38, w * 3, h * 2)): [map_17, "(w * 14, h * 3, w, h * 2)"],
            Trigger((w * 22, h * 38, w * 3, h * 2)): [map_17, "(w * 22, h * 3, w, h * 2)"],
            Trigger((w * 28, h * 38, w * 3, h * 2)): [map_17, "(w * 28, h * 3, w, h * 2)"],
            Trigger((w * 0, h * 22, w * 1, h * 15)): [map_17, "(w * 38, h * 30, w, h * 2)"],
            Trigger((w * 36, h * 22, w * 1, h * 15)): [map_17, "(w * 5, h * 31, w, h * 2)"],
            Trigger((w * 0, h * 2, w * 1, h * 7)): [map_17, "(w * 36, h * 5, w, h * 2)"],
            Trigger((w * 0, h * 13, w * 1, h * 7)): [map_17, "(w * 36, h * 15, w, h * 2)"],
            Trigger((w * 39, h * 2, w * 1, h * 7)): [map_17, "(w * 5, h * 5, w, h * 2)"],
            Trigger((w * 39, h * 13, w * 1, h * 15)): [map_17, "(w * 5, h * 15, w, h * 2)"]
        }
        # Trigger((w * 37, h * 24, w * 3, h * 15)): [map_17, "(w * 3, h * 30, w, h * 2)"]}
        self.c_main = (184, 182, 184)
        self.c_sec = (232, 110, 34)
        self.gran = []
        for i in load_map(mas_map_16[::]):
            self.gran.append(eval(i))


class map_17(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 9, h * 0, w * 3, h * 2)): [map_16, "(w * 9, h * 36, w, h * 2)"],
            Trigger((w * 14, h * 0, w * 3, h * 1)): [map_16, "(w * 14, h * 34, w, h * 2)"],
            Trigger((w * 22, h * 0, w * 3, h * 1)): [map_16, "(w * 22, h * 34, w, h * 2)"],
            Trigger((w * 28, h * 0, w * 3, h * 2)): [map_16, "(w * 28, h * 34, w, h * 2)"],
            Trigger((w * 1, h * 23, w * 1, h * 15)): [map_16, "(w * 34, h * 23, w, h * 2)"],
            Trigger((w * 39, h * 23, w * 1, h * 15)): [map_16, "(w * 4, h * 25, w, h * 2)"],
            Trigger((w * 39, h * 23, w * 1, h * 15)): [map_16, "(w * 4, h * 25, w, h * 2)"],
            Trigger((w * 2, h * 37, w * 4, h * 2)): [map_18, "(w * 2, h * 4, w, h * 2)"],
            # положение F
            Trigger((w * 34, h * 38, w * 4, h * 2)): [map_18, "(w * 36, h * 4, w, h * 2)"],
            # положение C
            Trigger((w * 7, h * 38, w * 3, h * 2)): [map_18, "(w * 8, h * 5, w, h * 2)"],
            Trigger((w * 11, h * 38, w * 3, h * 2)): [map_18, "(w * 12, h * 5, w, h * 2)"],
            Trigger((w * 26, h * 38, w * 3, h * 2)): [map_18, "(w * 27, h * 5, w, h * 2)"],
            Trigger((w * 31, h * 38, w * 3, h * 2)): [map_18, "(w * 32, h * 5, w, h * 2)"],
            Trigger((w * 22, h * 38, w * 3, h * 2)): [map_18, "(w * 24, h * 5, w, h * 2)"],
            Trigger((w * 15, h * 38, w * 3, h * 2)): [map_18, "(w * 15, h * 5, w, h * 2)"],
            Trigger((w * 0, h * 2, w * 1, h * 7)): [map_16, "(w * 36, h * 5, w, h * 2)"],
            Trigger((w * 0, h * 13, w * 1, h * 7)): [map_16, "(w * 36, h * 15, w, h * 2)"],
            Trigger((w * 39, h * 2, w * 1, h * 7)): [map_16, "(w * 4, h * 5, w, h * 2)"],
            Trigger((w * 39, h * 13, w * 1, h * 7)): [map_16, "(w * 4, h * 15, w, h * 2)"]
        }
        # Trigger((w * 7, h * 38, w * 3, h * 2)): [map_18, "(w * 8, h * 2, w, h * 2)"],}
        self.c_main = (184, 182, 184)
        self.c_sec = (232, 110, 34)
        self.gran = []
        for i in load_map(mas_map_17[::]):
            self.gran.append(eval(i))


class map_18(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 2, h * 2, w * 4, h * 2)): [map_17, "(w * 2, h * 35, w, h * 2)"],
            # возвратный триггерв положение F
            Trigger((w * 34, h * 2, w * 4, h * 2)): [map_17, "(w * 35, h * 36, w, h * 2)"],
            # возвратный триггер в положение C
            Trigger((w * 7, h * 2, w * 3, h * 2)): [map_17, "(w * 7, h * 33, w, h * 2)"],
            Trigger((w * 11, h * 2, w * 3, h * 2)): [map_17, "(w * 12, h * 33, w, h * 2)"],
            Trigger((w * 26, h * 2, w * 3, h * 2)): [map_17, "(w * 27, h * 33, w, h * 2)"],
            Trigger((w * 31, h * 2, w * 3, h * 2)): [map_17, "(w * 32, h * 33, w, h * 2)"],
            Trigger((w * 15, h * 2, w * 3, h * 2)): [map_17, "(w * 15, h * 33, w, h * 2)"],
            Trigger((w * 22, h * 2, w * 3, h * 2)): [map_17, "(w * 24, h * 33, w, h * 2)"],
            Trigger((w * 0, h * 2, w * 1, h * 36)): [map_24, "(w * 37, h * 23, w, h * 2)"],
            Trigger((w * 39, h * 4, w * 1, h * 36)): [map_27, "(w * 4, h * 23, w, h * 2)"], }
        self.c_main = (184, 182, 184)
        self.c_sec = (232, 110, 34)
        self.gran = []
        for i in load_map(mas_map_18[::]):
            self.gran.append(eval(i))


class map_19(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 39, h * 8, w * 1, h * 15)): [map_20, "(w * 7, h * 17, w, h * 2)"],
            Trigger((w * 0, h * 8, w * 1, h * 15)): [map_20, "(w * 35, h * 17, w, h * 2)"],
            Trigger((w * 38, h * 2, w * 1, h * 4)): [map_20, "(w * 5, h * 3, w, h * 2)"],
            Trigger((w * 0, h * 2, w * 1, h * 4)): [map_20, "(w * 35, h * 3, w, h * 2)"],
            Trigger((w * 3, h * 39, w * 2, h * 1)): [map_21, "(w * 4, h * 5, w, h * 2)"],
            Trigger((w * 8, h * 39, w * 2, h * 1)): [map_21, "(w * 9, h * 5, w, h * 2)"],
            Trigger((w * 15, h * 39, w * 4, h * 2)): [map_21, "(w * 16, h * 5, w, h * 2)"],
            Trigger((w * 21, h * 39, w * 4, h * 2)): [map_21, "(w * 24, h * 5, w, h * 2)"],
            Trigger((w * 30, h * 39, w * 3, h * 2)): [map_21, "(w * 31, h * 5, w, h * 2)"],
            Trigger((w * 35, h * 39, w * 3, h * 2)): [map_21, "(w * 36, h * 5, w, h * 2)"]
        }
        self.c_main = (184, 182, 184)
        self.c_sec = (248, 10, 0)
        self.gran = []
        for i in load_map(mas_map_19[::]):
            self.gran.append(eval(i))


class map_20(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 18, h * 38, w * 4, h * 2)): [map_22, "(w * 19, h * 7, w, h * 2)"],
            Trigger((w * 13, h * 38, w * 3, h * 2)): [map_22, "(w * 13, h * 5, w, h * 2)"],
            Trigger((w * 24, h * 38, w * 4, h * 2)): [map_22, "(w * 24, h * 5, w, h * 2)"],
            Trigger((w * 3, h * 38, w * 4, h * 2)): [map_22, "(w * 3, h * 5, w, h * 2)"],
            Trigger((w * 33, h * 38, w * 4, h * 2)): [map_22, "(w * 33, h * 5, w, h * 2)"],
            Trigger((w * 0, h * 2, w * 1, h * 4)): [map_19, "(w * 37, h * 3, w, h * 2)"],
            Trigger((w * 0, h * 8, w * 1, h * 15)): [map_19, "(w * 35, h * 17, w, h * 2)"],
            Trigger((w * 38, h * 8, w * 1, h * 15)): [map_19, "(w * 7, h * 17, w, h * 2)"],
            Trigger((w * 38, h * 2, w * 1, h * 4)): [map_19, "(w * 5, h * 3, w, h * 2)"],
            Trigger((w * 19, h * 18, w * 3, h * 1)): [map_20, "(w * 24, h * 3, w, h * 2)"], # телепортация за стену
            }
        self.c_main = (184, 182, 184)
        self.c_sec = (248, 10, 0)
        self.gran = []
        for i in load_map(mas_map_20[::]):
            self.gran.append(eval(i))


class map_21(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 3, h * 2, w * 3, h * 2)): [map_19, "(w * 5, h * 35, w, h * 2)"],
            Trigger((w * 8, h * 2, w * 3, h * 2)): [map_19, "(w * 9, h * 35, w, h * 2)"],
            Trigger((w * 15, h * 2, w * 4, h * 2)): [map_19, "(w * 16, h * 35, w, h * 2)"],
            Trigger((w * 21, h * 2, w * 4, h * 2)): [map_19, "(w * 23, h * 35, w, h * 2)"],
            Trigger((w * 30, h * 2, w * 3, h * 2)): [map_19, "(w * 32, h * 35, w, h * 2)"],
            Trigger((w * 35, h * 2, w * 3, h * 2)): [map_19, "(w * 36, h * 35, w, h * 2)"],
            Trigger((w * 38, h * 22, w * 2, h * 9)): [map_22, "(w * 5, h * 25, w, h * 2)"],
            Trigger((w * 38, h * 32, w * 2, h * 6)): [map_22, "(w * 5, h * 35, w, h * 2)"],
            Trigger((w * 19, h * 15, w * 4, h * 2)): [map_21, "(w * 19, h * 25, w, h * 2)"], # телепортация за стену
            Trigger((w * 3, h * 22, w * 1, h * 9)): [map_22, "(w * 35, h * 25, w, h * 2)"],
            Trigger((w * 3, h * 32, w * 1, h * 8)): [map_22, "(w * 35, h * 35, w, h * 2)"],
            Trigger((w * 15, h * 38, w * 10, h * 2)): [map_21, "(w * 20, h * 26, w, h * 2)"]
        }
        self.c_main = (184, 182, 184)
        self.c_sec = (248, 10, 0)
        self.gran = []
        for i in load_map(mas_map_21[::]):
            self.gran.append(eval(i))


class map_22(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 15, h * 38, w * 8, h * 2)): [map_23, "(w * 16, h * 33, w, h * 2)"],
            Trigger((w * 18, h * 2, w * 4, h * 2)): [map_20, "(w * 23, h * 33, w, h * 2)"],
            Trigger((w * 13, h * 2, w * 4, h * 2)): [map_20, "(w * 13, h * 33, w, h * 2)"],
            Trigger((w * 24, h * 2, w * 4, h * 2)): [map_20, "(w * 24, h * 33, w, h * 2)"],
            Trigger((w * 3, h * 2, w * 4, h * 2)): [map_20, "(w * 4, h * 33, w, h * 2)"],
            Trigger((w * 33, h * 2, w * 4, h * 2)): [map_20, "(w * 33, h * 33, w, h * 2)"],
            Trigger((w * 0, h * 22, w * 1, h * 10)): [map_21, "(w * 35, h * 25, w, h * 2)"],
            Trigger((w * 0, h * 33, w * 1, h * 10)): [map_21, "(w * 35, h * 35, w, h * 2)"],
            Trigger((w * 38, h * 22, w * 1, h * 9)): [map_21, "(w * 5, h * 25, w, h * 2)"],
            Trigger((w * 38, h * 33, w * 1, h * 10)): [map_21, "(w * 5, h * 35, w, h * 2)"],
        }
        self.c_main = (184, 182, 184)
        self.c_sec = (248, 10, 0)
        self.gran = []
        for i in load_map(mas_map_22[::]):
            self.gran.append(eval(i))


class map_23(play):  # белый замок
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 16, h * 38, w * 9, h * 2)): [map_24, "(w * 16, h * 5, w, h * 2)"],
            Trigger((w * 16, h * 24, w * 6, h * 2)): [map_22, "(w * 16, h * 33, w, h * 2)"], }
        self.c_main = (184, 182, 184)
        self.c_sec = (255, 255, 255)
        self.gran = [(0, 0, w * 2, h * 40),  # левая полоса
                     (0, 0, w * 10, h * 4),  # верхняя левая
                     (0, h * 38, w * 15, h * 4),  # нижняя левая
                     (w * 11, 0, w, h * 6),  # столбик 1
                     (w * 13, 0, w, h * 6),  # столбик 2
                     (w * 15, 0, w, h * 6),  # столбик 3
                     (w * 25, h * 38, w * 15, h * 4),  # правая нижняя
                     (w * 30, 0, w * 10, h * 4),  # правая верхняя
                     (w * 24, 0, w, h * 6),  # столбик 4
                     (w * 26, 0, w, h * 6),  # столбик 5
                     (w * 28, 0, w, h * 6),  # столбик 6
                     (w * 9, h * 4, w * 7, h * 13),  # квадрат левый верхний
                     (w * 24, h * 4, w * 7, h * 13),  # квадрат правый верхний
                     (w * 38, 0, w * 2, h * 40),  # правая полоса
                     (w * 21, h * 9, w * 7, h * 15),
                     (w * 11, h * 9, w * 7, h * 15),
                     (w * 11, h * 24, w * 7, h * 7),  # квадрат левый нижний
                     (w * 21, h * 24, w * 7, h * 7),  # квадрат правый нижний
                     ]

        if not open_1:
            self.gran.append((w * 11, h * 9, w * 17, h * 15))  # прямоугольник посередине


class map_24(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 40, h * 2, w * 2, h * 36)): [map_18, "(w * 5, h * 24, w, h * 2)"],
            Trigger((w * 40, h * 2, w * 2, h * 36)): [map_18, "(w * 5, h * 24, w, h * 2)"],
            Trigger((w * 15, h * 38, w * 8, h * 2)): [map_25, "(w * 16, h * 5, w, h * 2)"],
            Trigger((w * 15, h * 3, w * 10, h * 2)): [map_23, "(w * 20, h * 33, w, h * 2)"],
            Trigger((w * 0, h * 2, w * 2, h * 36)): [map_24, "(w * 20, h * 20, w, h * 2)"], }
        self.c_main = (184, 182, 184)
        self.c_sec = (107, 142, 35)
        self.gran = []
        for i in load_map(mas_map_24[::]):
            self.gran.append(eval(i))


class map_25(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 15, h * 2, w * 8, h * 2)): [map_24, "(w * 17, h * 33, w, h * 2)"]}
        self.c_main = (184, 182, 184)
        self.c_sec = (107, 142, 35)
        self.gran = []
        for i in load_map(mas_map_25[::]):
            self.gran.append(eval(i))


class map_26(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 15, h * 38, w * 8, h * 2)): [map_27, "(w * 17, h * 5, w, h * 2)"]}
        self.c_main = (184, 182, 184)
        self.c_sec = (138, 0, 255)
        self.gran = []
        for i in load_map(mas_map_26[::]):
            self.gran.append(eval(i))


class map_27(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 0, h * 3, w * 1, h * 36)): [map_18, "(w * 36, h * 23, w, h * 2)"],
            Trigger((w * 15, h * 38, w * 8, h * 2)): [map_28, "(w * 16, h * 5, w, h * 2)"],
            Trigger((w * 15, h * 2, w * 8, h * 2)): [map_26, "(w * 16, h * 33, w, h * 2)"],
            Trigger((w * 40, h * 2, w * 2, h * 36)): [map_27, "(w * 20, h * 20, w, h * 2)"]}
        self.c_main = (184, 182, 184)
        self.c_sec = (0, 191, 255)
        self.gran = []
        for i in load_map(mas_map_24[::]):
            self.gran.append(eval(i))


class map_28(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {
            Trigger((w * 15, h * 2, w * 8, h * 2)): [map_27, "(w * 17, h * 33, w, h * 2)"]}
        self.c_main = (184, 182, 184)
        self.c_sec = (255, 43, 43)
        self.gran = []
        for i in load_map(mas_map_25[::]):
            self.gran.append(eval(i))


start(screen)
pygame.quit()

import pygame
from pygame.locals import *
import sys


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
        if any([pygame.sprite.collide_rect(self, i) for i in borders]):  # если пересекается потом граница
            self.rect = self.rect.move(-mm1, -mm2)


class start:
    def __init__(self, screen):
        self.screen = screen

        self.st()
        self.run()

    def st(self):
        w, h = pygame.display.get_surface().get_size()
        screen.fill((161, 71, 221))
        pygame.draw.rect(self.screen, (184, 182, 184), ((w // 20), (h // 20), ((w // 20) * 18), ((h // 20) * 18)))
        pygame.draw.rect(self.screen, (184, 182, 184), (((w // 20) * 8), ((h // 20) * 18), ((w // 20) * 4), ((h // 20) * 3)))

        font = pygame.font.Font(None, 72)
        t_cont = font.render("Нажмите любую кнопку для начала", True, (66, 187, 79))
        self.screen.blit(t_cont, (w // 2 - t_cont.get_width() // 2, h // 2 - t_cont.get_height() // 2))
        t_esc = font.render("Для выхода нажмите ESC", True, (66, 187, 79))
        self.screen.blit(t_esc, (w // 2 - t_cont.get_width() // 2, h // 2 + t_esc.get_height() // 2))
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
        self.step = 30  # кол-во шагов за один раз
        self.init()
        self.initSU()
        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                print(event)  # ОТЛД
                if event.type == QUIT:  # завершение работы
                    running = False
                    break

                if event.type == TEXTINPUT:
                    kk = pygame.key.get_pressed()

                    if kk[K_w]:  # шаг вверх
                        self.player.update(0, -self.step, self.borders)
                    if kk[K_a]:  # влево
                        self.player.update(-self.step, 0, self.borders)
                    if kk[K_s]:  # вниз
                        self.player.update(0, self.step, self.borders)
                    if kk[K_d]:  # вправо
                        self.player.update(self.step, 0, self.borders)

                    for i in self.trigger.keys():  # не пришел ли пользователь в триггер
                        if pygame.sprite.collide_rect(self.player, i):
                            running = False
                            a = self.trigger[i][0]
                            a(self.screen, self.trigger[i][1])

                if event.type == KEYDOWN:
                    kk = pygame.key.get_pressed()
                    if kk[K_ESCAPE]:  # завершение работы при ESC
                        running = False

                if event.type == WINDOWRESIZED:  # перерисовка при изменении размеров окна
                    running = False
                    self.init()
                    self.initSU()
                    self.run()

            # отрисовка
                if running:
                    screen.fill(self.c_main)
                    self.all_sprites.draw(screen)
                    pygame.display.flip()

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


class map_1(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()  # получаем размеры окна сейчас
        w, h = w_n // 40, h_n // 40  # делим (потом будем размещать объекты исходя из этих размеров (пропорционально))
        self.trigger = {Trigger((w * 15, h * 39, w * 10, h * 2)): [map_2, "(w * 19, h * 3, w, h * 2)"]}
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
                     (w * 11, h * 9, w * 17, h * 15),  # прямоугольник посередине
                     (w * 11, h * 24, w * 7, h * 7),  # квадрат левый нижний
                     (w * 21, h * 24, w * 7, h * 7),  # квадрат правый нижний
                     (w * 38, 0, w * 2, h * 40),  # правая полоса
                     ]


class map_2(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((w * 15, 0, w * 10, h * 2)): [map_1, "(w * 19, h * 37, w, h * 2)"]}
        self.c_main = (184, 182, 184)  # цвет_основной
        self.c_sec = (72, 185, 81)  # цвет_второй
        self.gran = [(0, 0, w * 2, h * 40),  # левая полоса
                     (0, 0, w * 15, h * 2),  # верхняя левая
                     (0, h * 38, w_n, h * 4),  # нижняя
                     (w * 25, 0, w * 15, h * 2),  # правая верхняя
                     ]


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
        self.trigger = {Trigger((0, 0, w * 2, h_n)): [map_2, "(w * 37, h * 19, w, h * 2)"]}
        self.c_main = (184, 182, 184)  # цвет_основной
        self.c_sec = (171, 176, 60)  # цвет_второй
        self.gran = [(0, h * 38, w * 15, h * 2),  # нижняя левая
                     (0, 0, w_n, h * 4),  # верхняя
                     (w * 25, h * 38, w * 15, h * 2),  # нижняя правая
                     ]


class map_4(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((w * 38, 0, w * 2, h_n)): [map_2, "(w * 3, h * 19, w, h * 2)"],
                        Trigger((w * 15, 0, w * 10, h * 2)): [map_5, "(w * 19, h * 36, w, h * 2)"],
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
        self.trigger = {Trigger((w * 15, h * 39, w * 10, h * 2)): [map_4, "(w * 19, h * 3, w, h * 2)"],
                        Trigger((0, h * 33, w * 2, h * 5)): [map_6, "(w * 36, h * 34, w, h * 2)"],
                        Trigger((w * 0, h * 20, w * 2, h * 8)): [map_6, "(w * 36, h * 22, w, h * 2)"],
                        Trigger((w * 0, h * 3, w * 2, h * 10)): [map_6, "(w * 37, h * 5, w, h * 2)"]
                        }
        self.c_main = (184, 182, 184)  # цвет_основной
        self.c_sec = (46, 64, 232)  # цвет_второй
        self.gran = [(0, h * 38, w * 15, h * 2),  # нижняя левая
                     (w * 25, h * 38, w * 15, h * 2),  # нижняя правая
                     (0, 0, w * 8, h * 3),
                     (w * 6, 0, w * 2, h * 32),
                     (0, h * 30, w * 8, h * 3),
                     (w * 32, h * 30, w * 8, h * 3),
                     (w * 32, 0, w * 8, h * 3),
                     (w * 32, 0, w * 2, h * 30),
                     (0, h * 13, w * 3, h * 6),
                     (w * 37, h * 13, w * 3, h * 6),
                     (w * 11, 0, w * 2, h * 33),
                     (w * 11, h * 30, w * 18, h * 3),
                     (w * 27, 0, w * 2, h * 33),
                     (w * 15, 0, w, h * 18),
                     (w * 24, 0, w, h * 18),
                     (w * 15, h * 15, w * 10, h * 3),
                     (w * 18, 0, w * 4, h * 4),
                     ]


class map_6(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((w * 39, h * 33, w * 1, h * 5)): [map_5, "(w * 2, h * 34, w, h * 2)"],
                        Trigger((w * 39, h * 19, w * 1, h * 11)): [map_5 , "(w * 2, h * 26, w, h * 2)"],
                        Trigger((w * 39, h * 3, w * 1, h * 10)): [map_5, "(w * 2, h * 6, w, h * 2)"],
                        Trigger((34 * w, 0, w * 3, h * 3)): [map_9, "(w * 35, h * 35, w, h * 2)"],
                        Trigger((w * 18, 0, w * 4, h * 2)): [map_9, "(w * 19, h * 36, w, h * 2)"]}
        self.c_main = (184, 182, 184)  # цвет_основной
        self.c_sec = (46, 64, 232)  # цвет_второй
        self.gran = [(0, 0, w * 2, h * 3),
                     (w * 6, 0, w, h * 13),
                     (0, h * 13, w * 13, h * 6),
                     (w * 11, h * 19, w * 2, h * 21),
                     (w * 6, h * 25, w, h * 13),
                     (0, h * 30, w * 2, h * 3),
                     (0, h * 38, w * 7, h * 2),
                     (w * 16, 0, w * 2, h * 27),
                     (w * 16, h * 27, w, h * 13),
                     (w * 22, 0, w * 2, h * 27),
                     (w * 23, h * 27, w, h * 13),
                     (w * 33, 0, w, h * 13),
                     (w * 27, h * 13, w * 13, h * 6),
                     (w * 38, 0, w * 2, h * 3),
                     (w * 27, h * 19, w * 2, h * 21),
                     (w * 33, h * 25, w, h * 13),
                     (w * 38, h * 30, w * 2, h * 3),
                     (w * 33, h * 38, w * 7, h * 2),
                     (w * 12, 0, w * 4, h * 3),
                     (w * 24, 0, w * 4, h * 3),
                     ]


class map_7(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((w * 0, h * 2, w * 2, h * 9)): [map_8, "(w * 35, h * 3, w, h * 2)"],
                        Trigger((w * 17, 0, w * 6, h * 2)): [map_6, "(w * 18, h * 35, w, h * 2)"]}
        self.c_main = (184, 182, 184)  # цвет_основной
        self.c_sec = (46, 64, 232)  # цвет_второй
        self.gran = [(0, 0, w * 7, h * 2),
                     (w * 33, 0, w * 7, h * 2),
                     (w * 11, 0, w * 2, h * 3),
                     (w * 27, 0, w * 2, h * 3),
                     (w * 6, h * 2, w, h * 11),
                     (w * 33, h * 2, w, h * 11),
                     (w * 16, 0, w, h * 13),
                     (w * 23, 0, w, h * 13),
                     (w * 6, h * 13, w * 11, h * 2),
                     (w * 23, h * 13, w * 11, h * 2),
                     (0, h * 11, w * 3, h * 17),
                     (w * 37, h * 11, w * 3, h * 17),
                     (0, h * 37, w_n, h * 3),
                     (w * 3, h * 24, w * 6, h * 4),
                     (w * 31, h * 24, w * 6, h * 4),
                     (w * 9, h * 24, w * 2, h * 13),
                     (w * 29, h * 24, w * 2, h * 13),
                     ]


class map_8(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((0, h * 29, w * 2, h * 9)): [map_9, "(w * 36, h * 32, w, h * 2)"],
                        Trigger((w * 38, h * 2, w * 2, h * 9)): [map_7, "(w * 4, h * 5, w, h * 2)"]}
        self.c_main = (184, 182, 184)  # цвет_основной
        self.c_sec = (46, 64, 232)  # цвет_второй
        self.gran = [(0, 0, w_n, h * 2),
                     (0, h * 11, w * 3, h * 17),
                     (w * 37, h * 11, w * 3, h * 17),
                     (w * 3, h * 11, w * 6, h * 4),
                     (w * 31, h * 11, w * 6, h * 4),
                     (w * 13, h * 11, w * 14, h * 4),
                     (w * 18, h * 15, w * 4, h * 25),
                     (0, h * 37, h * 6, w * 3),
                     (w * 34, h * 37, h * 6, w * 3),
                     (w * 6, h * 22, w * 2, h * 18),
                     (w * 32, h * 22, w * 2, h * 18),
                     (w * 15, h * 22, w, h * 18),
                     (w * 24, h * 22, w, h * 18),
                     (w * 6, h * 20, w * 10, h * 2),
                     (w * 24, h * 20, w * 10, h * 2),
                     (w * 11, h * 38, w * 2, h * 2),
                     (w * 27, h * 38, w * 2, h * 2)]

class map_9(play):
    def init(self):
        w_n, h_n = pygame.display.get_surface().get_size()
        w, h = w_n // 40, h_n // 40
        self.trigger = {Trigger((w * 34, h * 37, w * 4, h * 3)): [map_6, "(w * 35, h * 3, w, h * 2)"],
                        Trigger((w * 39, h * 28, w, h * 9)): [map_8, "(w * 2, h * 32, w, h * 2)"]}
        self.c_main = (184, 182, 184)  # цвет_основной
        self.c_sec = (46, 64, 232)  # цвет_второй
        self.gran = [(0, 0, w * 12, h * 2),
                     (w * 12, 0, w * 2, h * 8),
                     (w * 12, h * 8, w * 4, h * 4),
                     (w * 28, 0, w * 12, h * 2),
                     (w * 26, 0, w * 2, h * 8),
                     (w * 24, h * 8, w * 4, h * 4),
                     (w * 7, 0, w, h * 22),
                     (w * 32, 0, w, h * 22),
                     (0, h * 11, w * 3, h * 11),
                     (w * 37, h * 11, w * 3, h * 11),
                     (0, h * 22, w * 18, h * 6),
                     (w * 22, h * 22, w * 18, h * 6),
                     (0, h * 37, w * 2, h * 3),
                     (w * 38, h * 37, w * 2, h * 3),
                     (w * 16, h * 28, w * 2, h * 12),
                     (w * 22, h * 28, w * 2, h * 12),
                     (w * 22, h * 28, w * 2, h * 12),
                     (w * 12, h * 37, w * 4, h * 3),
                     (w * 24, h * 37, w * 4, h * 3),
                     (w * 6, h * 28, w, h * 12),
                     (w * 33, h * 28, w, h * 12),
                     ]


start(screen)
pygame.quit()

import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.color_border = pygame.Color(0, 0, 0)  # цвет рамки
        self.colors = [pygame.Color("white"), pygame.Color("blue")]

    def render(self, screen):  # такой способ выбрал, тк он самый гибкий: можно просто добавить цвет в массив
        font = pygame.font.Font(None, 40)
        for y in range(self.height):
            for x in range(self.width):
                a = pygame.draw.rect(screen, self.colors[self.board[y][x] % len(self.colors)], (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size))

                text = font.render(str(x % 10 + 1), True, (100, 100, 100))
                screen.blit(text, (self.left + x * self.cell_size, self.top + y * self.cell_size))
                pygame.draw.rect(screen, self.color_border, (a.x, a.y, a.w, a.h), 1)  # рамка

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


def rev(n):
    return 0 if n == 1 else 1


def main():
    pygame.init()
    size = 1020, 1020
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Создание карты')

    board = Board(40, 40)
    board.set_view(10, 10, 25)
    running = True
    draw = False
    last = ()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                draw = True
            elif event.type == pygame.MOUSEBUTTONUP:
                draw = False
            elif event.type == pygame.MOUSEMOTION and draw:
                x, y = event.pos[0] - board.left, event.pos[1] - board.top
                pp = (None if x > board.cell_size * board.width or
                              y > board.cell_size * board.height else
                      (x // board.cell_size, y // board.cell_size))

                if pp and pp != last:
                    try:
                        board.board[pp[1]][pp[0]] = rev(board.board[pp[1]][pp[0]])
                        last = pp
                    except:
                        pass

        screen.fill((255, 255, 255))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
    print(board.board)


if __name__ == '__main__':
    main()

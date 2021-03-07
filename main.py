import pygame
import sys
import random


WIDTH, HEIGHT = 1200, 750
BIT_WIDTH = 15
FPS = 40

# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED   = (255,0,0)
GREEN = (0,255,0)
BLUE  = (0,0,255)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game of Life')
clock = pygame.time.Clock()


class Bit:
    def __init__(self, x, y, w, color=BLACK, *a, **kw):
        self.x     = x
        self.y     = y
        self.w     = w
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.w])

    def __repr__(self):
        return f'Bit({self.x, self.y})'

board = []
for row in range(0, WIDTH, BIT_WIDTH):
    board_row = []
    for col in range(0, HEIGHT, BIT_WIDTH):
        board_row.append(Bit(row, col, BIT_WIDTH-1))

    board.append(board_row)


def main():
    run = True
    started = False
    global board

    def draw(win):
        win.fill(BLACK)
        for i, row in enumerate(board):
            for j, bit in enumerate(row):
                bit.draw(win)

                number_of_neighbors = 0
                if started:
                    try:
                        neighbors = [board[i][j-1], board[i][j+1], board[i-1][j], board[i+1][j],
                                     board[i-1][j-1], board[i+1][j+1], board[i-1][j+1], board[i+1][j-1]]
                        for neighbor in neighbors:
                            if neighbor.color == GREEN:
                                number_of_neighbors += 1

                    except Exception as e:
                        pass

                    if board[i][j].color == GREEN:
                        if number_of_neighbors == 2 or number_of_neighbors == 3:
                            board[i][j].color = GREEN
                        elif number_of_neighbors < 2:
                            board[i][j].color = BLACK
                        elif number_of_neighbors > 3:
                            board[i][j].color = BLACK
                    else:
                        if number_of_neighbors == 3:
                            board[i][j].color = GREEN

        pygame.display.update()

    while run:
        clock.tick(FPS)
        mouse_state = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            _x = pos[0] // BIT_WIDTH
            _y = pos[1] // BIT_WIDTH

            if mouse_state == (1,0,0):
                board[_x][_y].color = GREEN

            elif mouse_state == (0,0,1):
                board[_x][_y].color = BLACK

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    started = True
                elif event.key == pygame.K_s:
                    started = False
                elif event.key == pygame.K_r:
                    started = False
                    for row in board:
                        for j, bit in enumerate(row):
                            bit.color = BLACK

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit(0)

        draw(WIN)
        pygame.display.update()

if __name__ == '__main__':
    main()


# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import random
import sys

import pygame

size = width, height = 600, 600
cells = (40, 40)
cellsize = (width // cells[0], height // cells[1])
black = 0, 0, 0
red = 255, 0, 0
red_head = 255, 255, 0
green = 0, 255, 0
pygame.display.set_caption("Snake")
screen = pygame.display.set_mode(size)


class Item(object):
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__color = red

    def draw(self):
        pygame.draw.rect(screen, self.__color, (self.__x * cellsize[0], self.__y * cellsize[1],
                                                cellsize[0], cellsize[1]))

    def set_color(self, color):
        self.__color = color

    def set_coord(self, coords):
        self.__x, self.__y = coords

    def get_coord(self):
        return self.__x, self.__y

    def is_collide(self, other):
        return other.get_coord() == (self.__x, self.__y)


class Snake(object):

    def __init__(self):
        item = Item()
        item.set_coord((15, 15))
        item.set_color(red_head)
        self.__snake = [item]
        self.__direction = pygame.K_RIGHT

    def draw(self):
        for item in self.__snake:
            item.draw()

    def change_direction(self, key):
        if key == pygame.K_RIGHT and not self.__direction == pygame.K_LEFT \
                or key == pygame.K_UP and not self.__direction == pygame.K_DOWN \
                or key == pygame.K_DOWN and not self.__direction == pygame.K_UP \
                or key == pygame.K_LEFT and not self.__direction == pygame.K_RIGHT:
            self.__direction = key

    def get_next_pos(self):
        actual = self.get_head().get_coord()
        next = (0, 0)
        if self.__direction == pygame.K_RIGHT:
            next =  actual[0] + 1, actual[1]
        if self.__direction == pygame.K_UP:
            next = actual[0], actual[1] - 1
        if self.__direction == pygame.K_DOWN:
            next = actual[0], actual[1] + 1
        if self.__direction == pygame.K_LEFT:
            next = actual[0] - 1, actual[1]

        next = next[0] % cells[0], next[1] % cells[1]

        return next

    def update(self):
        next_pos = self.get_next_pos()

        for i in range(len(self.__snake) - 1, 0, -1):
            item = self.__snake[i]
            item_next = self.__snake[i - 1]
            item.set_coord(item_next.get_coord())

        self.get_head().set_coord(next_pos)

    def is_collide(self, other):
        return self.get_head().is_collide(other)

    def is_collide_self(self):
        for item in self.__snake[1::]:
            if self.get_head().is_collide(item):
                return True

        return False

    def get_head(self):
        return self.__snake[0]

    def increase(self):
        self.__snake.append(Item())


def main():

    pygame.init()
    pygame.font.init()
    snake = Snake()
    fruit = Item()
    fruit.set_coord((random.randint(0, cells[0] - 1), random.randint(0, cells[1] - 1)))
    fruit.set_color(green)
    clock = pygame.time.Clock()
    myfont = pygame.font.SysFont('Comic Sans MS', 24)
    game_over = False
    points = 0

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.change_direction(event.key)

        if not game_over:
            screen.fill(black)
            snake.draw()
            fruit.draw()
            if snake.is_collide(fruit):
                fruit.set_coord((random.randint(0, cells[0] - 1), random.randint(0, cells[1] - 1)))
                snake.increase()
                points += 100

            snake.update()
            if snake.is_collide_self():
                game_over = True
                textsurface = myfont.render('GameOver', False, (255, 0, 0))
                screen.blit(textsurface, (100, 100))

            textsurface = myfont.render('Points:  ' + str(points), False, (255, 255, 255))
            screen.blit(textsurface, (0, 0))

        clock.tick(20)
        pygame.display.flip()


if __name__ == '__main__':
    main()

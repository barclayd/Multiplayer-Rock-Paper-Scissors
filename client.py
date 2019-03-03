import pygame
from network import Network
# set up

WIDTH = 500
HEIGHT = 500

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
pygame.init()

clientId = 0


# classes
class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.val = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.val

        if keys[pygame.K_RIGHT]:
            self.x += self.val

        if keys[pygame.K_UP]:
            self.y -= self.val

        if keys[pygame.K_DOWN]:
            self.y += self.val

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_position(string):
    string = string.split(",")
    return int(string[0]), int(string[1])


def make_position(tup):
    return str(tup[0]) + "," + str(tup[1])


# functions
def re_draw_window(win, player, player2):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    start_pos = read_position(n.get_pos())
    player = Player(start_pos[0], start_pos[1], 100, 100, (255, 255, 0))
    player2 = Player(0, 0, 100, 100, (255, 0, 0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        # send player 1 coordinates to server
        player2_position = read_position(n.send(make_position((player.x, player.y))))
        # server sends back player 2 coordinates
        # draw player2 with new coordinates
        player2.x = player2_position[0]
        player2.y = player2_position[1]
        player2.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        player.move()
        re_draw_window(win, player, player2)


main()

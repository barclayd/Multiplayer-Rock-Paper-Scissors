import pygame
from network import Network
from player import Player
# set up

WIDTH = 500
HEIGHT = 500

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
pygame.init()


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

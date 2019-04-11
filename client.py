import pygame
from network import Network
pygame.font.init()

# set up
WIDTH = 500
HEIGHT = 500

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, colour):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = 100
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 36)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2)
                        - round(text.get_height()/2)))

    def click(self, position):
        x1 = position[0]
        y1 = position[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


# functions
def re_draw_window(win, player, player2):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


buttons = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (255, 0, 0)),
           Button("Paper", 450, 500, (0, 255, 0))]


def main():
    run = True
    network = Network()
    player = int(network.get_player())
    clock = pygame.time.Clock()
    print("You are player number: {}".format(player))

    while run:
        clock.tick(60)
        try:
            game = network.send("get")
        except:
            run = False
            print("Could not retrieve game from server")
            break

        if game.both_went():
            re_draw_window()
            pygame.time.delay(500)
            try:
                game = network.send("reset")
            except:
                run = False
                print("Could not retrieve game from server")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Win!", 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("You Drew with your Opponent!", 1, (255, 0, 0))
            else:
                text = font.render("You Lose! Better luck next time!", 1, (255, 0, 0))

            win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(position) and game.connected():
                        if player == 0:
                            if not game.p1_went:
                                # check if player has not made a move
                                # if not, send move to server
                                network.send(button.text)
                        else:
                            if not game.p2_went:
                                # check if player has not made a move
                                # if not, send move to server
                                network.send(button.text)

        re_draw_window(win, game, player)


main()

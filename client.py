import pygame
from network import Network
pygame.font.init()

# set up
WIDTH = 700
HEIGHT = 700

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, colour):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = 150
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
def re_draw_window(win, game, player):
    win.fill((255, 255, 255))

    if not(game.connected()):
        # other player is yet to connect
        font = pygame.font.SysFont("comicsans", 36)
        text = font.render("Waiting for both players to connect...", 1, (0, 0, 255), True)
        win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponent's", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.both_went():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            # check if we need to hide opponents move
            if game.p1_went and player == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1_went:
                text1 = font.render("Locked in", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2_went and player == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2_went:
                text2 = font.render("Locked in", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

            # render text on screen

            if player == 1:
                win.blit(text2, (100, 350))
                win.blit(text1, (400, 350))
            else:
                win.blit(text1, (100, 350))
                win.blit(text2, (400, 350))

    for button in buttons:
        button.draw(win)
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
            print('made it passed game')
        except:
            run = False
            print("Could not retrieve game from server - game failed locally")
            break

        if game.both_went():
            re_draw_window(win, game, player)
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
            if event.type == pygame.MOUSEBUTTONUP:
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

from game import Game
from startWindow import StartWindow

if __name__ == '__main__':
    check = True
    while check:
        sw = StartWindow((1000, 600))
        sw.run()
        if sw.data["close"]:
            break
        g = Game((1600, 900), sw.data, sw.game_state)
        g.run()
        check = g.data["new_game"]

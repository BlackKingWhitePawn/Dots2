from game import Game
from startWindow import StartWindow

if __name__ == '__main__':
    sw = StartWindow((200, 200))
    sw.run()
    g = Game((32, 39), (1600, 900), sw.data)
    g.run()

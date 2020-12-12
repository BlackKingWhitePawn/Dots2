from game.game import Game
from runApplication.playerWindow import PlayerWindow
from runApplication.startWindow import StartWindow

if __name__ == '__main__':
    check = True
    while check:
        sw = StartWindow((1000, 600))
        sw.run()
        pw = PlayerWindow(sw.men_images, sw.ai_images)
        if sw.data["close"]:
            break
        if sw.game_state is not None:
            sw.data["n_x"] = len(sw.game_state['matrix'])
            sw.data["n_y"] = len(sw.game_state['matrix'][0])
        else:
            pw.run()
        if pw.back:
            sw.run()
        width = sw.data["n_x"]
        height = sw.data["n_y"]
        actual_res_x = max(sw.data["resolution_set"][0], width * 20 + 600)
        actual_res_y = max(sw.data["resolution_set"][1], height * 20 + 50)
        g = Game((actual_res_x, actual_res_y), sw.data, sw.game_state, pw.player_men, pw.player_bot)
        g.run()
        check = g.data["new_game"]

import go.start
import go.menu

g = go.start.StartGame()

while g.running:
    g.game_loop()

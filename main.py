import go.Start
import go.Menu

g = go.Start.StartGame()

while g.running:
    g.game_loop()

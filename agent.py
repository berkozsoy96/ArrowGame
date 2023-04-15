import game
from random import randint


mygame = game.Game(grid_size=4, value_count=4)
mygame.start_drawing()

while True:
    mygame.click(randint(0, 3), randint(0, 3))
    if mygame.check_win():
        break
mygame.quit()

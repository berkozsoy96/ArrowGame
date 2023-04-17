import game
import numpy as np


mygame = game.Game(grid_size=4, value_count=4)
mygame.start_drawing()
print(np.array(mygame.starting_grid, dtype=game.Tile))
click_count = 0
while True:
    # first n-1 row
    for i in range(mygame.grid_size-1):
        # first n-1 column
        for j in range(mygame.grid_size-1):
            if mygame.grid[i][j].value != 0:
                mygame.pause()
                for _ in range(mygame.value_count - mygame.grid[i][j].value):
                    mygame.click(i+1, j+1)
                    click_count += 1

        # last column
        if mygame.grid[i][3].value != 0:
            mygame.pause()
            for _ in range(mygame.grid[i][3].value):
                mygame.click(i+1, 1)
                click_count += 1
            for _ in range(mygame.value_count - mygame.grid[i][3].value):
                mygame.click(i+1, 0)
                mygame.click(i+1, 3)
                click_count += 2

    # last row
    if mygame.grid[-1][0].value != 0:
        mygame.pause()
        for _ in range(mygame.grid[-1][0].value):
            mygame.click(-3, 0)
            click_count += 1
        for _ in range(mygame.value_count - mygame.grid[-3][0].value):
            mygame.click(0, 0)
            mygame.click(-1, 0)
            click_count += 2
    if mygame.grid[-1][1].value != 0:
        mygame.pause()
        for _ in range(mygame.grid[-1][1].value):
            mygame.click(-3, 2)
            click_count += 1
        for _ in range(mygame.value_count - mygame.grid[-3][2].value):
            mygame.click(0, 2)
            mygame.click(-1, 2)
            click_count += 2
    if mygame.grid[-1][2].value != 0:
        mygame.pause()
        for _ in range(mygame.grid[-1][2].value):
            mygame.click(-3, 3)
            click_count += 1
        for _ in range(mygame.value_count - mygame.grid[-3][3].value):
            mygame.click(0, 3)
            mygame.click(-1, 3)
            click_count += 2
    if mygame.grid[-1][3].value != 0:
        mygame.pause()
        for _ in range(mygame.grid[-1][3].value):
            mygame.click(-3, 3)
            mygame.click(-3, 0)
            click_count += 2
        for _ in range(mygame.value_count - mygame.grid[-3][3].value):
            mygame.click(-3, 1)
            click_count += 1
        for _ in range(mygame.grid[-1][3].value):
            mygame.click(0, 1)
            mygame.click(-1, 1)
            click_count += 2
        for _ in range(mygame.value_count - mygame.grid[-3][3].value):
            mygame.click(0, 0)
            mygame.click(0, -1)
            mygame.click(-1, 0)
            mygame.click(-1, -1)
            click_count += 4
    
    if mygame.check_win():
        mygame.pause()
        break
mygame.quit()
print(f"{click_count = }")
print(mygame.click_counts)
print(np.sum(mygame.click_counts%mygame.value_count))
print(mygame.click_counts%mygame.value_count)

import curses
import time

WIDTH = 10
HEIGHT = 20

TETROMINO = [
  [1, 1],
  [1, 1, 1]
]

def draw(stdscr, field, px, py):
  stdscr.clear()

  for y in range(HEIGHT):
    for x in range(WIDTH):
      if field[y][x]:
        stdscr.addstr(y, x * 2, "[]")

  for y, row in enumerate(TETROMINO):
    for x, cell in enumerate(row):
      if cell:
        stdscr.addstr(py + y, (px + x) * 2, "[]")

  stdscr.refresh()

def can_move(field, px, py):
  for y, row in enumerate(TETROMINO):
    for x, cell in enumerate(row):
      if not cell:
        continue
      nx = px + x
      ny = py + y

      if nx < 0 or nx >= WIDTH or ny >= HEIGHT:
        return False
      if ny >= 0 and field[ny][nx]:
        return False

  return True

def main(stdscr):
  curses.curs_set(0)
  stdscr.nodelay(True)

  field = [[0] * WIDTH for _ in range(HEIGHT)]

  px = WIDTH // 2 - 1
  py = 0

  last_fall = time.time()

  while True:
    key = stdscr.getch()

    if key == ord("q"):
      break

    if key == curses.KEY_LEFT and can_move(field, px - 1, py):
      px -= 1
    if key == curses.KEY_RIGHT and can_move(field, px + 1, py):
      px += 1

    if time.time() - last_fall > 0.5:
      if can_move(field, px, py + 1):
        py += 1
      else:
        for y, row in enumerate(TETROMINO):
          for x, cell in enumerate(row):
            if cell:
              field[py + y][px + x] = 1
        break

      last_fall = time.time()

    draw(stdscr, field, px, py)
    time.sleep(0.02)

curses.wrapper(main)

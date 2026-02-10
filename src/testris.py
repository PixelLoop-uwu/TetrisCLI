from config import Config
from board import Board
from figure import Figure
from shapes import SHAPES

import time
import curses
import random

class Tetris:
  def __init__(self, stdscr):
    self.stdscr = stdscr
    self.board = Board(Config.WIDTH, Config.HEIGHT)
    self.score = 0
    self.cleared = 0
    self.current_figure = None
    self.next_figure = None
    self.game_over = False
    self.fall_speed = 0.5
    self.speed_increase_threshold = Config.SPEED_INCREASE_THRESHOLD
    self.last_fall_time = time.time()
    self.skip_move = False

  def update_fall_speed(self) -> None:
    if self.cleared >= self.speed_increase_threshold:
      self.fall_speed = max(0.05, self.fall_speed - 0.15) 
      self.speed_increase_threshold += 8 

  def spawn_figure(self) -> None:
    shape = SHAPES[random.randint(0, len(SHAPES) - 1)]
    start_x = (Config.WIDTH - len(shape[0])) // 2
    self.current_figure = self.next_figure if self.next_figure else Figure(shape, start_x, 0)
    self.next_figure = Figure(shape, start_x, 0)

    if not self.board.is_valid_move(self.current_figure):
      self.game_over = True

  def hard_drop(self):
    if not self.current_figure:
      return
    dropped = 0
    while self.board.is_valid_move(self.current_figure, dy=1):
      self.current_figure.move(0, 1)
      dropped += 1
    if dropped:
      self.score += dropped * 5
    cleared = self.board.freeze_figure(self.current_figure)
    self.score += cleared * 500
    self.cleared += cleared
    self.spawn_figure()
    self.last_fall_time = time.time()

  def handle_input(self):
    key = self.stdscr.getch()
    if key == ord('q'): self.game_over = True
          
    if key == curses.KEY_LEFT:
      if self.board.is_valid_move(self.current_figure, dx=-1):
        self.current_figure.move(-1, 0)

    elif key == curses.KEY_RIGHT:
      if self.board.is_valid_move(self.current_figure, dx=1):
        self.current_figure.move(1, 0)

    elif key == curses.KEY_DOWN:
      if self.board.is_valid_move(self.current_figure, dy=1):
        self.current_figure.move(0, 1)
        self.skip_move = True
        self.score += 5

    elif key == ord(' '):
      self.hard_drop()

    elif key == curses.KEY_UP:
      old_shape = self.current_figure.shape
      self.current_figure.rotate()
      if not self.board.is_valid_move(self.current_figure):
        self.current_figure.shape = old_shape 


  def update(self):
    if time.time() - self.last_fall_time > self.fall_speed:
      if self.board.is_valid_move(self.current_figure, dy=1):
        if not self.skip_move:
          self.current_figure.move(0, 1)
          self.score += 5
        else: self.skip_move = False
      else:
        cleared = self.board.freeze_figure(self.current_figure)
        self.cleared += cleared
        self.score += cleared * 500
        self.spawn_figure()

      self.last_fall_time = time.time()

  def draw(self):
    self.stdscr.clear()

    # Игровое поле
    for y, row in enumerate(self.board.grid):
      for x, cell in enumerate(row):
        if cell > 0:
          self.stdscr.addstr(y, x * 2, "[]")

        else:
          self.stdscr.addstr(y, x * 2, ".")
          
    # Активная фигура
    if self.current_figure:
      for ry, row in enumerate(self.current_figure.shape):
        for rx, cell in enumerate(row):
          if cell:

            screen_y = self.current_figure.y + ry
            screen_x = (self.current_figure.x + rx) * 2

            if 0 <= screen_y < Config.HEIGHT:
              self.stdscr.addstr(screen_y, screen_x, "[]")

    
    sidebar_x = Config.WIDTH * 2 + 2
    self.stdscr.addstr(0, sidebar_x, f"Score: {self.score}")
    self.stdscr.addstr(1, sidebar_x, "Press 'Q' to Quit")

    self.stdscr.addstr(3, sidebar_x, "Next Figure:")
    if self.next_figure:
      for ry, row in enumerate(self.next_figure.shape):
        for rx, cell in enumerate(row):
          if cell:
            self.stdscr.addstr(5 + ry, sidebar_x + rx * 2 + 2, "[]")

    self.stdscr.refresh()

  def run(self):
    curses.curs_set(0)
    self.stdscr.nodelay(True)
    self.spawn_figure()

    while not self.game_over:
      self.handle_input()   
      self.update()
      self.update_fall_speed()
      self.draw()
      time.sleep(0.02)


if __name__ == "__main__":

    def main(stdscr):
        game = Tetris(stdscr)
        game.run()

    curses.wrapper(main)


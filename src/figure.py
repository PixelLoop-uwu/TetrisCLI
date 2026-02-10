from config import Config

class Figure:
  def __init__(self, shape: list, x: int, y: int):
    self.shape = shape
    self.x = x
    self.y = y

  def rotate(self) -> None:
    """Поворачивает фигуру по часовой стрелке"""
    self.shape = [list(row[::-1]) for row in zip(*self.shape)]

  def move(self, dx, dy) -> None:
    """Сдвигает фигуру на заданное смещение"""
    self.x += dx
    self.y += dy

  # def undo_move(self, dx, dy -> None):
  #   """Отменяет движение (нужно при столкновениях)"""
  #   self.x -= dx
  #   self.y -= dy
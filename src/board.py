from figure import Figure

class Board:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.grid = [[0 for _ in range(width)] for _ in range(height)]

  def is_valid_move(self, figure: Figure, dx: int = 0, dy: int = 0) -> bool:
    """Может ли фигура сдвинуться на указанное расстояние"""
    for y, row in enumerate(figure.shape):
      for x, cell in enumerate(row):
        if not cell:
          continue

        new_x = figure.x + x + dx
        new_y = figure.y + y + dy

        if new_x < 0 or new_x >= self.width or new_y >= self.height:
          return False

        if new_y >= 0 and self.grid[new_y][new_x] != 0:
          return False

    return True
    
  def freeze_figure(self, figure) -> int:
    """Копирует блоки фигуры в сетку поля"""
    for ry, row in enumerate(figure.shape):
      for rx, cell in enumerate(row):
        if cell:
          new_y = figure.y + ry
          new_x = figure.x + rx
          if 0 <= new_y < self.height and 0 <= new_x < self.width:
            self.grid[new_y][new_x] = 1

    return self.clear_lines() 
    
  def clear_lines(self) -> int:
    """Проверяет наличие заполненных строк и при обнаружении добавляет новые в начало сетки"""
    new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
    lines_cleared = self.height - len(new_grid)

    for _ in range(lines_cleared):
      new_grid.insert(0, [0 for _ in range(self.width)])

    self.grid = new_grid
    return lines_cleared
import yaml
import os
from pathlib import Path

class Config:
  WIDTH: int 
  HEIGHT: int
  SPEED_INCREASE_THRESHOLD: int
  
  _DEFAULTS = {
    'WIDTH': 10,
    'HEIGHT': 14,
    'SPEED_INCREASE_THRESHOLD': 8,
  }
  
  _CONFIG_PATH = Path(__file__).parent.parent / 'config.yaml'
  
  @classmethod
  def _create_default_config(self) -> None:
    self._CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(self._CONFIG_PATH, 'w') as f:
      yaml.dump(self._DEFAULTS, f, default_flow_style=False)
  
  @classmethod
  def load(self) -> None:
    """Загружает конфиг из YAML, создаёт если не существует"""
    if not self._CONFIG_PATH.exists() or self._CONFIG_PATH.stat().st_size == 0:
      self._create_default_config()
    
    try:
      with open(self._CONFIG_PATH, 'r') as f:
        config_data = yaml.safe_load(f)
      
      if config_data:
        for key, value in config_data.items():
          setattr(self, key, value)
    except Exception as e:
      print(f"Ошибка загрузки конфига: {e}, используются дефолтные значения")


Config.load()

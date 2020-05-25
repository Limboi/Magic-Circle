from enum import Enum


class GameStates(Enum):
	STANDART = 0
	PLAYER_DEAD = 1
	SHOW_INVENTORY = 2
	DROP_INVENTORY = 3
	TARGETING = 4
	HELP = 5
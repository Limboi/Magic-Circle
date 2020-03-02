import random
import tcod as libtcod

from map.tiles import Tile
from map.terrain_gen import generate_terrain, generate_test_arena
from entities import Humanoid
from components.combat import Fighter
from components.ai import BasicMonster, Player


class GameMap:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.tiles = self.initialize_tiles()


	def initialize_tiles(self):
		tiles = [[Tile("rock_wall") for y in range(self.width)] for x in range(self.height)]
		return tiles


	def create_map(self, seed):
		#pre_map = generate_terrain(self.width, self.height, seed)
		pre_map = generate_test_arena(self.width, self.height)
		for i in range( self.height):
			for j in range( self.width ):
				self.tiles[i][j] = Tile( pre_map[i][j])


	def place_entities_test(self, entities, number):
		random.seed()

		player = Humanoid(int(self.width / 2), int(self.height / 2), '@', libtcod.white, 'Player', 
			blocks = True, combat_aspect = Fighter(3000,5,10), ai = Player())
		entities.append(player)

		for i in range(number):
			x = random.randint(1, self.width - 1)
			y = random.randint(1, self.height - 1)

			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				monster = Humanoid(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks = True, 
					combat_aspect = Fighter(20,0,10), ai = BasicMonster())

			entities.append(monster)
		

	def is_blocked(self, x, y):
			if self.tiles[y][x].blocked:
				return True
			else:
				return False



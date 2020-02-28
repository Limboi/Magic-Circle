import random
from map.tiles import Tile
from map.terrain_gen import generate_terrain, generate_test_arena


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


	def place_entities(self):
		pass
		

	def is_blocked(self, x, y):
			if self.tiles[y][x].blocked:
				return True
			else:
				return False



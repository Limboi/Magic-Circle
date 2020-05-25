import random
import tcod as libtcod

from map.tiles import Tile
from map.terrain_gen import generate_terrain, generate_test_arena
from entities import Humanoid, Item, StationaryEffect
from components.combat import Combatant
from components.inventory import Inventory
from components.item import Item_aspect, heal, cast_fireball
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
		pre_map = generate_terrain(self.width, self.height, seed)
		#pre_map = generate_test_arena(self.width, self.height)
		for i in range( self.height):
			for j in range( self.width ):
				self.tiles[i][j] = Tile( pre_map[i][j])


	def place_entities_test(self, entities, number_of_enemies, number_of_items, player = None):
		random.seed()

		if player == None:
			player = Humanoid(int(self.width / 2), int(self.height / 2), '@', libtcod.white, 'Player', 
				blocks = True, combat_aspect = Combatant(200, 20, 20, 15), ai = Player(), speed = 20, inventory = Inventory(20))

		entities.append(player)

		for i in range(number_of_enemies):
			x = random.randint(1, self.width - 1)
			y = random.randint(1, self.height - 1)

			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				monster = Humanoid(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks = True, 
					combat_aspect = Combatant(100, 10, 10, 5), ai = BasicMonster())

			entities.append(monster)

		for i in range(number_of_items):
			x = random.randint(1, self.width - 1)
			y = random.randint(1, self.height - 1)

			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				if random.randint(1,100) < 0:
					item = Item(x, y, '!', libtcod.violet, 'Healing Potion', item_aspect = Item_aspect(use_function=heal, amount=10))
				elif random.randint(1,100) < 70:
					item = Item(x, y, '=', libtcod.red, 'Fireball Scroll', 
								item_aspect = Item_aspect(use_function=cast_fireball, targeting=True, targeting_message=
								'Left-click a target tile for the fireball, or right-click to cancel.', damage=50, radius=3))
				else:
					pass
				try:
					entities.append(item)
				except:
					pass

			else:
				i -= 1
				


	def place_entities(self, entities, number_of_enemies, number_of_items, player = None):
		random.seed()

		x = random.randint(2, self.width - 2)
		y = random.randint(2, self.height - 2)
		while self.is_blocked(x,y):
			x = random.randint(2, self.width - 2)
			y = random.randint(2, self.height - 2)
			
		if player == None:
			player = Humanoid(x, y, '@', libtcod.white, 'Player', 
				blocks = True, combat_aspect = Combatant(200, 20, 20, 15), ai = Player(), speed = 20, inventory = Inventory(20))

		entities.append(player)

		for i in range(number_of_enemies):
			x = random.randint(2, self.width - 2)
			y = random.randint(2, self.height - 2)
			while self.is_blocked(x,y):
				x = random.randint(2, self.width - 2)
				y = random.randint(2, self.height - 2)

			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				monster = Humanoid(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks = True, 
					combat_aspect = Combatant(100, 10, 10, 5), ai = BasicMonster())

			entities.append(monster)

		for i in range(number_of_items):
			x = random.randint(2, self.width - 2)
			y = random.randint(2, self.height - 2)
			while self.is_blocked(x,y):
				x = random.randint(2, self.width - 2)
				y = random.randint(2, self.height - 2)

			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				if random.randint(1,100) < 50:
					item = Item(x, y, '!', libtcod.violet, 'Healing Potion', item_aspect = Item_aspect(use_function=heal, amount=10))
				elif random.randint(1,100) < 70:
					item = Item(x, y, '=', libtcod.red, 'Fireball Scroll', 
								item_aspect = Item_aspect(use_function=cast_fireball, targeting=True, targeting_message=
								'Left-click a target tile for the fireball, or right-click to cancel.', damage=50, radius=3))
				else:
					pass
				try:
					entities.append(item)
				except:
					pass

			else:
				i -= 1
		

	def is_blocked(self, x, y):
			if self.tiles[y][x].blocked:
				return True
			else:
				return False



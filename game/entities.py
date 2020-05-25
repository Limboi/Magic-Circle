from abc import ABC, abstractmethod
import math
import tcod as libtcod
from rendering import RenderOrder



class Entity(ABC):
	def __init__(self, x, y):
		self.x, self.y = x, y



class Self_moving(Entity):
	def __init__(self, x, y, energy):
		self.x, self.y = x, y
		self.energy = energy


	def move(self, dx, dy):
		if abs(dx) == abs(dy) and self.energy >= 141:
			self.x += dx
			self.y += dy
			self.energy = 0
			return True

		elif self.energy >= 100:
			self.x += dx
			self.y += dy
			self.energy = 0
			return True

		else:
			return False


	def move_towards(self, target_x, target_y, nav_map, entities):
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		dx = int(round(dx / distance))
		dy = int(round(dy / distance))

		if not get_blocking_entities_at_location(entities, self.x + dx, self.y + dy):
			self.move(dx, dy)


	def distance_to(self, other):
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)

	def distance_to_point(self,x,y):
		dx = x - self.x
		dy = y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)


	def move_astar(self, target_x, target_y, entities, nav_map):
		for entity in entities:
			if entity.blocks and entity != self and entity.x != target_x and entity.y != target_y:
				libtcod.map_set_properties(nav_map, entity.x, entity.y, True, False)

		my_path = libtcod.path_new_using_map(nav_map, 1.41)
		libtcod.path_compute(my_path, self.x, self.y, target_x, target_y)

		if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
			x, y = libtcod.path_walk(my_path, True)
			if x or y:
				if abs(x) == abs(y) and self.energy >= 141:
					self.x = x
					self.y = y
					self.energy = 0

				elif self.energy >= 100:
					self.x = x
					self.y = y
					self.energy = 0
		else:
			self.move_towards(target_x, target_y, nav_map, entities)

			# Delete the path to free memory
		libtcod.path_delete(my_path)



	def give_energy(self, energy):
		self.energy += energy



class Humanoid(Self_moving):
	def __init__(self, x, y, char, color, name, energy = 0, speed = 10, render_order = RenderOrder.ACTOR, 
		blocks = False, combat_aspect = None, item_aspect = None, ai = None, inventory = None):

		self.x, self.y = x, y
		self.char = char
		self.color = color
		self.name = name
		self.energy = energy
		self.speed = speed
		self.render_order = render_order
		self.blocks = blocks
		self.combat_aspect = combat_aspect
		self.item_aspect = item_aspect
		self.ai = ai
		self.inventory = inventory

		if self.combat_aspect:
			self.combat_aspect.owner = self

		if self.item_aspect:
			self.item_aspect.owner = self

		if self.ai:
			self.ai.owner = self

		if self.inventory:
			self.inventory.owner = self



def get_blocking_entities_at_location(entities, destination_x, destination_y):
	for entity in entities:
		if entity.blocks and entity.x == destination_x and entity.y == destination_y:
			return entity

	return None



class Item(Entity):
	def __init__(self, x, y, char, color, name, render_order = RenderOrder.ITEM, 
		blocks = False, combat_aspect = None, item_aspect = None, ai = None):

		self.x, self.y = x, y
		self.char = char
		self.color = color
		self.name = name
		self.render_order = render_order
		self.blocks = blocks
		self.combat_aspect = combat_aspect
		self.item_aspect = item_aspect
		self.ai = ai

		if self.combat_aspect:
			self.combat_aspect.owner = self

		if self.item_aspect:
			self.item_aspect.owner = self

		if self.ai:
			self.ai.owner = self

	def distance_to_point(self,x,y):
		dx = x - self.x
		dy = y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)



class StationaryEffect(Entity):
	def __init__(self, x, y, char, color, name, amount, lifetime = None, render_order = RenderOrder.EFFECT):

		self.x, self.y = x, y
		self.char = char
		self.color = color
		self.name = name
		self.amount = amount
		self.lifetime = lifetime
		self.render_order = render_order

	def distance_to_point(self,x,y):
		dx = x - self.x
		dy = y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)



def superimpose_effect(effect, all_effects):
	if all_effects:
		for old_effect in all_effects:
			if (effect.x == old_effect.x) and (effect.y == old_effect.y) and (effect.name == old_effect.name):
				old_effect.amount += effect.amount
				return all_effects
	all_effects.append(effect)
	return all_effects



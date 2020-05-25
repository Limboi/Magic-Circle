import tcod as libtcod

class Item_aspect:
	def __init__(self, use_function=None, targeting = False, targeting_message = None, **kwargs):
		self.use_function = use_function
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.function_kwargs = kwargs


def heal(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount')

	results = []

	if entity.combat_aspect.hp == entity.combat_aspect.max_hp:
		results.append({'consumed': False, 'message': 'You are already at full health'})
	else:
		entity.combat_aspect.heal(amount)
		results.append({'consumed': True, 'message': 'Your wounds start to feel better!'})

	return results


def cast_fireball(*args, **kwargs):
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	damage = kwargs.get('damage')
	radius = kwargs.get('radius')
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')

	results = []

	if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
		results.append({'consumed': False, 'message': 'You cannot target a tile outside your field of view.'})
		return results

	results.append({'consumed': True, 'message': 'The fireball explodes, burning everything within {0} tiles!'.format(radius)})

	for entity in entities:
		if entity.distance_to_point(target_x, target_y) <= radius and entity.combat_aspect:
			results.append({'message': 'The {0} gets burned for {1} hit points.'.format(entity.name, damage)})
			results.extend(entity.combat_aspect.take_damage(damage, 'burn', True))

	return results
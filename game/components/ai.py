import tcod as libtcod
from input_handlers import handle_keys
from entities import get_blocking_entities_at_location
from game_states import GameStates


class Player:
	def take_action(self, action, game_map, entities, game_state):
		player = self.owner
		results = []

		move = action.get('move')
		exit = action.get('exit')
		fullscreen = action.get('fullscreen')

		if game_state != GameStates.PLAYER_DEAD:
			if move:
				dx, dy = move
				dest_x = player.x + dx
				dest_y = player.y + dy

				if not game_map.is_blocked(dest_x, dest_y):
					target = get_blocking_entities_at_location(entities, dest_x, dest_y)

					if target:
						attack_results = player.combat_aspect.attack(target)
						results.extend(attack_results)
					else:
						if player.move(dx, dy):
							results.append({'fov_recompute': True})
						else:
							results.append({'not_enough_energy': True})
				else:
					results.append({})

		if exit:
			results.append({'exit': True})

		if fullscreen:
			results.append({'fullscreen': True})

		return results





class BasicMonster:
	def __init__(self, fov_recompute = True, seen_target = None):
		self.fov_recompute = fov_recompute
		self.seen_target = seen_target 


	def take_action(self, nav_map, entities):
		results = []
		target = None

		monster = self.owner

		libtcod.map_compute_fov(nav_map, monster.x, monster.y, 10, True, 0)
		self.fov_recompute = False

		for entity in entities:
			if entity.ai.__class__.__name__== 'Player' and libtcod.map_is_in_fov(nav_map, entity.x, entity.y):
				target = entity
				self.seen_target = (target.x, target.y)

		if target:
			if monster.distance_to(target) >= 2:
				monster.move_astar(target.x, target.y, entities, nav_map)
				#monster.move_towards(target.x,target.y,game_map,entities)

			elif target.combat_aspect.hp > 0:
				attack_results = monster.combat_aspect.attack(target)
				results.extend(attack_results)

		elif self.seen_target:
			if (monster.x, monster.y) != self.seen_target:
				x,y = self.seen_target
				monster.move_astar(x, y, entities, nav_map)
			else:
				self.seen_target = None

		return results
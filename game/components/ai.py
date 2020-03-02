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
	def take_action(self, target, fov_map, game_map, entities):
		results = []

		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

			if monster.distance_to(target) >= 2:
				#monster.move_astar(target, entities, game_map)
				monster.move_towards(target.x,target.y,game_map,entities)

			elif target.combat_aspect.hp > 0:
				attack_results = monster.combat_aspect.attack(target)
				results.extend(attack_results)

		return results

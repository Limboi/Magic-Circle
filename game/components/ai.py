import tcod as libtcod
from input_handlers import handle_keys
from entities import get_blocking_entities_at_location
from game_states import GameStates


class Player:
	def take_action(self, action, m_action, game_map, fov_map, entities, game_state, targeting_item):
		player = self.owner
		results = []

		move = action.get('move')
		pickup = action.get('pickup')
		show_inventory = action.get('show_inventory')
		drop_inventory = action.get('drop_inventory')
		inventory_index = action.get('inventory_index')
		left_click = m_action.get('left_click')
		right_click = m_action.get('right_click')
		show_help = action.get('show_help')
		exit = action.get('exit')
		fullscreen = action.get('fullscreen')
		toggle_realtime = action.get('toggle_realtime')
		go_deeper = action.get('go_deeper')

		if game_state == GameStates.STANDART:
			if move:
				dx, dy = move
				dest_x = player.x + dx
				dest_y = player.y + dy

				if not game_map.is_blocked(dest_x, dest_y):
					target = get_blocking_entities_at_location(entities, dest_x, dest_y)

					if target:
						attack_results = player.combat_aspect.attack(target, 'cut')
						results.extend(attack_results)
					else:
						if player.move(dx, dy):
							results.append({'fov_recompute': True})
						else:
							results.append({'not_enough_energy': True})
				else:
					results.append({})

			if pickup:
				for entity in entities:
					if entity.item_aspect and entity.x == player.x and entity.y == player.y:
						pickup_results = player.inventory.add_item(entity)
						results.extend(pickup_results)

						break
				else:
					results.append({'message':'There is nothing here to pick up.'})

		if game_state == GameStates.TARGETING:
			if left_click:
				target_x, target_y = left_click
				item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
														target_x=target_x, target_y=target_y)
				results.extend(item_use_results)
				results.append({'exit': True})
			elif right_click:
				results.append({'exit': True})

		if exit:
			results.append({'exit': True})

		if fullscreen:
			results.append({'fullscreen': True})

		if show_inventory:
			results.append({'show_inventory': True})

		if drop_inventory:
			results.append({'drop_inventory': True})

		if inventory_index != None and game_state == GameStates.SHOW_INVENTORY:
			if inventory_index is not None and inventory_index < len(player.inventory.items):
				item = player.inventory.items[inventory_index]
				results.extend(player.inventory.use(item))

		if inventory_index != None and game_state == GameStates.DROP_INVENTORY:
			if inventory_index is not None and inventory_index < len(player.inventory.items):
				item = player.inventory.items[inventory_index]
				results.extend(player.inventory.drop_item(item))

		if show_help:
			results.append({'show_help': True})

		if toggle_realtime:
			results.append({'toggle_realtime': True})

		if go_deeper:
			results.append({'go_deeper': True, 'fov_recompute': True})

		results.extend(player.combat_aspect.update_combatant_state())

		return results





class BasicMonster:
	def __init__(self, fov_recompute = True, seen_target = None):
		self.fov_recompute = fov_recompute
		self.seen_target = seen_target 


	def take_action(self, nav_map, entities, game_state):
		results = []
		target = None

		monster = self.owner

		if game_state == GameStates.STANDART:
			libtcod.map_compute_fov(nav_map, monster.x, monster.y, 10, True, 0)
			#self.fov_recompute = False

			for entity in entities:
				if entity.ai.__class__.__name__== 'Player' and libtcod.map_is_in_fov(nav_map, entity.x, entity.y):
					target = entity
					self.seen_target = (target.x, target.y)

			if target:
				if monster.distance_to(target) >= 2:
					monster.move_astar(target.x, target.y, entities, nav_map)

				elif target.combat_aspect.active:
					attack_results = monster.combat_aspect.attack(target, 'cut')
					results.extend(attack_results)

			elif self.seen_target:
				if (monster.x, monster.y) != self.seen_target:
					x,y = self.seen_target
					monster.move_astar(x, y, entities, nav_map)
				else:
					self.seen_target = None

			results.extend(monster.combat_aspect.update_combatant_state())

		return results
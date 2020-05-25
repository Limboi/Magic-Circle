import tcod as libtcod

from input_handlers import handle_keys, is_valid_input, handle_mouse
from entities import Humanoid, get_blocking_entities_at_location, superimpose_effect
from map.game_map import GameMap
from rendering import clear_all, render_all
from fov_calculation import initialize_fov, recompute_fov
from game_states import GameStates
from death_functions import kill_monster, kill_player
from game_messages import Message, MessageLog


def main():
	screen_width = 80
	screen_height = 80

	bar_width = 20
	panel_height = 10
	panel_y = screen_height - panel_height

	map_width = 80
	map_height = 80 - panel_height

	message_x = bar_width + 2
	message_width = screen_width - bar_width - 2
	message_height = panel_height - 1

	fov_algorithm = 0
	fov_light_walls = True
	fov_radius = 10
	fov_recompute = True

	colors = 0

	entities = []
	items = []
	effects = []

	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	libtcod.console_init_root(screen_width, screen_height, 'Project Magic Circle', False)

	con = libtcod.console_new(screen_width, screen_height)
	panel = libtcod.console_new(screen_width, panel_height)

	seed = 1000

	map = GameMap(map_width, map_height)
	map.create_map(seed)
	fov_map = initialize_fov(map)
	nav_map = initialize_fov(map)
	nav_map_recompute = False
	message_log = MessageLog(message_x, message_width, message_height)

	map.place_entities(entities, 5, 5)
	player = entities[0]

	key = libtcod.Key()
	mouse = libtcod.Mouse()

	game_state = GameStates.STANDART
	realtime = False
	action_buffer = None

	message = Message('To get help press "?"', libtcod.white)
	message_log.add_message(message)
	targeting_item = None
	danger_level = 1

	while not libtcod.console_is_window_closed():
		if nav_map_recompute:
			fov_map = initialize_fov(map)
			nav_map = initialize_fov(map)
			fov_recompute = True
			nav_map_recompute = False

		if fov_recompute:
			recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)		

		render_all(con, panel, entities, effects, map, fov_map, fov_radius, fov_recompute, message_log,
					screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state)
		fov_recompute = False
		libtcod.console_flush()
		clear_all(con, entities+effects)

		for entity in entities:
			try:
				entity.give_energy( int(entity.speed/5) )
			except:
				pass

		for entity in entities:
			if entity == player:

				if action_buffer == None:
					if realtime:
						libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS or libtcod.EVENT_MOUSE, key, mouse)
					else:
						while True:
							libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS or libtcod.EVENT_MOUSE, key, mouse)
							render_all(con, panel, entities, effects, map, fov_map, fov_radius, fov_recompute, message_log,
											screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state)
							libtcod.console_flush()
							clear_all(con, entities)
							if is_valid_input(key, mouse):
								break
					keys_action = handle_keys(key, game_state)
					mouse_action = handle_mouse(mouse, game_state)
					action_buffer = (keys_action, mouse_action)

				if game_state != GameStates.TARGETING:
					targeting_item = None
				turn_results = entity.ai.take_action(action_buffer[0], action_buffer[1], map, fov_map, entities, game_state, targeting_item)
				
				if turn_results:
					for turn_result in turn_results:
							message = turn_result.get('message')
							dead_entity = turn_result.get('dead')
							fov_recompute = turn_result.get('fov_recompute')
							energy = turn_result.get('not_enough_energy')
							exit = turn_result.get('exit')
							fullscreen = turn_result.get('fullscreen')
							effect = turn_result.get('create effect')
							item_added = turn_result.get('item_added')
							item_dropped = turn_result.get('item_dropped')
							show_inventory = turn_result.get('show_inventory')
							drop_inventory = turn_result.get('drop_inventory')
							targeting = turn_result.get('targeting')
							show_help = turn_result.get('show_help')
							toggle_realtime = turn_result.get('toggle_realtime')
							go_deeper = turn_result.get('go_deeper')


							if message:
								message = Message(message, libtcod.white)
								message_log.add_message(message)

							if dead_entity:
								if dead_entity == player:
									message, game_state = kill_player(dead_entity)
									message = Message(message, libtcod.red)
								else:
									message = kill_monster(dead_entity)
									message = Message(message, libtcod.white)
								message_log.add_message(message)

							if effect:
								superimpose_effect(effect, effects)

							if energy == None:
								action_buffer = None

							if fov_recompute == None:
								fov_recompute = False

							if item_added:
								entities.remove(item_added)

							if show_inventory:
								previous_game_state = game_state
								game_state = GameStates.SHOW_INVENTORY

							if drop_inventory:
								previous_game_state = game_state
								game_state = GameStates.DROP_INVENTORY

							if item_dropped:
								entities.append(item_dropped)

							if targeting:
								targeting_item = targeting
								message = Message(targeting_item.item_aspect.targeting_message, libtcod.yellow)
								message_log.add_message(message)
								previous_game_state = GameStates.STANDART
								game_state = GameStates.TARGETING

							if exit:
								if game_state in {GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, 
												GameStates.TARGETING, GameStates.HELP}:
									if game_state == GameStates.TARGETING:
										message = Message('Exited targeting', libtcod.yellow)
										message_log.add_message(message)
									game_state = previous_game_state
								else:
									return True

							if fullscreen:
								libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

							if show_help:
								previous_game_state = game_state
								game_state = GameStates.HELP

							if toggle_realtime:
								message = Message('Gamemode changed', libtcod.green)
								message_log.add_message(message)
								realtime = not realtime

							if go_deeper:
								'''clear_all(con, entities)
								items = []
								effects = []
								map = GameMap(map_width, map_height)
								map.initialize_tiles()
								map.create_map(seed+danger_level)
								fov_map = initialize_fov(map)
								nav_map = initialize_fov(map)
								map.place_entities(entities, 5+danger_level, 5+danger_level, player = player)
								player = entities[0]
								danger_level += 2'''
								pass


				else:
					action_buffer = None

			else:
				if entity.ai:
					turn_results = entity.ai.take_action(nav_map, entities, game_state)

					if turn_results:
						for turn_result in turn_results:
								message = turn_result.get('message')
								dead_entity = turn_result.get('dead')
								exit = turn_result.get('exit')
								fullscreen = turn_result.get('fullscreen')
								effect = turn_result.get('create effect')

								if message:
									message = Message(message, libtcod.white)
									message_log.add_message(message)

								if dead_entity:
									if dead_entity == player:
										message, game_state = kill_player(dead_entity)
										message = Message(message, libtcod.red)
									else:
										message = kill_monster(dead_entity)
										message = Message(message, libtcod.white)
									message_log.add_message(message)

								if effect:
									superimpose_effect(effect, effects)

								if game_state == GameStates.PLAYER_DEAD:
									break





if __name__ == '__main__':
	 main()
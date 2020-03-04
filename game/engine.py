import tcod as libtcod

from input_handlers import handle_keys
from entities import Humanoid, get_blocking_entities_at_location
from map.game_map import GameMap
from rendering import clear_all, render_all
from fov_calculation import initialize_fov, recompute_fov
from game_states import GameStates
from death_functions import kill_monster, kill_player


def main():
	screen_width = 80
	screen_height = 80
	map_width = 50
	map_height = 50

	fov_algorithm = 0
	fov_light_walls = True
	fov_radius = 100
	fov_recompute = True

	colors = {
		'dark_rock_wall': libtcod.Color(0, 0, 50),
		'dark_rock_floor': libtcod.Color(30, 30, 80),
		'dark_chasm': libtcod.Color(30,30,30),
		'dark_smooth_floor': libtcod.Color(100, 50, 150),
		'dark_fort_wall': libtcod.Color(40, 0, 0),

		'light_rock_wall': libtcod.Color(130, 110, 50),
		'light_rock_floor': libtcod.Color(200, 180, 50),
		'light_chasm': libtcod.Color(50,50,50),
		'light_smooth_floor': libtcod.Color(255, 120, 0),
		'light_fort_wall': libtcod.Color(200, 20, 20)
	}

	entities = []

	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	libtcod.console_init_root(screen_width, screen_height, 'Project Magic Circle', False)
	con = libtcod.console_new(screen_width, screen_height)

	map = GameMap(map_width, map_height)
	map.create_map(547)
	fov_map = initialize_fov(map)
	nav_map = initialize_fov(map)
	nav_map_recompute = False
	map.place_entities_test(entities, 10)

	player = entities[0]

	key = libtcod.Key()
	mouse = libtcod.Mouse()

	game_state = 0
	realtime = False
	action_buffer = None

	while not libtcod.console_is_window_closed():
		if nav_map_recompute:
			fov_map = initialize_fov(map)
			nav_map = initialize_fov(map)
			fov_recompute = True
			nav_map_recompute = False

		if fov_recompute:
			recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)		

		render_all(con, entities, map, fov_map, fov_radius, fov_recompute, screen_width, screen_height, colors)
		fov_recompute = False
		libtcod.console_flush()
		clear_all(con, entities)

		for entity in entities:
			entity.give_energy( int(entity.speed/5) )

		for entity in entities:
			if entity == player:

				if action_buffer == None:
					if realtime:
						libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
					else:
						libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key, mouse, True)
					action = handle_keys(key)
					action_buffer = action

				turn_results = entity.ai.take_action(action_buffer, map, entities, game_state)

				if turn_results:
					for turn_result in turn_results:
							message = turn_result.get('message')
							dead_entity = turn_result.get('dead')
							fov_recompute = turn_result.get('fov_recompute')
							energy = turn_result.get('not_enough_energy')
							exit = turn_result.get('exit')
							fullscreen = turn_result.get('fullscreen')


							if message:
								print(message)

							if dead_entity:
								if dead_entity == player:
									message, game_state = kill_player(dead_entity)
								else:
									message = kill_monster(dead_entity)
								print(message)

							if energy == None:
								action_buffer = None

							if fov_recompute == None:
								fov_recompute = False

							if exit:
								return True

							if fullscreen:
								libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
				else:
					action_buffer = None

			else:
				if entity.ai:
					turn_results = entity.ai.take_action(nav_map, entities)

					if turn_results:
						for turn_result in turn_results:
								message = turn_result.get('message')
								dead_entity = turn_result.get('dead')
								exit = turn_result.get('exit')
								fullscreen = turn_result.get('fullscreen')

								if message:
									print(message)

								if dead_entity:
									if dead_entity == player:
										message, game_state = kill_player(dead_entity)
									else:
										message = kill_monster(dead_entity)

									print(message)

								if game_state == GameStates.PLAYER_DEAD:
									break





if __name__ == '__main__':
	 main()
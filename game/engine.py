import tcod as libtcod

from entities import Humanoid
from input_handlers import handle_keys
from map.game_map import GameMap
from rendering import clear_all, render_all
from fov_calculation import initialize_fov, recompute_fov


def main():
	screen_width = 80
	screen_height = 80
	map_width = 80
	map_height = 80

	fov_algorithm = 0
	fov_light_walls = True
	fov_radius = 100
	fov_recompute = True

	colors = {
		'dark_rock_wall': libtcod.Color(0, 0, 100),
		'dark_rock_floor': libtcod.Color(50, 50, 150),
		'dark_chasm': libtcod.Color(30,30,30),
		'dark_smooth_floor': libtcod.Color(100, 50, 150),
		'dark_fort_wall': libtcod.Color(40, 0, 0),

		'light_rock_wall': libtcod.Color(130, 110, 50),
		'light_rock_floor': libtcod.Color(200, 180, 50),
		'light_chasm': libtcod.Color(50,50,50),
		'light_smooth_floor': libtcod.Color(255, 120, 0),
		'light_fort_wall': libtcod.Color(200, 20, 20)
	}

	player = Humanoid(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
	entities = [player]

	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	libtcod.console_init_root(screen_width, screen_height, 'Project Magic Circle', False)
	con = libtcod.console_new(screen_width, screen_height)

	map = GameMap(map_width, map_height)
	map.create_map(547)
	fov_map = initialize_fov(map)

	key = libtcod.Key()
	mouse = libtcod.Mouse()

	while not libtcod.console_is_window_closed():
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

		if fov_recompute:
			recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

		render_all(con, entities, map, fov_map, fov_recompute, screen_width, screen_height, colors)
		libtcod.console_flush()
		clear_all(con, entities)

		action = handle_keys(key)

		move = action.get('move')
		exit = action.get('exit')
		fullscreen = action.get('fullscreen')

		if move:
			dx, dy = move

			if not map.is_blocked(player.x + dx, player.y + dy):
				player.move(dx, dy)
				fov_recompute = True

		if exit:
			return True

		if fullscreen:
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
	 main()
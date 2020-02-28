import tcod as libtcod


def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
	if fov_recompute:
		for y in range(game_map.height):
			for x in range(game_map.width):
				visible = libtcod.map_is_in_fov(fov_map, x, y)

				if visible:
					color = 'light_' + game_map.tiles[y][x].name
					libtcod.console_set_char_background(con, x, y, colors.get(color), libtcod.BKGND_SET)
					game_map.tiles[y][x].explored = True

				elif game_map.tiles[y][x].explored == True:
					color = 'dark_' + game_map.tiles[y][x].name
					libtcod.console_set_char_background(con, x, y, colors.get(color), libtcod.BKGND_SET)

	for entity in entities:
		draw_entity(con, entity)

	libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
	for entity in entities:
		clear_entity(con, entity)


def draw_entity(con, entity):
	libtcod.console_set_default_foreground(con, entity.color)
	libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
	libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
import tcod as libtcod
from enum import Enum
import math
from game_states import GameStates
from menus import inventory_menu, help_menu

class RenderOrder(Enum):
	EFFECT = 1
	CORPSE = 2
	ITEM = 3
	OBJECT = 4
	ACTOR = 5


def render_all(con, panel, entities, effects, game_map, fov_map, fov_radius, fov_recompute, message_log,
	screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state):

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


	for entity in entities:
		if entity.ai.__class__.__name__== 'Player':
			player = entity
			break

	if fov_recompute:
		for y in range(game_map.height):
			for x in range(game_map.width):
				visible = libtcod.map_is_in_fov(fov_map, x, y)

				if visible:
					color = 'light_' + game_map.tiles[y][x].name
					hue = math.sqrt((player.x - x)**2 + (player.y - y)**2) / (fov_radius * 1.5)
					libtcod.console_set_char_background(con, x, y, colors.get(color) * (1-hue), libtcod.BKGND_SET)
					game_map.tiles[y][x].explored = True

				elif game_map.tiles[y][x].explored == True:
					color = 'dark_' + game_map.tiles[y][x].name
					libtcod.console_set_char_background(con, x, y, colors.get(color), libtcod.BKGND_SET)


	entities_in_render_order = sorted(entities+effects, key=lambda x: x.render_order.value)

	for effect in effects:
		draw_entity(con, effect, fov_map)
	
	for entity in entities_in_render_order:
		draw_entity(con, entity, fov_map)

	libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

	libtcod.console_set_default_background(panel, libtcod.black)
	libtcod.console_clear(panel)

	y = 1
	for message in message_log.messages:
		libtcod.console_set_default_foreground(panel, message.color)
		libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
		y += 1

	render_bar(panel, 1, 1, bar_width, 'HP', player.combat_aspect.hp, player.combat_aspect.max_hp,
			libtcod.light_red, libtcod.darker_red)

	if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
		if game_state == GameStates.SHOW_INVENTORY:
			inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
		else:
			inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

		inventory_menu(con, inventory_title, player.inventory, 50, screen_width, screen_height)

	if game_state == GameStates.HELP:
		help_menu(con, screen_width, screen_width, screen_height)


	libtcod.console_set_default_foreground(panel, libtcod.light_gray)
	libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
							 get_names_under_mouse(mouse, entities, effects, fov_map))

	libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)




def clear_all(con, entities):
	for entity in entities:
		clear_entity(con, entity)



def draw_entity(con, entity, fov_map):
	if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
		libtcod.console_set_default_foreground(con, entity.color)
		libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)



def clear_entity(con, entity):
	libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
	bar_width = int(float(value) / maximum * total_width)

	libtcod.console_set_default_background(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

	libtcod.console_set_default_background(panel, bar_color)
	if bar_width > 0:
		libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
							 '{0}: {1}/{2}'.format(name, value, maximum))



def get_names_under_mouse(mouse, entities, effects, fov_map):
	(x, y) = (mouse.cx, mouse.cy)

	names = [entity.name for entity in entities + effects if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
	names = ', '.join(names)

	return names.capitalize()

def targetting_tile(con, mouse):
	(x, y) = (mouse.cx, mouse.cy)
	libtcod.console_set_char_background(con, x, y, (200,0,0), libtcod.BKGND_SET)
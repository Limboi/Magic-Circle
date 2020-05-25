import tcod as libtcod
from game_states import GameStates

def is_valid_input(key, mouse):
	inputs = set('1234567890qwertyuiopasdfghjklzxcvbnm/?')
	inputs.update({libtcod.KEY_ESCAPE, libtcod.KEY_ENTER})
	if chr(key.c) in inputs or key.vk in inputs or mouse.lbutton_pressed or mouse.rbutton_pressed:
		return True
	else:
		return False


def handle_keys(key, game_state):
	key_char = chr(key.c)

	if game_state == GameStates.STANDART:
		if key_char == 'w':
			return {'move': (0, -1)}
		elif key_char == 's':
			return {'move': (0, 1)}
		elif key_char == 'a':
			return {'move': (-1, 0)}
		elif key_char == 'd':
			return {'move': (1, 0)}
		elif key_char == 'q':
			return {'move': (-1, -1)}
		elif key_char == 'e':
			return {'move': (1, -1)}
		elif key_char == 'z':
			return {'move': (-1, 1)}
		elif key_char == 'c':
			return {'move': (1, 1)}

		if key_char == 'g':
			return {'pickup': True}

		elif key_char == 'i':
			return {'show_inventory': True}

		elif key_char == 'b':
			return {'drop_inventory': True}

		if key_char == 'p':
			return {'toggle_realtime': True}

		if key_char == '/':
			return {'show_help': True}

		if key_char == 't':
			return {'go_deeper': True}

	elif game_state == GameStates.SHOW_INVENTORY or game_state == GameStates.DROP_INVENTORY:
		if key.vk != libtcod.KEY_ESCAPE:
			index = ord(key_char) - ord('a')
			index = abs(index)
			return {'inventory_index': index}


	if key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}

	return {}


def handle_mouse(mouse, game_state):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}
import tcod as libtcod


def menu(con, header, options, width, screen_width, screen_height):
	header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
	height = len(options) + header_height

	window = libtcod.console_new(width, height)

	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

	y = header_height
	letter_index = ord('a')
	for option_text in options:
		text = '(' + chr(letter_index) + ') ' + option_text
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
		y += 1
		letter_index += 1

	x = int(screen_width / 2 - width / 2)
	y = int(screen_height / 2 - height / 2)
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height):
	if len(inventory.items) == 0:
		options = ['Inventory is empty.']
	else:
		options = [item.name for item in inventory.items]

	menu(con, header, options, inventory_width, screen_width, screen_height)


def help_menu(con, width, screen_width, screen_height):
	height = screen_height
	window = libtcod.console_new(width, height)
	libtcod.console_set_default_foreground(window, libtcod.white)
	header = 'Help'
	text = ['Use wasd to move;',
			'Use g to pick up items;',
			'Use b to drop items;',
			'Use i to open inventory;',
			'Use p to toggle realtime mode on and off'
			'Use t to teleport to the next floor',
			'Be advised though, the deeper you go, the more dangerous dungeon becomes'
			'Hover mouse over something, to see what is it. ',
			'Press esc to exit',
			'',
			'Now go explore dungeon and genocide local population.']


	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

	y = 1
	for elem in text:
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, elem)
		y += 1

	x = int(screen_width / 2 - width / 2)
	y = int(screen_height / 2 - height / 2)
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
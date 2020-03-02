import tcod as libtcod
from PIL import Image


def main():
	screen_width = 80
	screen_height = 80

	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	libtcod.console_init_root(screen_width, screen_height, 'Image', fullscreen = False)
	con = libtcod.console_new(screen_width, screen_height)

	n = 30
	backgr = 0.7
	im = Image.open('D:\\(un)important\\python\\3year\\project\\other\\test5.png')

	rgbim = im.convert('RGB')
	rgbim.thumbnail((n,n), Image.ANTIALIAS)

	for x in range(rgbim.size[0]):
		for y in range(rgbim.size[1]):
			r, g, b = rgbim.getpixel((x,y))
			backcolor = libtcod.Color(int(r*backgr), int(g*backgr), int(b*backgr))
			libtcod.console_set_char_background(con, x, y, backcolor , libtcod.BKGND_SET)
			ch = get_char(x, y, rgbim)
			libtcod.console_set_default_foreground(con, libtcod.Color(int(r), int(g), int(b)))
			libtcod.console_put_char(con, x, y, ch, libtcod.BKGND_NONE)

	libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
	libtcod.console_flush()

	key = libtcod.Key()
	mouse = libtcod.Mouse()
	libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key, mouse, True)




def get_char(x,y, image):
	vx = 0
	vy = 0

	brightness = max(image.getpixel((x,y)))

	for i in range(-1, 2):
		for j in range(-1, 2):
			try:
				r, g, b = image.getpixel((x+i,y+j))
			except:
				r, g, b = 0, 0, 0
			vx += max(r, g, b)*i
			vy += max(r, g, b)*(-j)

	if vx == 0:
		vx = 1

	if vx < 20 and vy < 20 and brightness < 200:
		return '.'
	elif vx < 20 and vy < 20 and brightness >= 200:
		return ' '	
	elif 0.5 < abs(vy/vx) < 2:
		if vy/vx > 0:
			return '\\'
		else:
			return '/'
	elif abs(vy/vx) > 2:
		return '_'
	elif abs(vy/vx) < 0.5:
		return '|'
	else:
		return ' '
		



if __name__ == '__main__':
	 main()
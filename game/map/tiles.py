class Tile:
	def __init__(self, name, explored = False):
		self.name = name

		if name == "rock_wall":
			self.blocked = True
			self.block_sight = True
		elif name == "chasm":
			self.blocked = True
			self.block_sight = False
		else:
			self.blocked = False
			self.block_sight = False

		self.explored = explored
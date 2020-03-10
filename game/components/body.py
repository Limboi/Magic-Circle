class Bodypart:
	def __init__(self, durability, status = {}):
		self.durability = durability
		self.status = status

class Torso(Bodypart):
	pass

class Head(Bodypart):
	pass

class Arm(Bodypart):
	pass

class Leg(Bodypart):
	pass


def body_constructor(base_d, type = 'humanoid'):
	if type == 'humanoid':
		return [Torso(base_d),Head(base_d),Arm(base_d),Arm(base_d),Leg(base_d),Leg(base_d)]



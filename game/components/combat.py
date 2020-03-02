class Fighter:
	def __init__(self, hp, defense, power):
		self.max_hp = hp
		self.hp = hp
		self.defense = defense
		self.power = power


	def take_damage(self, damage):
		results = []
		self.hp -= damage
		if self.hp <= 0:
			results.append({'dead': self.owner})

		return results
		

	def attack(self, target):
		if self.owner.energy >= 100:

			results = []
			damage = self.power - target.combat_aspect.defense
			if damage > 0:
				results.append({'message': '{0} attacks {1} for {2} hit points.'.format(
					self.owner.name.capitalize(), target.name, str(damage))})
				results.extend(target.combat_aspect.take_damage(damage))
			else:
				results.append({'message': '{0} attacks {1} but does no damage.'.format(
					self.owner.name.capitalize(), target.name)})

			self.owner.energy = 0

			return results

		else:
			return [{'not_enough_energy': True}]
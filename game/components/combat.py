#import components.body
import random
import copy
import tcod as libtcod
from entities import StationaryEffect

class Combatant:
	def __init__(self, hp, base_defense, attack_power, attack_power_deviation, 
		critical = 50, active = True, fear = 0, pain = 0, statuses = {}, feats = set()):
		self.hp = hp
		self.max_hp = hp
		self.base_defense = base_defense
		self.attack_power = attack_power
		self.attack_power_deviation = attack_power_deviation
		self.critical = critical
		self.active = active
		self.fear = fear
		self.pain = pain
		self.statuses = statuses
		self.feats = feats


	def take_damage(self, damage, attack_type, crit):  #attack types so far: 'cut', 'burn'
		results = []

		self.hp -= damage
		if crit == True:
			if attack_type == 'cut':
				self.statuses.update({'bleed':damage/2})
			elif attack_type == 'burn':
				pass

		return results
		

	def heal(self, amount):
		self.hp += amount

		if self.hp > self.max_hp:
			self.hp = self.max_hp
		

	def attack(self, target, attack_type):
		if self.owner.energy >= 150:

			results = []
			power = random.gauss(self.attack_power, self.attack_power_deviation)
			damage = power - target.combat_aspect.base_defense
			crit = False
			if random.randint(1,100) < self.critical:
				crit = True
			if crit == True:
				damage = damage*2

			if damage > 0:
				results.append({'message': '{0} attacks {1} for {2} damage'.format(self.owner.name.capitalize(), target.name, round(damage))})
				if crit == True:
					results.append({'message': 'Critical {0}!'.format(attack_type)})

				results.extend(target.combat_aspect.take_damage(damage, attack_type, crit))

				if damage > target.combat_aspect.hp/5:
					eff_x = random.choice((target.x-1, target.x+1))
					eff_y = random.choice((target.y-1, target.y+1))
					blood_splatter = StationaryEffect(eff_x, eff_y, ',', libtcod.desaturated_red, 'blood splatter', 5)
					results.append({'create effect' : blood_splatter})

			else:
				results.append({'message': '{0} attacks {1} but does no damage.'.format(self.owner.name.capitalize(), target.name)})

			self.owner.energy = 0
			return results

		else:
			return [{'not_enough_energy': True}]


	def update_combatant_state(self):
		results = []
		
		if random.randint(1,50) == 1:
			if self.statuses:
				#results.append({'message': 'proc!'})
				if self.statuses.get('bleed'):
					bleedout = self.statuses.get('bleed')
					if bleedout <= 1:
						self.statuses.pop('bleed')
					else:
						self.statuses.update({'bleed': bleedout - 1})

					self.hp -= 1
					
					if bleedout < 50:
						blood_splatter = StationaryEffect(self.owner.x, self.owner.y, ',', libtcod.desaturated_red, 'blood splatter', 1)
						results.append({'create effect' : blood_splatter})
					elif 50 < bleedout:
						blood_splatter = StationaryEffect(self.owner.x, self.owner.y, ',', libtcod.desaturated_red, 'blood splatter', 5)
						results.append({'create effect' : blood_splatter})

		if self.hp <= 0:
			results.append({'dead': self.owner})
			self.active = False

		return results
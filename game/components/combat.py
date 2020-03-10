import components.body
import random
import copy
import tcod as libtcod
from entities import StationaryEffect

class Combatant:
	def __init__(self, body, base_defense, attack_power, attack_power_deviation, active = True, fear = 0, pain = 0, blood = 10000, feats = set()):
		if type(body) == str:
			self.body = copy.deepcopy( components.body.body_constructor(base_defense, body) )
		else:
			self.body = body
		self.attack_power = attack_power
		self.attack_power_deviation = attack_power_deviation
		self.active = active
		self.fear = fear
		self.pain = pain
		self.blood = blood


	def take_damage(self, target, damage, attack_type):  #attack types:  'bruise', 'cut'
		results = []

		if damage < 5:
			attack = self.body[target].status.get('bruise')
			if attack:
				attack += 1
				self.body[target].status.update({'bruise' : attack})
			else:
				self.body[target].status.update({'bruise' : 1})
			results.append({'message': 'Minor bruise'})
			
		elif 5 < damage < 20:
			attack = self.body[target].status.get(attack_type)
			if attack:
				attack += 10
				self.body[target].status.update({attack_type : attack})
			else:
				self.body[target].status.update({attack_type : 10})
			results.append({'message': 'Major {0}'.format(attack_type)})

		elif 20 < damage:
			self.body[target].status.update({'destroyed' : True})
			attack = self.body[target].status.get(attack_type)
			if attack:
				attack += 100
				self.body[target].status.update({attack_type : attack})
			else:
				self.body[target].status.update({attack_type : 100})
			results.append({'message': 'Critical {0}!'.format(attack_type)})

		return results
		

	def attack(self, target, bodypart, attack_type):
		if self.owner.energy >= 100:

			results = []
			power = random.gauss(self.attack_power, self.attack_power_deviation)
			damage = power - target.combat_aspect.body[bodypart].durability
			if damage > 0:
				results.append({'message': '{0} attacks {1}'.format(self.owner.name.capitalize(), target.name)})
				results.extend(target.combat_aspect.take_damage(bodypart, damage, attack_type))
				if damage > 5:
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
		bleed = 0
		pain = 0
		for part in self.body:
			if (part.__class__.__name__ == 'Head' or part.__class__.__name__ == 'Torso') and part.status.get('destroyed', False):
				results.append({'dead': self.owner})
				self.active = False
				return results

			if part.status.get('cut'):
				bleed += part.status.get('cut')
				pain += int(part.status.get('cut')/5)

			if part.status.get('bruise'):
				pain += part.status.get('bruise')
				if part.status.get('bruise') > 99:
					bleed += int(part.status.get('bruise')/2)

		self.blood -= bleed
		self.pain += pain

		if self.blood <= 0:
			results.append({'dead': self.owner})
			self.active = False

		if 10 < bleed < 100:
			blood_splatter = StationaryEffect(self.owner.x, self.owner.y, ',', libtcod.desaturated_red, 'blood splatter', 1)
			results.append({'create effect' : blood_splatter})
		elif 100 < bleed:
			blood_splatter = StationaryEffect(self.owner.x, self.owner.y, ',', libtcod.desaturated_red, 'blood splatter', 5)
			results.append({'create effect' : blood_splatter})

		return results
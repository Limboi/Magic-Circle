class Inventory:
	def __init__(self, capacity):
		self.capacity = capacity
		self.items = []


	def add_item(self, item):
		results = []

		if len(self.items) >= self.capacity:
			results.append({
				'item_added': None,
				'message': 'You cannot carry any more, your inventory is full'})
		else:
			results.append({
				'item_added': item,
				'message': 'You pick up the {0}!'.format(item.name)})

			self.items.append(item)

		return results


	def use(self, item_entity, **kwargs):
		if self.owner.energy >= 200:
			results = []

			item_aspect = item_entity.item_aspect

			if item_aspect.use_function is None:
				results.append({'message': 'The {0} cannot be used'.format(item_entity.name)})
			else:
				if item_aspect.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
					results.append({'targeting': item_entity})
				else:
					kwargs = {**item_aspect.function_kwargs, **kwargs}
					item_use_results = item_aspect.use_function(self.owner, **kwargs)

					for item_use_result in item_use_results:
						if item_use_result.get('consumed'):
							self.remove_item(item_entity)

					results.extend(item_use_results)

			self.owner.energy = 0
			return results

		else:
			return [{'not_enough_energy': True}]


	def remove_item(self, item):
		self.items.remove(item)


	def drop_item(self, item):
		results = []

		item.x = self.owner.x
		item.y = self.owner.y

		self.remove_item(item)
		results.append({'item_dropped': item, 'message': 'You dropped the {0}'.format(item.name)})

		return results
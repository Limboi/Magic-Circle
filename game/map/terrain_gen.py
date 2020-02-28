import random
import copy


class Drunkard:

	def __init__(self, posx, posy, width, height, seed, bias = 1, bias_degree = 50):
		self.posx = posx
		self.posy = posy
		self.height = height
		self.width = width
		self.seed = seed
		random.seed(self.seed, version=2)
		self.bias = bias
		self.bias_degree = bias_degree


	def walk(self):
		dir = random.randint(0,3)
		if dir==0 and self.posx+1 < self.width-1:
			self.posx += 1 #right
		elif dir==1 and self.posy+1 < self.height-1:
			self.posy += 1 #down
		elif dir==2 and self.posx-1 > 0:
			self.posx -= 1 #left
		elif dir==3 and self.posy-1 >0:
			self.posy -= 1 #up 

	
	def biased_walk(self):
		if random.randint(0,100) < self.bias_degree:
			dir = self.bias
		else:
			dir = random.randint(0,3)

		if dir==0 and self.posx+1 < self.width - 1:
			self.posx += 1 #right
		elif dir==1 and self.posy+1 < self.height - 1:
			self.posy += 1 #down
		elif dir==2 and self.posx-1 > 0:
			self.posx -= 1 #left
		elif dir==3 and self.posy-1 >0:
			self.posy -= 1 #up

	
	def bias_change(self, bias):
		self.bias = bias


	def coord(self):
		return (self.posx, self.posy)



class Zone:

	def __init__(self, structure, seed):
		self.width = len(structure[0])
		self.height = len(structure)
		self.seed = seed
		random.seed(self.seed, version=2)
		self.__structure = structure


	def create_floor_drunkard_generation(self, chance_to_create, chance_to_destroy, creation_threshold,
		destruction_threshold, filling, frequency = 1, biased = True, tile = "rock_floor", level = 0, overwrite = True,
		safe_tiles = {"rock_wall"}):

		__flag = True
		__iteration = 0
		__walked = 0

		drunks = []
		newdr = Drunkard(self.width//2, self.height//2, self.width, self.height, self.seed)
		drunks.append(newdr)

		while __flag == True :
			destroyed = 0
			created = 0
			buff = []

			for drunk in drunks:
				x,y = drunk.coord()

				if overwrite or (self.__structure[y][x] in safe_tiles):
					self.__structure[y][x] = tile
				__walked += 1

				if __iteration % 10 == 0:
						drunk.bias_change(random.randint(0,3))

				exists = True

				if __iteration % frequency == 0:

					if (random.randint(1,100) < chance_to_create) and (created < creation_threshold):
						newdr = Drunkard(x, y, self.width, self.height, self.seed, random.randint(0,3))
						buff.append(newdr)
						created += 1
					
					if (random.randint(1,100) < chance_to_destroy) and (destroyed < destruction_threshold) and (len(drunks) > 1):
						drunks.remove(drunk)
						destroyed += 1
						exists = False
				
				if exists:
					if biased:
						drunk.biased_walk()
					else:
						drunk.walk()
					

			drunks.extend(buff)
			__iteration += 1

			if __walked > self.width * self.height * filling * 0.01 and __iteration % 10 == 0: 
				counter = 0
				for i in range(self.height):
					for j in range(self.width):
						if self.__structure[i][j] == tile:
							counter += 1
				if counter > self.width * self.height * filling * 0.01:
					__flag = False

			if __iteration > self.width * self.height:
				__flag = False
				#print( "Current seed probably creates problems" )
				self.seed += 10
				if level < 10:
					self.create_floor_drunkard_generation(chance_to_create, chance_to_destroy, creation_threshold, 
						destruction_threshold, filling, frequency, biased, tile, level + 1, overwrite, safe_tiles)


	def create_floor_rooms(self, number_of_rooms):
		rooms = []
		i = 0

		while i < number_of_rooms:
			px=round(random.gauss(self.width/2, self.width/2))
			py=round(random.gauss(self.height/2, self.height/2))
			if not((3 < px < self.width-3 ) and (3 < py < self.height-3 )):
				i -= 1
			else:
				rooms.append([[px - 1, px + 2],[py - 1, py + 2]])
			i += 1

		for i in range(5):
			for rectangle in rooms:
				rnd = random.randint(0,2)
				if rnd == 0:
					if rectangle[0][0] - 1 > 1:
						rectangle[0][0] -= 1
					if rectangle[0][1] + 1 < self.width - 1:
						rectangle[0][1] += 1

				if rnd == 1:
					if rectangle[1][0] - 1 > 1:
						rectangle[1][0] -= 1
					if rectangle[1][1] + 1 < self.height - 1:
						rectangle[1][1] += 1

				if rnd == 3:
					if rectangle[0][0] - 1 > 1:
						rectangle[0][0] -= 1
					if rectangle[0][1] + 1 < self.width - 1:
						rectangle[0][1] += 1
					if rectangle[1][0] - 1 > 1:
						rectangle[1][0] -= 1
					if rectangle[1][1] + 1 < self.height - 1:
						rectangle[1][1] += 1

		for rectangle in rooms:
			for x in range(rectangle[0][0], rectangle[0][1]):
				for y in range(rectangle[1][0], rectangle[1][1]):
					self.__structure[y][x] = "smooth_floor"

		centers = []
		for room in rooms:
			centers.append([ round((room[0][0] + room[0][1]) / 2) , round((room[1][0] + room[1][1]) / 2) ])

		for i in range(number_of_rooms):
			point = centers.pop(0)
			for other in centers:
				if point[0] - other[0] == 0:
					pass
				else:
					for j in range(0, -(point[0] - other[0]), -round( abs(point[0] - other[0])/(point[0] - other[0])) ):
						self.__structure[ point[1] ][ point[0] + j ] = "smooth_floor"
				if point[1] - other[1] == 0:
					pass
				else:
					for j in range(0, -(point[1] - other[1]), -round( abs(point[1] - other[1])/(point[1] - other[1])) ):
						self.__structure[point[1] + j][ point[0] ] = "smooth_floor"

		for y in range(self.height):
			for x in range(self.width):
				if self.__structure[y][x] == "smooth_floor":
					for i in range(y-1, y+2):
						for j in range(x-1, x+2):
							if self.__structure[i][j] != "smooth_floor":
								self.__structure[i][j] = "fort_wall"


	def create_floor_test(self, designation):
		self.__structure = [[ designation for i in range(self.width)] for j in range(self.height)]


	def give_structure(self):
		return self.__structure



class Terrain:

	def __init__(self, width, height, seed = 123, zoning = []):
		self.width = width
		self.height = height
		self.seed = seed
		self.__zoning = zoning
		self.__structure = [[ "rock_wall" for i in range(width)] for j in range(height)]


	def simple_create_zoning(self, number_of_zones, startx = 0, starty = 0, endx = None, endy = None, seed = None):
		if seed == None:
			seed = self.seed
		if endx == None:
			endx = self.width
		if endy == None:
			endy = self.height # maybe use kwargs ???

		random.seed(seed, version=2)

		if number_of_zones == 1:
			self.__zoning.append([[startx,endx],[starty,endy]])
		else:
			znr = random.randint(1, number_of_zones - 1) # zone number randomizer
			flag_v = True
			flag_h = True

			try:
				divider_v = random.randint(startx + round(endx * 0.1), round(endx * 0.9))
			except BaseException:
				flag_v = False
				divider_v = endx

			try:
				divider_h = random.randint(starty + round(endy * 0.1), round(endy * 0.9))
			except BaseException:
				flag_v = False
				divider_h = endy

			if random.randint(0,1) == 0 and flag_v == True:
				self.simple_create_zoning(number_of_zones - znr, startx, starty, divider_v, endy)
				self.simple_create_zoning(znr, divider_v, starty, endx, endy)
			elif flag_h == True:
				self.simple_create_zoning(number_of_zones - znr, startx, starty, endx, divider_h)
				self.simple_create_zoning(znr, startx, divider_h, endx, endy)


	def expanding_create_zoning(self, number_of_zones, seed = None):
		if seed == None:
			seed = self.seed
		i=0
		temp_zoning = []
		random.seed(seed, version=2)

		while i < number_of_zones:
			px=round(random.gauss(self.width/2, self.width/3))
			py=round(random.gauss(self.height/2, self.height/3))
			if not((0 < px < self.width-1 ) and (0 < py < self.height-1 )):
				i -= 1
			else:
				temp_zoning.append([[px - 1, px + 2],[py - 1, py + 2]])
			i += 1

		complete_flag = False

		while complete_flag == False:
			blocked = 0

			for rectangle in temp_zoning:

				c_rectangle = copy.deepcopy(rectangle)
				others = copy.deepcopy(temp_zoning)
				others.remove(c_rectangle)
				side_blocked = 0

				adv = True
				if rectangle[0][0] - 1 >= 0:
					for other in others:
						if (((rectangle[0][0] - 1 >= other[0][1]) or (rectangle[0][1] <= other[0][0])) 
						or ((rectangle[1][0] >= other[1][1]) or (rectangle[1][1] <= other[1][0] ))):
							pass
						else:
							side_blocked += 1
							adv = False
							break
					if adv == True:
						rectangle[0][0] -= 1
				else:
					side_blocked +=1

				adv = True
				if rectangle[0][1] + 1 <= self.width:
					for other in others:
						if ((rectangle[0][0] >= other[0][1] or rectangle[0][1] + 1 <= other[0][0]) 
						or (rectangle[1][0] >= other[1][1] or rectangle[1][1] <= other[1][0] )):
							pass
						else:
							side_blocked += 1
							adv = False
							break
					if adv == True:
						rectangle[0][1] += 1
				else:
					side_blocked +=1

				adv = True
				if rectangle[1][0] - 1 >= 0:
					for other in others:
						if ((rectangle[0][0] >= other[0][1] or rectangle[0][1] <= other[0][0]) 
						or (rectangle[1][0] - 1 >= other[1][1] or rectangle[1][1] <= other[1][0] )):
							pass
						else:
							side_blocked += 1
							adv = False
							break
					if adv == True:
						rectangle[1][0] -= 1
				else:
					side_blocked +=1

				adv = True
				if rectangle[1][1] + 1 <= self.height:
					for other in others:
						if ((rectangle[0][0] >= other[0][1] or rectangle[0][1] <= other[0][0]) 
						or (rectangle[1][0] >= other[1][1] or rectangle[1][1] + 1 <= other[1][0] )):
							pass
						else:
							side_blocked += 1
							adv = False
							break
					if adv == True:
						rectangle[1][1] += 1
				else:
					side_blocked +=1

				if side_blocked == 4:
					blocked += 1

			if blocked == number_of_zones:
				complete_flag = True

		self.__zoning = temp_zoning


	def fill_zones(self, filling_type = "floor"):
		n = 0
		castle_counter = 0

		for element in self.__zoning:
			n += 1
			starting_struct = [[ None for i in range(element[0][1] - element[0][0])] for j in range(element[1][1] - element[1][0])]

			for y in range (element[1][1] - element[1][0]):
				for x in range (element[0][1] - element[0][0]):
					starting_struct[y][x] = self.__structure[y + element[1][0] ][x + element[0][0] ]

			a = Zone(starting_struct, self.seed + n * 2)

			if filling_type == "test":
				a.create_floor_test(n)
			if filling_type == "floor":
				a.create_floor_drunkard_generation(80, 20, 4, 2, 25, 5)
			if filling_type == "chasm":
				a.create_floor_drunkard_generation(90, 50, 5, 2, 10, 1, False, "chasm", overwrite = False)

			if filling_type == "castle":
				if ((element[0][1] - element[0][0]) * (element[1][1] - element[1][0]) >= 625 and
				castle_counter <= 2 ):
					a.create_floor_rooms(6)
					castle_counter += 1

			temp_struct = a.give_structure()
			for y in range (element[1][1] - element[1][0]):
				for x in range (element[0][1] - element[0][0]):
					self.__structure[y + element[1][0] ][x + element[0][0] ] = temp_struct[y][x]


	def connect_zones(self, density = 2):
		centers = []
		for zone in self.__zoning:
			centers.append([ round((zone[0][0] + zone[0][1]) / 2) , round((zone[1][0] + zone[1][1]) / 2) ])

		for i in range(density):
			point = centers.pop(0)
			for other in centers:
				if point[0] == other[0]:
					break
				vector = (point[1] - other[1])/(point[0] - other[0])
				indent = point[0] * (point[1] - other[1])/(other[0] - point[0]) + point[1]
				for j in range(0, -(point[0] - other[0]), -round( abs(point[0] - other[0])/(point[0] - other[0])) ):
					try:
						self.__structure[ round(vector * (point[0] +j) + indent) - 1 ][ point[0] +j ] = "rock_floor"
					except:
						pass
					try:
						self.__structure[ round(vector * (point[0] +j) + indent)][ point[0] +j ] = "rock_floor"
					except:
						pass
					try:
						self.__structure[ round(vector * (point[0] +j) + indent)][ point[0] +j - 1 ] = "rock_floor"
					except:
						pass

						
	def give_zoning(self):
		return self.__zoning


	def clear_zoning(self):
		self.__zoning = []


	def give_structure(self):
		return self.__structure


		



def generate_terrain(width, height, seed):
	field = Terrain(width, height, seed)

	print("starting")

	field.expanding_create_zoning(5, seed)
	print("new zoning created")
	field.fill_zones()
	field.connect_zones(3)
	field.clear_zoning()

	field.expanding_create_zoning(10, seed + 50)
	print("new zoning created")
	field.fill_zones("castle")
	field.clear_zoning()

	field.expanding_create_zoning(10, seed +100)
	print("new zoning created")
	field.fill_zones("chasm")

	print("ready to start")
	return field.give_structure() 


def generate_test_arena(width, height):
	terrain = [[ "rock_wall" for i in range(width)] for j in range(height)]
	for y in range(height):
		for x in range(width):
			if (1 < x < width - 1) and (1 < y < height - 1):
				terrain[y][x] = "rock_floor"
	return terrain










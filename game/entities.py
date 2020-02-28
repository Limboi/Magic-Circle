from abc import ABC, abstractmethod

class Entity(ABC):
	pass



class Self_moving(Entity):

	def __init__(self, x, y, char, color):
		self.x, self.y = x, y
		self.char = char
		self.color = color

	def move(self, dx, dy):
		self.x += dx
		self.y += dy



class Living(Self_moving):
	pass



class Humanoid(Living):
	def __init__(self, x, y, char, color):
		self.x, self.y = x, y
		self.char = char
		self.color = color
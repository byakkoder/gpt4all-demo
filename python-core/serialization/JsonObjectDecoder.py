from collections import namedtuple

class JsonObjectDecoder:
	def __init__(self, dictionary):
		self.__dict__.update(dictionary)
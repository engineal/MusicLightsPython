from tkinter import *
from tkinter import ttk

class ChristmasEffect(object):
	def __init__(self, pixels):
		self.pixels = pixels
		self.update = False

	def createUI(self, parent):
		ttk.Label(parent, text="Merry Christmas!!!").grid(column=0, row=1, sticky=(W, E))

	def selectionChanged(self):
		self.update = True
		avg_color = tuple(int(sum(x)/len(x)) for x in zip(*[pixel.color for pixel in self.pixels if pixel.selected]))
		if avg_color:
			self.red_scale.set(avg_color[0])
			self.green_scale.set(avg_color[1])
			self.blue_scale.set(avg_color[2])
		self.update = False
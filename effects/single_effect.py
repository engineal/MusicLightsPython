from tkinter import *
from tkinter import ttk

class SingleEffect(object):
	def __init__(self, pixels):
		self.pixels = pixels
		self.update = False

	def createUI(self, parent):
		ttk.Label(parent, text="Red:").grid(column=0, row=1, sticky=(W, E))
		self.red_scale = ttk.Scale(parent, orient=HORIZONTAL, from_=0, to=255, value=255, command=self.setColor)
		self.red_scale.grid(column=1, row=1, sticky=(W, E))
		ttk.Label(parent, text="Green:").grid(column=0, row=2, sticky=(W, E))
		self.green_scale = ttk.Scale(parent, orient=HORIZONTAL, from_=0, to=255, value=255, command=self.setColor)
		self.green_scale.grid(column=1, row=2, sticky=(W, E))
		ttk.Label(parent, text="Blue:").grid(column=0, row=3, sticky=(W, E))
		self.blue_scale = ttk.Scale(parent, orient=HORIZONTAL, from_=0, to=255, value=255, command=self.setColor)
		self.blue_scale.grid(column=1, row=3, sticky=(W, E))
	
	def setColor(self, value):
		if not self.update:
			red = int(self.red_scale.get())
			green = int(self.green_scale.get())
			blue = int(self.blue_scale.get())
			
			for pixel in self.pixels:
				if pixel.selected:
					pixel.color = (red, green, blue)

	def selectionChanged(self):
		self.update = True
		avg_color = tuple(int(sum(x)/len(x)) for x in zip(*[pixel.color for pixel in self.pixels if pixel.selected]))
		if avg_color:
			self.red_scale.set(avg_color[0])
			self.green_scale.set(avg_color[1])
			self.blue_scale.set(avg_color[2])
		self.update = False
from tkinter import *
from tkinter import ttk

class Pixel(object):
	def __init__(self, strip, canvas, x, y):
		self.strip = strip
		self.canvas = canvas
		self._selected = False
		self._color = (255, 0, 0)
		self.id = canvas.create_oval(x, y, x + 10, y + 10, fill="#%02x%02x%02x" % self._color, width=0, tags="pixel")
		
	@property
	def selected(self):
		return self._selected

	@selected.setter
	def selected(self, value):
		self._selected = value
		if value:
			self.canvas.itemconfig(self.id, width=2)
		else:
			self.canvas.itemconfig(self.id, width=0)
			
	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, value):
		if self._color != value:
			self._color = value
			self.canvas.itemconfig(self.id, fill="#%02x%02x%02x" % value)
			self.strip.setPixelColor(self.id, value)

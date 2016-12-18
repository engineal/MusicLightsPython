from tkinter import *
from tkinter import ttk

class IndividualEffect(object):

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
		if self._selected_item:
			red = int(self.red_scale.get())
			green = int(self.green_scale.get())
			blue = int(self.blue_scale.get())
			
			new_color = "#%02x%02x%02x" % (red, green, blue)
			self.canvas.itemconfig(self._selected_item, fill=new_color)
			self.strip.setPixelColor(self._selected_item, (red, green, blue))

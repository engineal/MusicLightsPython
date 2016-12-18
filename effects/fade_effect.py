from tkinter import *
from tkinter import ttk

class FadeEffect(object):
	def createUI(self, parent):		
		ttk.Label(parent, text="Red:").grid(column=0, row=1, sticky=(W, E))
		self.red_scale = ttk.Scale(color_group, orient=HORIZONTAL, from_=0, to=255, value=255, command=self.setColor)
		self.red_scale.grid(column=1, row=1, sticky=(W, E))
		ttk.Label(parent, text="Green:").grid(column=0, row=2, sticky=(W, E))
		self.green_scale = ttk.Scale(color_group, orient=HORIZONTAL, from_=0, to=255, value=255, command=self.setColor)
		self.green_scale.grid(column=1, row=2, sticky=(W, E))
		ttk.Label(parent, text="Blue:").grid(column=0, row=3, sticky=(W, E))
		self.blue_scale = ttk.Scale(color_group, orient=HORIZONTAL, from_=0, to=255, value=255, command=self.setColor)
		self.blue_scale.grid(column=1, row=3, sticky=(W, E))

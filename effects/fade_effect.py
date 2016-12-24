from tkinter import *
from tkinter import ttk

class FadeEffect(object):
	def __init__(self, pixels):
		self.pixels = pixels
		self.update = False

	def createUI(self, parent):
		ttk.Label(parent, text="Fade").grid(column=0, row=1, sticky=(W, E))

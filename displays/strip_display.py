from tkinter import *
from tkinter import ttk
from pixel import Pixel
from effects.single_effect import SingleEffect
from effects.fade_effect import FadeEffect

class StripDisplay(object):
	def __init__(self, strip):
		self.strip = strip
		self.pixels = []
		self.effect = SingleEffect(self.pixels)

	def createUI(self, parent):
		parent.columnconfigure(0, weight=0)
		parent.columnconfigure(1, weight=1, minsize=200)
		
		ttk.Label(parent, text="Linear Array").grid(column=0, row=1, sticky=(W, E))
		ttk.Label(parent, text="Pixel Count:").grid(column=0, row=2, sticky=(W, E))
		ttk.Label(parent, text=str(self.strip.numPixels())).grid(column=1, row=2, sticky=(W, E))
		ttk.Label(parent, text="Brightness:").grid(column=0, row=3, sticky=(W, E))
		ttk.Scale(parent, orient=HORIZONTAL, from_=0, to=255, value=self.strip.getBrightness(), command=self.setBrightness).grid(column=1, row=3, sticky=(W, E))
		
		self.effect_box = ttk.Combobox(parent, values=("Single", "Fade", "Script"), state='readonly')
		self.effect_box.current(0)
		self.effect_box.bind("<<ComboboxSelected>>", self.effectChanged)
		self.effect_box.grid(column=0, row=4, sticky=(N, W, E))
		
		color_group = ttk.LabelFrame(parent, text='Effect')
		color_group.grid(column=1, row=4, sticky=(W, E))
		color_group.columnconfigure(0, weight=0)
		color_group.columnconfigure(1, weight=1)
		self.effect.createUI(color_group)
		
		self.canvas = Canvas(parent, background="#FFFFFF")
		self.canvas.grid(column=0, row=5, columnspan=2, sticky=(N, W, E, S))
		
		self._drag_data = {"x": 0, "y": 0, "drag": False}
		self._select_data = {"x": 0, "y": 0, "id": None}
		
		self.canvas.tag_bind("pixel", "<ButtonPress-1>", self.onPixelButtonPress)
		self.canvas.tag_bind("pixel", "<ButtonRelease-1>", self.onPixelButtonRelease)
		self.canvas.tag_bind("pixel", "<B1-Motion>", self.onPixelMotion)
		
		self.canvas.bind("<ButtonPress-1>", self.onButtonPress)
		self.canvas.bind("<ButtonRelease-1>", self.onButtonRelease)
		self.canvas.bind("<B1-Motion>", self.onMotion)
		
		for i in range(0, 20):
			self.pixels.append(Pixel(self.strip, self.canvas, (20*i)+5, 5))
		
	def onPixelButtonPress(self, event):
		'''Begin drag of an object'''
		for pixel in self.pixels:
			if pixel.id in self.canvas.find_closest(event.x, event.y):
				above = pixel
		
		if not above.selected and event.state != 9:
			for pixel in self.pixels:
				pixel.selected = False;
		above.selected = True;
		self.effect.selectionChanged()

		self._drag_data["x"] = event.x
		self._drag_data["y"] = event.y
		self._drag_data["drag"] = True

	def onPixelButtonRelease(self, event):
		'''End drag of an object'''
		self._drag_data["x"] = 0
		self._drag_data["y"] = 0
		self._drag_data["drag"] = False

	def onPixelMotion(self, event):
		'''Handle dragging of an object'''
		if self._drag_data["drag"]:
			# compute how much this object has moved
			delta_x = event.x - self._drag_data["x"]
			delta_y = event.y - self._drag_data["y"]
			# move the object the appropriate amount
			for pixel in self.pixels:
				if pixel.selected:
					self.canvas.move(pixel.id, delta_x, delta_y)
			# record the new position
			self._drag_data["x"] = event.x
			self._drag_data["y"] = event.y
				
	def onButtonPress(self, event):
		'''Begin selection box'''
		if not self._drag_data["drag"]:
			self._select_data["id"] = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, fill="#476042", stipple="gray50")
			self._select_data["x"] = event.x
			self._select_data["y"] = event.y
			
			for pixel in self.pixels:
				pixel.selected = False
			self.effect.selectionChanged()
	
	def onButtonRelease(self, event):
		'''End selection box'''
		if self._select_data["id"]:
			self.canvas.delete(self._select_data["id"])
			self._select_data["id"] = None
			self._select_data["x"] = 0
			self._select_data["y"] = 0
	
	def onMotion(self, event):
		'''Handle dragging of selection box'''
		if self._select_data["id"]:
			self.canvas.coords(self._select_data["id"], self._select_data["x"], self._select_data["y"], event.x, event.y)
			
			xlow = min(self._select_data["x"], event.x)
			xhigh = max(self._select_data["x"], event.x)
			
			ylow = min(self._select_data["y"], event.y)
			yhigh = max(self._select_data["y"], event.y)

			for pixel in self.pixels:
				x1, y1, x2, y2 = self.canvas.coords(pixel.id)
				x, y = (x1+x2)/2, (y1+y2)/2
				if (xlow < x < xhigh) and (ylow < y < yhigh):
					pixel.selected = True
				else:
					pixel.selected = False
			
			self.effect.selectionChanged()
		
	def setBrightness(self, value):
		self.strip.setBrightness(int(float(value)))
		
	def effectChanged(self, event):
		print(self.effect_box.get())

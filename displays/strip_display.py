from tkinter import *
from tkinter import ttk

def HTMLColorToRGB(colorstring):
	""" convert #RRGGBB to an (R, G, B) tuple """
	colorstring = colorstring.strip()
	if colorstring[0] == '#': colorstring = colorstring[1:]
	if len(colorstring) != 6:
		raise ValueError("input #%s is not in #RRGGBB format" % colorstring)
	r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
	r, g, b = [int(n, 16) for n in (r, g, b)]
	return (r, g, b)

class StripDisplay(object):
	def __init__(self, strip):
		self.strip = strip
		self._selected_item = None

	def createUI(self, parent):
		parent.columnconfigure(0, weight=0)
		parent.columnconfigure(1, weight=1, minsize=200)
		
		ttk.Label(parent, text="Linear Array").grid(column=0, row=1, sticky=(W, E))
		ttk.Label(parent, text="Pixel Count:").grid(column=0, row=2, sticky=(W, E))
		ttk.Label(parent, text=str(self.strip.numPixels())).grid(column=1, row=2, sticky=(W, E))
		ttk.Label(parent, text="Brightness:").grid(column=0, row=3, sticky=(W, E))
		ttk.Scale(parent, orient=HORIZONTAL, from_=0, to=255, value=self.strip.getBrightness(), command=self.setBrightness).grid(column=1, row=3, sticky=(W, E))
		
		color_group = ttk.LabelFrame(parent, text='Color')
		color_group.grid(column=1, row=4, sticky=(W, E))
		color_group.columnconfigure(0, weight=0)
		color_group.columnconfigure(1, weight=1)
		
		ttk.Label(color_group, text="Red:").grid(column=0, row=1, sticky=(W, E))
		self.red_scale = ttk.Scale(color_group, orient=HORIZONTAL, from_=0, to=255, value=255, command=self.setColor)
		self.red_scale.grid(column=1, row=1, sticky=(W, E))
		ttk.Label(color_group, text="Green:").grid(column=0, row=2, sticky=(W, E))
		self.green_scale = ttk.Scale(color_group, orient=HORIZONTAL, from_=0, to=255, value=255, command=self.setColor)
		self.green_scale.grid(column=1, row=2, sticky=(W, E))
		ttk.Label(color_group, text="Blue:").grid(column=0, row=3, sticky=(W, E))
		self.blue_scale = ttk.Scale(color_group, orient=HORIZONTAL, from_=0, to=255, value=255, command=self.setColor)
		self.blue_scale.grid(column=1, row=3, sticky=(W, E))
		
		self.canvas = Canvas(parent, background="#FFFFFF")
		self.canvas.grid(column=0, row=5, columnspan=2, sticky=(N, W, E, S))
		
		self._drag_data = {"x": 0, "y": 0, "item": None, "drag": False}
		
		self.canvas.tag_bind("token", "<ButtonPress-1>", self.onTokenButtonPress)
		self.canvas.tag_bind("token", "<ButtonRelease-1>", self.onTokenButtonRelease)
		self.canvas.tag_bind("token", "<B1-Motion>", self.onTokenMotion)
		
		o1 = self.canvas.create_oval(10, 10, 20, 20, fill="#FF0000", width=0, tags="token")
		o2 = self.canvas.create_oval(30, 10, 40, 20, fill="#00FF00", width=0, tags="token")
		o3 = self.canvas.create_oval(50, 10, 60, 20, fill="#0000FF", width=0, tags="token")
		
	def onTokenButtonPress(self, event):
		'''Being drag of an object'''
		# record the item and its location
		self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
		self._drag_data["x"] = event.x
		self._drag_data["y"] = event.y

	def onTokenButtonRelease(self, event):
		'''End drag of an object'''
		if not self._drag_data["drag"]:
			if self._selected_item:
				self.canvas.itemconfig(self._selected_item, width=0)
				
			if self._selected_item is self._drag_data["item"]:
				self._selected_item = None
			else:
				self._selected_item = None
				red, green, blue = HTMLColorToRGB(self.canvas.itemcget(self._drag_data["item"], "fill"))
				self.red_scale.set(red)
				self.green_scale.set(green)
				self.blue_scale.set(blue)
				
				self._selected_item = self._drag_data["item"]
				self.canvas.itemconfig(self._selected_item, width=2)

		# reset the drag information
		self._drag_data["item"] = None
		self._drag_data["x"] = 0
		self._drag_data["y"] = 0
		self._drag_data["drag"] = False

	def onTokenMotion(self, event):
		'''Handle dragging of an object'''
		# compute how much this object has moved
		delta_x = event.x - self._drag_data["x"]
		delta_y = event.y - self._drag_data["y"]
		# move the object the appropriate amount
		self.canvas.move(self._drag_data["item"], delta_x, delta_y)
		# record the new position
		self._drag_data["x"] = event.x
		self._drag_data["y"] = event.y
		self._drag_data["drag"] = True
		
	def setBrightness(self, value):
		self.strip.setBrightness(int(float(value)))
		
	def setColor(self, value):
		if self._selected_item:
			red = int(self.red_scale.get())
			green = int(self.green_scale.get())
			blue = int(self.blue_scale.get())
			
			new_color = "#%02x%02x%02x" % (red, blue, green)
			self.canvas.itemconfig(self._selected_item, fill=new_color)
			self.strip.setPixelColor(self._selected_item, (red, green, blue))

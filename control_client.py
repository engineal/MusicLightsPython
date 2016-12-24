from tkinter import *
from tkinter import ttk
import Pyro4
from displays.strip_display import StripDisplay

class ControlClient(object):
	def __init__(self):
		self.displays = []
		ns = Pyro4.locateNS(host="engineal.com", port=5621)
		uri = ns.lookup("lights.server")
		with Pyro4.Proxy(uri) as server:
			for client in server.get_clients():
				print(client)
				display = StripDisplay(client)
				self.displays.append(display)

	def createUI(self):
		root = Tk()
		root.title("Control Lights")
		
		mainframe = ttk.Frame(root)
		mainframe.pack(side="top", fill="both", expand=True)
		
		self.canvas = Canvas(mainframe)
		self.canvas.pack(side="left", fill="both", expand=True)
		
		vsb = ttk.Scrollbar(mainframe, orient="vertical", command=self.canvas.yview)
		vsb.pack(side="right", fill="y")
		self.canvas.configure(yscrollcommand=vsb.set)
		
		groupframe = ttk.Frame(self.canvas)
		groupframe.bind("<Configure>", self.onFrameConfigure)
		self.canvas.create_window((0,0), window=groupframe, anchor="nw", tags="groupframe")
		groupframe.columnconfigure(0, weight=1)
		
		for display in self.displays:
			group = ttk.LabelFrame(groupframe, text='Display 1')
			group.grid(column=0, row=0, sticky=(W, E))
			display.createUI(group)
		
		root.update()
		root.minsize(root.winfo_width(), root.winfo_height())
		root.mainloop()
		
	def onFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

def main():
	client = ControlClient()
	client.createUI()
	
if __name__ == "__main__":
	main()

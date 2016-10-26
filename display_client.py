import Pyro4
#from dotstar import Adafruit_DotStar

@Pyro4.expose
class StripClient(object):
	def __init__(self, numpixels):
		self.numpixels = numpixels
		#strip = Adafruit_DotStar(numpixels)
		#strip.begin()
		#strip.setBrightness(64)

	def clear(self):
		#self.strip.clear()
		print("clear")
		
	def setBrightness(self, value):
		#self.strip.setBrightness()
		print("setBrightness: ", value)
		
	def setPixelColor(self, pixel, color):
		#self.strip.setPixelColor(pixel, color)
		print("setPixelColor: ", pixel, color)
		
	def show(self):
		#self.strip.show()
		print("show")
		
	def getPixelColor(self):
		#self.strip.getPixelColor()
		print("getPixelColor")
		
	def numPixels(self):
		#return self.strip.numPixels()
		return self.numpixels
		
	def getBrightness(self):
		#return self.strip.setBrightness()
		return 64

def main():
	with Pyro4.Daemon() as daemon:
		client = StripClient(150)
		daemon.register(client)
		
		ns = Pyro4.locateNS(host="engineal.com", port=5621)
		uri = ns.lookup("lights.server")
		print(uri)
		with Pyro4.Proxy(uri) as server:
			server.connect(client)
		
		print("Client is now listening for commands.")
		daemon.requestLoop()
	
if __name__ == "__main__":
    main()

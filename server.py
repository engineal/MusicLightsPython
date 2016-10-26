import Pyro4

@Pyro4.expose
class LightServer(object):
	def __init__(self):
		self.clients = []
	
	def connect(self, client):
		self.clients.append(client)
		print("Client connected")

	def get_clients(self):
		return self.clients

def main():
	with Pyro4.Daemon(port=5622,nathost="engineal.com",natport=5622) as daemon:
		server = LightServer()
		uri = daemon.register(server)
		with Pyro4.locateNS() as ns:
			ns.register("lights.server", uri)
		print("Server ready.")
		daemon.requestLoop()
	
if __name__ == "__main__":
    main()

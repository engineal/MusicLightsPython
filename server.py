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
	with Pyro4.Daemon(host="192.168.1.2", port=5622, nathost="engineal.com", natport=0) as daemon:
		server = LightServer()
		uri = daemon.register(server)
		print(uri)
		with Pyro4.locateNS(host="engineal.com", port=5621) as ns:
			ns.register("lights.server", uri)
		print("Server ready.")
		daemon.requestLoop()
	
if __name__ == "__main__":
    main()

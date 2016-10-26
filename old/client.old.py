import sys
import socket

class Client(object):
	def connect(self, server_address):
		# Create a TCP/IP socket
		self.sock = socket.create_connection(server_address)
		
	def disconnect(self):
		self.sock.close()

	def send(self, message):
		self.sock.sendall(message.encode())

	def receive(self):
		# Look for the response
		amount_received = 0
		amount_expected = 6
		data = b""
		
		while amount_received < amount_expected:
			data += self.sock.recv(80)
			amount_received += len(data)
			
		return data.decode('UTF-8')
            
client = Client()
client.connect(("engineal.com", 5622))
client.send("Hello World!")
client.disconnect()

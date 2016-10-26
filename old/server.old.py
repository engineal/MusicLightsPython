import sys
import socket
import select
import errno

class LightServer(object):
	def __init__(self, server_address):
		# Create a TCP/IP socket
		self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Bind the socket to the port
		print('starting up on %s port %s' % server_address)
		self.srvsock.bind(server_address)

		# Listen for incoming connections
		self.srvsock.listen(1)

		self.descriptors = [self.srvsock]

	def run(self):
		while True:
			# Await an event on a readable socket descriptor
			(sread, swrite, sexc) = select.select(self.descriptors, [], [])

			# Iterate through the tagged read descriptors
			for sock in sread:
				# Received a connect to the server (listening) socket
				if sock == self.srvsock:
					self.accept_new_connection()
				else:
					# Received something on a client socket
					try:
						str = sock.recv(100).decode()
						# Check to see if the peer socket closed
						if str == '':
							host,port = sock.getpeername()
							str = 'Client left %s:%s' % (host, port)
							self.broadcast_string(str, sock)
							sock.close()
							self.descriptors.remove(sock)
						else:
							self.decode_command(sock, str)
					except socket.error as error:
						host,port = sock.getpeername()
						str = 'Client left %s:%s' % (host, port)
						self.broadcast_string(str, sock)
						sock.close()
						self.descriptors.remove(sock)

	def decode_command(self, sock, str):
		host,port = sock.getpeername()
		newstr = '[%s:%s] %s' % (host, port, str)
		if str == "list clients":
			sock.send("client list".encode())
		else:
			self.broadcast_string(newstr, sock)
	
	def broadcast_string(self, str, omit_sock):
		for sock in self.descriptors:
			if sock != self.srvsock and sock != omit_sock:
				sock.send(str.encode())

		print(str)

	def accept_new_connection(self):
		newsock, (remhost, remport) = self.srvsock.accept()
		self.descriptors.append(newsock)

		str = 'Client joined %s:%s' % (remhost, remport)
		self.broadcast_string(str, newsock)

if __name__ == "__main__":
	server = LightServer(('192.168.1.2', 5622))
	server.run()

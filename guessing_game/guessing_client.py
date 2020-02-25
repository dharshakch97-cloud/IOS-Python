import socket

s = socket.socket()
host = socket.gethostname()
port = 10002
s.connect((host, port))
flag = True
while flag:
	msg = input()	
	# print("\nClient input : "+msg)
	s.sendall(msg.encode())
	from_server = (s.recv(1024).decode())
	print("From Server : "+from_server)
	if (from_server.find('correct') != -1): 
          flag = False 
s.close()	
print("Game Completed")
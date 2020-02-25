import socket                
import random
  
# next create a socket object 
#s = socket.socket()          
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 10002             
  
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind((socket.gethostname(),port))         
print ("socket binded to %s" %(port)) 
  
# put the socket into listening mode 
s.listen(5)      
random_number = 0
count = 0       
  
# a forever loop until we interrupt it or  
# an error occurs 
while True:
	c, addr = s.accept()
	print ('Got connection from', addr)
		
	while True:
		from_client = c.recv(1024).decode()
		print("from Client : " + from_client)
		if(from_client.find('Hi') != -1):
			name = from_client.split(" ",2)
			random_number = random.randint(1,100)
			c.sendall("READY".encode())
		else:
			count = count+1
			if(int(from_client) == random_number):
				c.sendall(("Correct! "+name[1]+" no of guesses "+str(count)).encode())
				c.close()
				break
			if(int(from_client)>random_number):
				c.sendall("HIGH".encode())
			if(int(from_client)<random_number):
				c.sendall("LOW".encode())
	
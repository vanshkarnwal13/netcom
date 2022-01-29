import socket
import threading
import sys
s=socket.socket() #cretes a default socket
port = 13877  # reserve a port on your computer                
s.connect(('127.0.0.1', port)) #for connecting with this IP address with the server
s.send('Thank you for connecting with the client'.encode())
print (s.recv(2048).decode())
#for receiving message from the server and check if server want to end the connection
def receive():
  while True:
      
            msg = s.recv(2048).decode()
                
            print ("server message:'%s'\n" %msg)
            if(msg=="close" or msg==''):
                print ("closing now")
                #close connection with client
                s.close()
                break
      
def send():
    while True:
        try:
            msg=input()
            s.send(msg.encode())
        except:
            print ("closing now")
            s.close()
            break

clientreceive_thread=threading.Thread(target=receive)
clientsend_thread=threading.Thread(target=send)
clientreceive_thread.start()
clientsend_thread.start()
clientreceive_thread.join()
sys.exit()

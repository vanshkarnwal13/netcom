import socket
import threading
import sys
s=socket.socket() #cretes a default socket
print("Socket created sucessfully")
port = 13877  # reserve a port on your computer             
s.bind(('', port))    #bind to the port here it is empty so comp listens to any comming resquest from other comp   
print ("socket binded to %s" %(port))

s.listen(5)    #socket will accept 5 connections and socket is listening to that connection 
print ("socket is listening")   
        
c, addr = s.accept() #establish connection with client
print ('Got connection from', addr )
c.send('Thank you for connecting with the server- VANSH KARNWAL 20BCT0182'.encode())
print (c.recv(2048).decode())

#receiving the message from the client and continuos loop until interuuption or error or client want to end the connection
def receive():
    while True:
        
      #close connection with client
            msg = c.recv(2048).decode()
            print ("client message:'%s'\n" %msg)
            if(msg=="close" or msg==''):
                print ("closing now")
                c.close()
                #breaking once connection is closed
                break
          
#for  sending  messages to the client  until client stop the process    
def send():
    while True:
        try:
            #msg=input("your message:\n")
            msg=input()
            
            c.send(msg.encode())
        except:
            print ("closing now")
            c.close()
            break
receive_thread=threading.Thread(target=receive)
send_thread=threading.Thread(target=send)
receive_thread.start()
send_thread.start()
receive_thread.join()
sys.exit()

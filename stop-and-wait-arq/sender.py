#vansh karnwal 20BCT0182
import socket
import threading
import time
s=socket.socket() 
print("welcom to vansh karnwal(20bct0182) sender")
print("Socket created sucessfully")
port = 12345               
s.bind(('', port)) 
print ("socket binded to %s" %(port))
s.listen()    
print ("socket is listening")           
c, addr = s.accept()
print ('Got connection from', addr )
print("Enter the number of frames you want to send")
numberOfFrames=int(input())

frames=[]
for i in range(numberOfFrames):
    frames.append(i%2)
c.send(str(numberOfFrames).encode())

print ("Starting to send the data")

acknowledgementReceived=-1

def receive():
    try:
        global acknowledgementReceived
        msg = c.recv(1).decode()
        if(msg=="c"):
            print ("Done")
            c.close()
            acknowledgementReceived=-1
            print ("closing acknowledgement received")
            return
        print ("received acknowledgement for "+str(msg)+" frame")
        print("\n")
        acknowledgementReceived=int(msg)
    except:
        return
idx=0
flag=0    
flag2=1
while True:
    
    if(idx==numberOfFrames):
        break
    print ("Sending "+str(frames[idx])+" frame with value "+str(idx+1))
    
    c.send(str(frames[idx]).encode())
    
    receive_thread=threading.Thread(target=receive)
    receive_thread.start()
   
    time.sleep(0.5)    
    if(acknowledgementReceived==-1):
        break
    if(acknowledgementReceived==(frames[idx]+1)%2):
        print ("correct acknowledgement received")
        print("\n")
        idx+=1
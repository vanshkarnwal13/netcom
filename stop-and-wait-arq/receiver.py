#vansh karnwal 20BCT0182
import socket
import threading
import time
s=socket.socket() 
print("welcom to vansh karnwal(20bct0182) receiver")
print("\n")
port = 12345               
s.connect(('127.0.0.1', port))
numberOfFrames=int(s.recv(2).decode())
frames=[]
for i in range(numberOfFrames):
    frames.append(i%2)   
acknowledgement=-1

def send():
    global acknowledgement
    s.send(str(acknowledgement).encode())    
idx=0
flag=0    
flag2=1
while True:   
    msg=s.recv(1).decode()
    print("Received "+msg+" frame with value "+str(idx+1))
    if(int(msg)==frames[idx]):
        print("frame accepted")
        print("\n")
        acknowledgement=(int(msg)+1)%2
        idx+=1
    else:
        print("frame discarded")
        print("\n")
       
    if(idx==numberOfFrames):
        print("sending closing acknowledgement")  
        print("\n")  
        s.send("c".encode())
        break
    
    print("sending acknowledgement for "+str(acknowledgement)+" frame")    
    print("\n")
    send_thread=threading.Thread(target=send)
    send_thread.start()
   
    time.sleep(1)       
print ("Done")
time.sleep(2)
s.close()


import socket
import select
import threading
import time
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket successfully created.")
IP = "127.0.0.1"  
port = 3000 
serverSocket.bind((IP,port))
serverSocket.listen()
print("VANSH KARNWAL(20BCT0182)")
print("Socket(Server) is currently active and listening to requests!!")
socketsList = [serverSocket]
clients = {}
m = int(input("Enter the size of the sequence number field in bits : "))
total_frames = int(input("Enter the total frames to be sent : "))
sequence = []
for i in range(0,(2**m)):
    sequence.append(i)
sf = 0
sn = 0
frames_sent = 1
alarm = 0

sent = []
for i in range(total_frames):
    sent.append(0)

# A function to recieve messages from the clients connected over the network
def recieveMessage(clientSocket):
    try:
        return {"Data" : clientSocket.recv(7)}
    except: 
        return False
    
def recieve_ack(notifiedSocket):
    global sf,sn,frames_sent
    while True:           
        if(sf<=sn):
            ack_message = recieveMessage(notifiedSocket)
            if(ack_message['Data'].decode()):
                if(ack_message['Data'].decode()[0]=='A'):
                    user = clients[notifiedSocket]
                    print(f"{user['Data'].decode()} >> {ack_message['Data'].decode()}")
                    if(int(ack_message['Data'].decode()[-1])>=(sf+1) or int(ack_message['Data'].decode()[-1])==0):
                        sent[int(ack_message['Data'].decode()[-1]) - 1] = 1
                        print("Correct Acknowledgement Recieved")
                        difference = (int(ack_message['Data'].decode()[-1])-(sf))
                        if(difference>=0):   
                            sf = sf + difference
                            frames_sent = frames_sent + difference
                            if(sf>=(2**m-1)):
                                sf = sf - (2**m)
                        else:
                            difference = difference + (2**m)
                            sf = sf + difference
                            frames_sent = frames_sent + difference
                            if(sf>=(2**m-1)):
                                sf = sf - (2**m)
                        if(difference > 1):
                            print("Number of Jumped acknowledgement : ",difference-1)
                else:
                    user = clients[notifiedSocket]
                    print(f"{user['Data'].decode()} >> {ack_message['Data'].decode()}")
                    message = "Frame : " + str(sequence[int(ack_message['Data'].decode()[-1])])
                    notifiedSocket.send(message.encode())
   
def timer():
    global alarm,sf,sn
    while True:
        time.sleep(1.5)
        if(sf!=sn):
            alarm = (alarm + 1) % 2
thread3 = threading.Thread(target = timer, args = ())
thread3.start() 
# Making a thread for every user connected to the server
def clientThread(notifiedSocket):
    global sf,sn,frames_sent,total_frames,alarm
    temp_flag = 0
    while (frames_sent!=total_frames):          
        if(alarm==1):
            print("Timer Expired")
            print("Resending Frames")
            for i in range(sf,sf+2**(m-1)):
                if(sent[i] != 1):
                    message = "Frame : " + str(sequence[sn])
                    notifiedSocket.send(message.encode())  
            alarm = 0
        if((sn-sf)<=(2**(m-1)-1) and (sn<=(2**m-1))):
            time.sleep(1)
            message = "Frame : " + str(sequence[sn])
            if(sn==3 and temp_flag==0):
                print("Not sending Third Frame for the first time :")
                temp_flag = 1
            else:
                notifiedSocket.send(message.encode())
            sn = sn + 1
            if(sn>=(2**m)):
                sn = sn - (2**m)
            # The part to do if a client leaves the connection
            if message is False:
                print("The message is False")
                print(f"Closed Connection from {clients[notifiedSocket]['Data'].decode()}")
                socketsList.remove(notifiedSocket)
                del clients[notifiedSocket]
                break
    else:
        sf = sf + 1
        print("All the frames were sent successfully")

# Listening to requests infinitely untill interupted
while True:
    # Accepting the user and storing its address in the below defined variables
    clientSocket, clientAddress = serverSocket.accept()
    # Getting the information user wants to send
    user = recieveMessage(clientSocket)
    if user is False:
        continue
    socketsList.append(clientSocket)
    clients[clientSocket] = user
    print(f"Connection from {clientAddress} has been established!! : UserName : {user['Data'].decode()}") 
    clientSocket.send(str(m).encode())
    # Sending the count of total frames
    clientSocket.send(str(total_frames).encode())
    msg = "Welcome to the server,Thanks for connecting!!"
    # Sending information to client socket
    clientSocket.send(msg.encode())
    thread = threading.Thread(target = clientThread, args = (clientSocket,))
    thread.start()
    thread2= threading.Thread(target = recieve_ack, args = (clientSocket,))
    thread2.start()
    
import socket
import threading
ip = "127.0.0.1"
port = 55555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip,port))
print("socket created and binded to port {}".format(port))
server.listen()
print("socket is listening")
sockets_list = [server]
clients_dict = {}

def disp(client,message):
    for c in clients_dict.keys():
        if c!=client:
            c.send(message)

def display(client):
    while True:
        try:
            message=client.recv(1024)
            print("Message from client {}".format(message.decode("ascii")))
            disp(client,message)
        except:
            print("Client {} has disconnected".format(clients_dict[client]))
            disp(client,"\n{} left!".format(clients_dict[client]).encode("ascii"))
            clients_dict.pop(client)
            client.close()
            break

def servermsg():
    while True:
        s=input("enter message: ") 
        disp(server,"Message from Server: {}".format(s).encode("ascii"))         
         
write = threading.Thread(target=servermsg)
write.start()           
while True:
    client, addr = server.accept()
    print("Connected with address: {}".format(str(addr)))
    client.send("username".encode("ascii"))
    username = client.recv(1024).decode("ascii")
    if len(username):
        clients_dict[client]=username
    print("Username is: {}".format(username))
    disp(client,"{} joined the server!!!".format(username).encode("ascii"))
    client.send("Welcome to the server {}!!!".format(username).encode("ascii"))
    thread = threading.Thread(target=display, args=(client,))
    thread.start()
    


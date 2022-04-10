
import socket
import threading
u = input("enter name: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "username":
                client.send(u.encode("ascii"))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        try:
            i = input("")
            message = "{}: {}".format(u, i)
            client.send(message.encode("ascii"))
        except:
            print("\nAn error has occurred\n")
            client.close()
            break
receive = threading.Thread(target=receive)
receive.start()
write = threading.Thread(target=write)
write.start()

import socket
from ssl import SOCK_STREAM
import threading

client_HOST = socket.gethostbyname(socket.gethostname()) # here, the server's IP address should be assigned because the client side socket is not hosting any
# server but is simply connecting to an existing one. In this case, 'client_HOST' is the same local, private IPv4 address from
# 'Ethernet Adapter Virtualbox' as server and client both are present on the same local IP. In order to connect to a server with another
# IP, the local, private IPv4 address of that server should be assigned here IF BOTH SERVER AND CLIENT BELONG TO THE SAME Local Area
# Network(LAN). If the client wants to connect to a server which is not a part of the LAN and is somewhere on the internet, then the 
# GLOBAL, PUBLIC IP address(modem's IP) of the server must be assigned to 'client_HOST' and NOT the private, local IP.
PORT = 9090

#stop_thread = False #global variable initially False.

ncknm = input("Enter the client's nickname:")
#if ncknm == "admin": # we are just anticipating the process and getting user input for password. This will be sent to the server only if
#    password = input("Enter password for admin:") # 'PASS' keyword is recieved.

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((client_HOST, PORT)) # at the client side, the socket is simply connecting to an existing server whose IPv4 
# and port number is specified in the argument tuple. On executing this method, the 'server_socket.accept()' method will be trigerred.
# and thus the client gets connected to the server.


#there will two methods and two threads running in the client. Each thread having one of the two methods as 'target' function.

def recieve():
    while True:
        """
        global stop_thread  
        if stop_thread == True: #whenever 'stop_thread' is made True, the while loop will break out of the NEXT iteration.
            break
        """
        try:
            message_recvd = client_socket.recv(1024).decode('utf-8')
            if message_recvd == "NICK": 
                client_socket.send(ncknm.encode('utf-8'))
                """
                next_message = client_socket.recv(1024).decode('utf-8')
                if next_message == "PASS": #this keyword will only be recieved if nickname sent was 'admin'.
                    client_socket.send(password.encode('utf-8'))
                    response_msg = client_socket.recv(1024).decode('utf-8')
                    if response_msg == "REFUSED":
                        print("Connection was REFUSED due to incorrect password!")
                        stop_thread = True
                elif next_message == "BAN":
                    print("Coonection REFUSED because you were banned!")
                    client_socket.close()
                    stop_thread = True 
                """
            else:
                print(message_recvd)
        except:
            print("An error ocurred!")
            client_socket.close()
            break



def write():
    while True:
        #if stop_thread == True: #cuz even if recieve thread will break if wrong password is entered, write thread will still continue
        #    break  #so that the client will not be able to recieve messages but will be able to send messages. We want both of these
            #threads to stop. this is why we're doing this.
        msg_raw = input("")
        """
        if msg_raw.startswith('/'):
            if ncknm == "admin":
                if msg_raw.startswith('/kick'): #msg_raw will be of type "/kick {nickname}" or "/ban {nickname}"
                    client_socket.send(f"KICK {msg_raw[6:]}".encode('utf-8')) #we are sending "KICK {nickname}" to the server.
                elif msg_raw.startswith('/ban'):
                    client_socket.send(f"BAN {msg_raw[5:]}".encode('utf-8')) #we are sending "BAN {nickname}" to the server.
            else:
                print("Commands can only be executed by the admin!")
        else:
        """
        messg_to_send = f"{ncknm} : {msg_raw}"
        client_socket.send(messg_to_send.encode('utf-8'))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()




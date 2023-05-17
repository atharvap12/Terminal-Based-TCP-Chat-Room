import socket
import threading
import hashlib
"""
TRUE_HASH = hashlib.sha256("adminpass".encode('utf-8')).hexdigest() #hexdigest of the sha256 hash of the true password "adminpass".
"""
server_HOST = '192.168.15.174' #enter 'ipconfig' on command prompt and get the local private IPv4 address from 'Wireless LAN adapter 
# WiFi'

host = socket.gethostbyname(socket.gethostname()) #alternate way to get local IPv4 address but returns ethernet adapter virtualbox 
#IPv4 address if you have virtualbox running on your device

PORT = 9090 #port number can be explained as one of the many doors to a room. The server represents the room and port number is just 
# one of the many doors that can be used to enter into it. Each port number provides a specific service to the client that connects to
# it. The first 1024 ports are already reserved for standard services and cannot be used for user defined services. E.g port 80 
# provides standard HTTP service, 443 provides HTTPS service, 80 provides SSH service, etc. Max. range of port no. is 65535.


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #server side socket object is the endpoint for server side communication
# The first argument 'AF_INET' specifies the family of our socket object which is an INTERNET socket. Sockets can also be of family
# AF_BLUETOOTH which are bluetooth based sockets. There are also infrared and radio socket. 'AF_INET6' is for IPv6 Internet sockets.
# The second argument 'SOCK_STREAM' signifies that following socket uses TCP for file transmission. 'SOCK_DGRAM' uses UDP protocol 
# to transfer files.

server_socket.bind((host, PORT)) # we bind the server_socket to the local IPv4 of this device and PORT number 9090

server_socket.listen(5) #this makes the socket ready to accept connections. Integer argument is the size of queue into which max. 
# number of client requests are queued.

clients_list = [] #list of client_sockets connected to the server.
nicknames_list = [] #list of corresponding nicknames of each client connected to the server. Client enters its nickname.

def broadcast(message):  #simply sends a message to all the clients connected to the server.
    for client in clients_list:
        client.send(message)

# this func. is called when the client is successfully connected to the server. This takes care of the communication of the 'client_socket' 
# passed as argument with every other client connected to the server. This func. continuously recieves message from a client, decodes it,
#  and broadcasts it to every other client(by calling broadcast). If an exception is ocurred, it closes the connection of the 
# 'client_socket' and removes it from the global clients_list and nicknames_list.
def handle(client_conn_socket):
    while True:
        try: 
            msg = message = client_conn_socket.recv(1024) #this the standard buffer size of the input message in bytes. There's also a 
            #protocol according to which we can take input of size first and then allocate the buffer of the user entered size.

            #msg is for the if-conditions and message is for broadcasting. If we try to pass the same variable through if-statements and
            #broadcast function, it gets stuck in loops and gives errors.
            """
            if msg.decode('utf-8').startswith("KICK"):
                if nicknames_list[clients_list.index(client_conn_socket)] == "admin":
                    name_to_kick = msg.decode('utf-8')[5:] #slicing out the first 5 chars.
                    kick_nickname(name_to_kick)
                else:
                    print("Commands can only executed by admin!")
            elif msg.decode('utf-8').startswith("BAN"):
                if nicknames_list[clients_list.index(client_conn_socket)] == "admin":
                    name_to_ban = msg.decode('utf-8')[4:] #slicing out the first 4 chars.
                    kick_nickname(name_to_ban)
                    with open('banned.txt', 'w') as f:
                        f.write(f"{name_to_ban}\n")
                    print(f"{name_to_ban} was banned!")
                else:
                    print("Commands can only be executed by admin!")
            # IMP_NOTE: If the client simply sends a message starting with 'KICK' or 'BAN' instead of '/kick' or '/ban', the function
            # to kick or ban will not be trigerred, because the message recieved at the server's side is '{nickname} : {raw_message}'
            # and some preprocessing has to be done to remove this 'nickname' from the message sent which will only happen at the
            # client side if the raw_msg startswith '/'
            else:
            """
            broadcast(message)
        except:
            #if client_conn_socket in clients_list:
            cindex = clients_list.index(client_conn_socket) #to get the index number of the given 'client_socket' from clients_list
            cnickname = nicknames_list[cindex]
            clients_list.remove(client_conn_socket)
            client_conn_socket.close()
            broadcast(f"{cnickname} has left the chat!".encode('utf-8'))
            nicknames_list.remove(cnickname)
            break



# this func. acts as the main function and combines both the above functions. This function is the first one to be called which is
# continuously listening and accepts a 'client_socket' trying to connect to the server, let's everyone else in the room know that
# the following client has joined the chat, and creates a new thread of the handle function which handles the communication of the newly 
# joined client.
def recieve():
    while True:
        client_conn_socket, client_address = server_socket.accept() # 'client_conn_socket' is the new client-side communication socket 
        # obj. returned by the accept() method of server_socket. send() and recv() methods are called on this client-side communication obj.
        # returned by the 'server_socket.accept()' method and not on 'server_socket'. However, these methods can be generally called on a 
        # socket obj.
        print(f"Connected with {str(client_address)}")
        client_conn_socket.send("NICK".encode('utf-8')) # this is the keyword sent for accepting nickname from the newly connected client.
        nickname = client_conn_socket.recv(1024).decode('utf-8')
        """
        with open('banned.txt', 'r') as f:
            all_bans = f.readlines() #list of banned names and '\n'
        
        if nickname + '\n' in all_bans:
            client_conn_socket.send("BAN".encode('utf-8'))
            client_conn_socket.close()
            continue #skip the current iteration but do not terminate the loop.

        if nickname == "admin":
            client_conn_socket.send("PASS".encode('utf-8')) #another keyword sent to the client which will indicate the client to send password.
            plain_password = client_conn_socket.recv(1024).decode('utf-8')
            #hashed_password = hashlib.sha256(plain_password.encode('utf-8')).hexdigest() #we hash the plain text password recieved 
            # using sha256 algo. It is first encoded with 'utf-8'. hexdigest() of this hash is stored here.
            if plain_password != "adminpass": 
                client_conn_socket.send("REFUSED".encode('utf-8')) #another keyword sent to the client indicating connection refused.
                client_conn_socket.close()
                continue # WE ARE NOT GOING TO 'break' THIS LOOP. BECAUSE THIS THREAD CONTINUOUSLY RUNS SO THAT SERVER CAN RECIEVE
                # NEW CLIENT CONNECTIONS. WE ARE ONLY GOING TO SKIP THIS ATTEMPT OF THE CLIENT TRYING TO CONNECT WITH A WRONG PASSWORD.
                # Therefore, the server can recieve the connection requests of other clients.
        
        """
        nicknames_list.append(nickname)
        clients_list.append(client_conn_socket)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} has joined the chat!".encode('utf-8'))
        client_conn_socket.send("Connected to the server.".encode('utf-8'))

        client_thread = threading.Thread(target=handle, args=(client_conn_socket,)) #creates a new thread of the 'handle' function 
        # as the target with the a tuple of (client_conn_socket,) sent as argument. A new thread of every connected client will run 
        # parallelly so that all clients can simultaneously communicate.
        client_thread.start() 

"""
def kick_nickname(nname):
    if nname in nicknames_list:
        nname_index = nicknames_list.index(nname)
        client_to_kick = clients_list[nname_index]
        clients_list.remove(client_to_kick)
        client_to_kick.send("You were kicked by an admin!".encode('utf-8')) #coz 'client_to_kick' will be a socket object.
        client_to_kick.close()
        nicknames_list.remove(nname)
        broadcast(f"{nname} has been kicked by an admin.".encode('utf-8'))
"""





print(socket.gethostname() + " : " + host )
print("Server is listening...")
recieve()


# Import required modules
import socket
import threading
import os
from ppadb.client import Client as AdbClient

HOST = '192.168.100.6'
PORT = 1234 # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users
disconnect_message = "exit"

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
device = devices[0]

file = open("server_messages.txt", "w")
file.write("Connected to server\n")
file.close()
device.push("server_messages.txt", "/sdcard/PythonChat/server_messages.txt")
#find recived_messages.txt and delete it if it exists in the current directory


def lisent_for_file_updates():
    last_lines = 0
    while True:
        #we will open a file named received_messages.txt and read the last line
        #if the last line is not the same as the last message we received
        #we will send the message to all the clients
        try:
            device.pull("/sdcard/PythonChat/recived_messages.txt", "recived_messages.txt")
            f = open("recived_messages.txt", "r")
            #get all the lines in the file
            lines = f.readlines()
            #check if the last line is not the same as the last message we received
            if last_lines < len(lines):
                for i in range(last_lines, len(lines)):
                    send_messages_to_all("USB Device~"+lines[i])
                last_lines = len(lines)
        except Exception as e:
            
            pass

# Function to listen for upcoming messages from a client
def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '' and message != disconnect_message:
            final_msg = username + '~' + message
            file = open("server_messages.txt", "a")
            file.write(f'[{username}] {message}' + "\n")
            file.flush()
            device.push("server_messages.txt", "/sdcard/PythonChat/server_messages.txt")
            send_messages_to_all(final_msg)
            file.close()
        elif message == disconnect_message:
            prompt_message = "SERVER~" + f"{username} left the chat"
            print(prompt_message)
            file = open("server_messages.txt", "a")
            file.write(f'[SERVER] {username} left the chat' + "\n")
            file.flush()
            device.push("server_messages.txt", "/sdcard/PythonChat/server_messages.txt")
            send_messages_to_all(prompt_message)
            active_clients.remove((username, client))
            client.close()
            file.close()
            break

        else:
            print(f"The message send from client {username} is empty")


# Function to send message to a single client
def send_message_to_client(client, message):

    client.sendall(message.encode())

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    # Write the message to the file
    
    
    for user in active_clients:

        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    
    # Server will listen for client message that will
    # Contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            file = open("server_messages.txt", "a")
            file.write(f'[SERVER] {username} added to chat' + "\n")
            file.flush()
            device.push("server_messages.txt", "/sdcard/PythonChat/server_messages.txt")
            send_messages_to_all(prompt_message)
            file.close()
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()
    

# Main function
def main():

    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)
    threading.Thread(target=lisent_for_file_updates).start()
    # This while loop will keep listening to client connections
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()
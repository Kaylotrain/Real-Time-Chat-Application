# import required modules
import socket
import threading


HOST = '127.0.0.1'
PORT = 1234



# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():

    # try except block
    try:

        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")

    username = input("Enter your username: ")
    if username != '':
        client.sendall(username.encode())
    else:
        print("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()


def send_message():
    message = input()
    if message != '':
        client.sendall(message.encode())
    else:
        print("Empty message", "Message cannot be empty")




def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            print(f"[{username}] {content}")
            
        else:
            print("Error", "Message recevied from client is empty")

# main function
def main():
    connect()
    #create a thread to listen for messages from server and another thread to send messages to server
    while 1:
        send_message()
    
    

if __name__ == '__main__':
    main()
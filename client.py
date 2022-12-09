# import required modules
import socket
import threading


HOST = '192.168.100.6'
PORT = 1234
disconnect_message = "exit"
disconnected = False

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



def listen_for_messages_from_server(client):
    global disconnected
    while not disconnected:

        message = client.recv(2048).decode('utf-8')
        #check if the mesage contains the word SERVER and the name of this user
        
        
        if message != '':
            
            username = message.split("~")[0]
            content = message.split('~')[1]
            if username == "SERVER" and content == f"{username} left the chat":
                disconnected = True
                break
            print(f"[{username}] {content}")
            
        else:
            break

# main function
def main():
    global disconnected
    connect()
    #create a thread to listen for messages from server and another thread to send messages to server
    while not disconnected:
        try:
            message = input()
            if message != '':
                client.sendall(message.encode())
                if message == disconnect_message:
                    disconnected = True
                    break
            else:
                print("Empty message", "Message cannot be empty")
        except:
            break

if __name__ == '__main__':
    main()
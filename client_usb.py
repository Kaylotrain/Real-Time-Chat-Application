import threading
import os
exit_message = "exit"
exited = False

file = open("recived_messages.txt", "w")
file.write("Connected to server\n")
file.close()
#find recived_messages.txt and delete it if it exists in the current directory

def read_message():
    last_lines = 0
    while not exited:
        #open the file named server_messages.txt
        try:
            f = open("server_messages.txt", "r")
            #get all the lines in the file
            lines = f.readlines()
            #check if the last line is not the same as the last message we received
            if last_lines < len(lines):
                for i in range(last_lines, len(lines)):
                    print(lines[i])
                last_lines = len(lines)
        except:
            pass

t = threading.Thread(target=read_message)
t.start()

while True:
    message = input()
    file = open("recived_messages.txt", "a")
    if message == exit_message:
        file.write( " left the chat " + "\n")
        exited = True
        break
    
    file.write( message + "\n")
    file.close()
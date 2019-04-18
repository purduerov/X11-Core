#!/usr/bin/env python3

import socket
import re
import traceback
import signal
import sys

def closeSocket(socket):
    def signal_handler(sig, frame):
        print("\nCtrl+C signal sensed!\nClosing the socket...")
        socket.close()
        sys.exit(0)

    return signal_handler

def send(sock, mess):
    sock.send(mess.encode('utf-8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind(('127.0.0.1', 5001))
        s.listen(1)

        client, address = s.accept()
        text = ''

        signal.signal(signal.SIGINT, closeSocket(s))

        while text != "end":
            send(client, 'hello from server')
            text = client.recv(1024).decode("utf-8")
            print(text)

            if text == "quit":
                text = "end"
                print("A.k.a. end")

    except:
        print(traceback.format_exc())

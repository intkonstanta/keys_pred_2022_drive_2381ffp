import socket
import gpio
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8000))

while True:

    letter = input()
    client.send(letter.encode("utf-8"))

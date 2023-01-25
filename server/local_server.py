import socket
import asyncio

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # поднимаем сервак
server.bind(("192.168.1.4", 8000))
server.listen()

while True:
    user, adrs = server.accept() # ждём подключение первого клиентов, и работаем с ним.
    print(user, adrs)
    break # закрываем считывание новых клиентов

while True:
    letter = input()

    user.send(letter.encode("utf-8"))

    data = user.recv(1024) # слушаем порт

    if data: # если чё-то есть, выводим
        print(data.decode("utf-8"))

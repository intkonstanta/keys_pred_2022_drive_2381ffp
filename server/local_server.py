import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # поднимаем сервак
server.bind(("127.0.0.1", 8000))
server.listen()

while True:
    user, adrs = server.accept() # ждём подключение первого клиентов, и работаем с ним.
    break # закрываем считывание новых клиентов

while True:
    data = user.recv(1024) # слушаем порт
    if data: # если чё-то есть, выводим
        print(data.decode("utf-8"))

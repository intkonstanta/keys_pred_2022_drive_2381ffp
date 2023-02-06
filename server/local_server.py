import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # поднимаем сервак
server.bind(("192.168.1.4", 8000))
all_users = []
connect_flag = 0
server.listen()

while connect_flag == 0:
    user, adress = server.accept()
    if adress not in all_users:
        all_users.append(adress)
        print(all_users)
        connect_flag = int(input())



 while True:
     for user, adress in all_users:
        data = user.recv(1024) # слушаем порт
        if data: # если чё-то есть, выводим
            data = data.decode("utf-8")



import socket
import struct
from datetime import datetime
import sys


attempts = 1
time_out = 1
multicast_group = ('224.51.105.104', 2340)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

start_words = ["1", "y", "Y", "yes", "Yes", "True", "true"]
stop_words = ["0", "n", "N", "no", "No", "False", "false"]
start_word = None



while True:
    list_all_connects = []
    while list_all_connects == []:
        flag_cs = input("Connect clients?[Y/N]: ")

        #control sum
        sock.settimeout(time_out)
        if flag_cs in start_words:
            sent = sock.sendto(b"1", multicast_group)
            print("Сlient connection started:")
            while True:
                try:
                    data_recv, address = sock.recvfrom(1024)
                except socket.timeout:
                    break
                else:
                    if address not in list_all_connects:
                        list_all_connects.append(address)
                        print(f"+ Client {address} connected")
            if list_all_connects:
                print(f"Client connection ended, connected clients: {list_all_connects}")
            else:
                print(f"No client connects, try again...")

    else:

        while start_word not in start_words:
            start_word = input("Start recording clients telemetry?[Y/N]: ")
            if start_word in start_words:

                print("Input race info:")
                num_of_comp = input("Num of comp: ")
                type_of_race = input("Type of race[1/2/3/4/8/16/32/q]: ")
                count_of_memb = input("Count of members: ")

                comp_stage_info = num_of_comp + " " + type_of_race + " " + count_of_memb
                message = bytes(comp_stage_info, 'utf-8')

                for i in range(attempts):
                    try:
                        sent = sock.sendto(message, multicast_group)
                        print(f"Race info sent to clients; info: {message.decode('utf-8')}, time: {datetime.now()}")
                    except OSError:
                        print('Failed sanding race info, try again...')

        print("Recording telemetry has been started")
        print("...recording telemetry...")
        sock.settimeout(70)
        while list_all_connects:
            try:
                data_recv, address = sock.recvfrom(1024)
            except sock.timeout:
                print("FAILED! telemetry was not sent еto DB, try recording telemtry again!")
                sock.close()
                exit()
            finally:
                if (data_recv.decode('utf-8') == "fr") and (address in list_all_connects):
                    list_all_connects = list_all_connects.remove(address)
                    print(f"- Client {address} sent telemetry to DB and disconnect")

        print(f"Successful recording, all data sent to DB\n")



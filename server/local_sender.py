import socket
import struct
from datetime import datetime
import sys


attempts = 1
time_out = 1
multicast_group = ('224.51.105.104', 2350)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

start_words = ["1", "y", "Y", "yes", "Yes", "True", "true"]
stop_words = ["0", "n", "N", "no", "No", "False", "false"]
start_word = None

sock.settimeout(time_out)

while True:
    control_sum = 0
    flag_cs = input("Connect clients?[Y/N]: ")

    #control sum

    if flag_cs in start_words:
        sent = sock.sendto(b"1", multicast_group)
        while True:
            print("start receive")
            try:
                data_recv, address = sock.recvfrom(1024)
            except socket.timeout:
                break
            else:
                control_sum += 1
                print(f"{data_recv} control_sum now == {control_sum}")

        print(f"!finish connecting! control_sum = {control_sum}")

        # while socket.timeout:
        #     str(socket.timeout)
        #     data_recv, address = sock.recvfrom(1024)
        #     data_recv.decode('utf-8')
        #     print(f"{data_recv}")
        # print("finish connecting")

    #recording telemetry
    else:
        comp_stage_info = input("num_of_comp/type_of_stage/count_of_memb: ")
        message = bytes(comp_stage_info, 'utf-8')
        while start_word not in start_words:
            start_word = input("Start recording?[Y/N]: ")
            if start_word in start_words:
                for i in range(attempts):
                    try:
                        sent = sock.sendto(message, multicast_group)
                        print(f"Package sent: {message.decode('utf-8')}, time: {datetime.now()}")
                    except OSError:
                        print('Failed sanding packet!')
            if start_word in stop_words:
                print("Goodbye!")
                sock.close()
                exit()

        print("Recording has been started")
        while True:
            print("start receive")
            try:
                data_recv, address = sock.recvfrom(1024)
            except socket.timeout:
                break
            else:
                control_sum -= 1
                print(f"{data_recv} control_sum now == {control_sum}")

        if control_sum == 0:
            print(f"Succsesful recording, control sum entire!")


sock.close()
exit()

import socket
import struct
from datetime import datetime
import sys


attempts = 1
comp_stage_info = input("num_of_comp/type_of_stage/count_of_memb: ")
message = bytes(comp_stage_info, 'utf-8')
multicast_group = ('224.51.105.104', 2349)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

start_words = ["1", "y", "Y", "yes", "Yes", "True", "true"]
stop_words = ["0", "n", "N", "no", "No", "False", "false"]
start_word = None

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

sock.close()
print("Recording has been started")

import json
import time
import pathlib
import os
import sys
import socket
import struct
from datetime import datetime

multicast_group = '224.51.105.104'
server_address = ('', 2350)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("IP local:", socket.gethostbyname(socket.gethostname()))
basedir = os.path.abspath(os.getcwd())
print(basedir)

all_data = {
    'all_data': []
}

time_to_rec = 60.1 # Recording duration
request_rate = 10 # Requests per second
request_rate = 1 / request_rate

while True:
    # create name indx of telemetry file
    data_recv, address = sock.recvfrom(1024)
    if data_recv:
        file_text = data_recv.decode('utf-8')
        print(f"Package received: '{file_text}', {address}")
        start_rec_time = time.time()
        if file_text == "1":
            sent = sock.sendto(b"1", address)
        else:
            print("Start new file recording:")
            file_name = f"{file_text.split(' ')[0]} {file_text.split(' ')[1]} " \
                        f"{file_text.split(' ')[2]} {socket.gethostbyname(socket.gethostname())}.json"

            # create file or rewrite
            time_delta_start = 0.0
            with open(file_name, 'w') as file_rec:
                while time_delta_start <= time_to_rec:
                    client_id = socket.gethostbyname(socket.gethostname())
                    mpu6050_acc_x = None
                    mpu6050_acc_y = None
                    mpu6050_acc_z = None

                    gy_273_az_N = None

                    gyneo7m_cor_x = None
                    gyneo7m_cor_y = None
                    gyneo7m_speed = None
                    gyneo7m_high = None


                    data = {
                        "id": client_id,
                        "time": f"{time_delta_start:.3}",
                        "mpu6050": [mpu6050_acc_x, mpu6050_acc_y, mpu6050_acc_z],
                        "gy273": gy_273_az_N,
                        "gyneo7m": [gyneo7m_high, gyneo7m_speed, gyneo7m_cor_x, gyneo7m_cor_y],
                        "real_time": str(datetime.now())
                        }

                    time.sleep(request_rate)
                    time_delta_start = time.time() - start_rec_time
                    all_data['all_data'].append(data)
                    print(data)
                json.dump(all_data, file_rec)

            print("File recording finished!")
            time_delta_start = 0.0
            #add file in DB
            sent = sock.sendto(b"2", address)
            # name_indx += 1


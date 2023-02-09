import json
import time
import pathlib
import os
import sys
import socket
import struct
from datetime import datetime

multicast_group = '224.1.1.1'
server_address = ('', 10000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("IP local:", socket.gethostbyname(socket.gethostname()))
basedir = os.path.abspath(os.getcwd())
print(basedir)

time_to_rec = 60.1 # Recording duration
request_rate = 10 # Requests per second
request_rate = 1 / request_rate

while True:
    # create name indx of telemetry file
    data_recv, address = sock.recvfrom(1024)
    if data_recv:
        print(f"Package received: '{data_recv.decode('utf-8')}', {address}")
        print("Start new file recording:")
        start_rec_time = time.time()
        file_basedir = os.listdir(basedir)
        max_indx = 0
        for file_name in file_basedir:
            try:
                if int(file_name) > max_indx:
                    max_indx = int(file_name)
            except Exception:
                print(f"{file_name} file not telemetry file ==> skip...")
        name_indx = max_indx + 1
        print(f"New filename indx: {name_indx}")

        # create file or rewrite
        time_delta_start = 0.0
        with open(str(name_indx), 'w+') as file_rec:
            info_comp_recv = json.dumps({
                "type": data_recv.decode('utf-8').split(" ")[0],
                "party": data_recv.decode('utf-8').split(" ")[0],
                 "id": socket.gethostbyname(socket.gethostname()),
                "time_rec": str(datetime.now())
            })
            file_rec.write(info_comp_recv + "\n")
            print(info_comp_recv)
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
                    "gyneo7m": [gyneo7m_high, gyneo7m_speed, gyneo7m_cor_x, gyneo7m_cor_y]
                    }

                time.sleep(request_rate)
                time_delta_start = time.time() - start_rec_time
                data = json.dumps(data)
                file_rec.write(data + "\n")

                print(data)
        print("File recording finished!")
        time_delta_start = 0.0
        name_indx += 1


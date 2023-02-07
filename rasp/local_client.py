import json
import socket
import time
import pathlib
import os


UDP_IP = "127.0.0.1"
UDP_PORT = 8000

client_id = UDP_IP + ":" + str(UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


while True:
    # create name indx of telemetry file
    basedir = os.path.abspath(os.getcwd())
    print(basedir)
    flag = int(input("Чтобы начать запись, введите 1: "))
    if flag == 1:
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
        print(f"new name indx = {name_indx}")
        # create file or rewrite
        time_delta_start = 0.0
        with open(str(name_indx), 'w+') as file_rec:
            while time_delta_start <= 60.1:
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

                time.sleep(0.1)
                time_delta_start = time.time() - start_rec_time
                data = json.dumps(data)
                file_rec.write(data + "\n")

                print(data)
        time_delta_start = 0.0
        name_indx += 1


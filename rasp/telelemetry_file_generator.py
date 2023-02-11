from datetime import datetime

with open("file_telemetry.csv", 'w') as file:
    file.write("time,client0,client1 \n")
    for i in range(1, 601):
        file.write(f"{str(datetime.now())},'{i}','{600 - i}'\n")

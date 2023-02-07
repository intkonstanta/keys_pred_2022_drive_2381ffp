import os
import pathlib
import json
path_to_rasp = f"C:\\Users\\intkonstanta\\all_projects\\pred_drive\\rasp"
base_dir = os.listdir(path_to_rasp)
for file_name in base_dir:
    path = pathlib.Path(path_to_rasp, file_name)
    print(path)
    try:
        with open(path, "r") as file:
            for line in file.readlines():
                dict = json.loads(line)
                print(dict["time"])
    except Exception:
        pass



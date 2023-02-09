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
            all_lines = file.readlines()
            comp_info = all_lines[0]
            print(f"info comp: {json.loads(comp_info)}")
            print("telemetry:")
            for i in range(1, len(all_lines) + 1):
                line = all_lines[i]
                dict = json.loads(line)
                print(dict)
    except Exception:
        pass



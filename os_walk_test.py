import os
all_mode = ["Run", "Attack", "Hit", "Dead"]
mode2index = {"Run":0, "Attack":1, "Hit":2, "Dead":3}
surfaces = [[],[],[],[]]
for i, mode in enumerate(all_mode):
    project_dir = f"image/enemy/Crabby/{mode}"
    file_count = 0
    for folder, subfolders, filenames in os.walk(project_dir):
        for filename in filenames:
            if filename.endswith(".png"):
                file_count += 1

    for j in range(file_count):
        surfaces[i].append(os.path.join(project_dir, str(j+1), str(".png")))

    # surfaces[i].reverse()

print(surfaces)
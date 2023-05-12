import cv2 , os

all_mode = ["Run", "Attack", "Hit", "Dead"]
characterSide = "enemy"
all_enemies = ["Crabby", "Fierce Tooth", "Pink Star", "Seashell", "Whale"]
for enemy in all_enemies:
    for i, mode in enumerate(all_mode):
        project_dir = f"test_image/{characterSide}/{enemy}/{mode}"
        file_count = 0
        for folder, _, filenames in os.walk(project_dir):
            for filename in filenames:
                if filename.endswith(".png"):
                    file_count += 1
        # self.surfaces[mode] = [pygame.image.load(f'{project_dir}/{j + 1}.png').convert_alpha() for j in range(file_count)]
        for j in range(file_count):
            path = f'{project_dir}/{j + 1}.png'
            print(path)
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            height, width, channels = img.shape
            print(img.shape)
            if(height/width >= 115/140):
                new_height = 115
                new_width = int(width * (115/height))
            else:
                new_width = 140
                new_height = int(width * (140/width))
            img = cv2.resize(img, (new_width, new_height),interpolation=cv2.INTER_NEAREST)
            # cv2.imshow("imshow", img)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            save_path = f'new_img/{characterSide}/{enemy}/{mode}/{j+1}.png'
            cv2.imwrite(save_path, img)


coordinate = [[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]

heroesInfo = {"dog": {"hp": 100, "damage": 100, "fps": 100, "speed_x": 7, "speed_y": 0, "cardCD": 500},
              "cat": {"hp": 500, "damage": 100, "fps": 200, "cardCD": 100},
              "mushroom": {"hp": 1000, "damage": 100, "fps": 200, "cardCD": 1000},
              "bee": {"hp": 100, "damage": 100, "fps": 100, "speed_x": 5, "speed_y": (-5, 0, 5), "cardCD": 100},
              "rino": {"hp": float('inf'), "damage": 100, "fps": 10, "cardCD": 1000},
              "bird": {"hp": 100, "damage": 100, "fps": 100, "speed_x": 7, "speed_y": 0, "cardCD": 500},
              "frog": {"hp": 100, "damage": 100, "fps": 100, "speed_x": 8, "speed_y": 0, "cardCD": 500},
              "fox": {"hp": 500, "damage": 100, "fps": 100, "cardCD": 100},
              "turtle": {"hp": 100, "damage": 100, "fps": 100, "cardCD": 100},
              "turkey": {"hp": float('inf'), "damage": 100, "fps": 10, "cardCD": 300}
              }

enemiesInfo = {"Crabby":{"hp":200, "damage":5, "fps":90, "speed":-5, "attack_fps":1000, "attack_moving_speed":-5},
             "Fierce Tooth":{"hp":200, "damage":10, "fps":90, "speed":-7, "attack_fps":1000, "attack_moving_speed":-5},
             "Pink Star":{"hp":30, "damage":5, "fps":90, "speed":-5, "attack_fps":1000, "attack_moving_speed":-30},
             "Seashell": {"hp":200, "damage":30, "fps":90, "speed":-1, "attack_fps":1000, "attack_moving_speed":-5},
             "Whale":{"hp":200, "damage":5, "fps":90, "speed":-2, "attack_fps":2000, "attack_moving_speed":-7}}
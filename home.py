level = 1
game_state = "main"
use_mouse = True

if __name__ == "__main__":
    while True:
        if game_state == "main":
            from main import main
            game_state, use_mouse = main(game_state, level)
        if game_state == "game_over":
            from game_over import game_over
            game_state = game_over(use_mouse=use_mouse)
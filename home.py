user = "test_level1"
level = 1

game_state = "main"
use_mouse = True

if __name__ == "__main__":
    while True:
        if game_state == "main":
            from main import main
            game_state, use_mouse = main(game_state, user, level)
        if game_state == "game_over_lose":
            from game_over import lose
            game_state = lose(use_mouse=use_mouse)
        if game_state == "game_over_win":
            from game_over import win
            game_state = win(use_mouse=use_mouse, level=level, user=user)
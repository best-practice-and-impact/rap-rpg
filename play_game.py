from rap_rpg import game

if __name__ == "__main__":
    try:
        g = game.Game("base_game", "hi", "bye")
        g.start_game()
    except KeyboardInterrupt:
        print("\n\nThank you for playing!")

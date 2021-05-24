from domain.game_play.mock_interface import MockGameProvider


def play_game():
    game_provider = MockGameProvider()
    game = game_provider.get_game()
    show_introduction(game)
    next_inject = game.first_inject
    while next_inject:
        show_next_inject(next_inject)
        print("Please input the number that corresponds to your choice.")
        print("Write 'stats' to see your current stats.")
        print("Write 'q' to quit the game.")
        next_inject = handle_input(game, inject=next_inject)
    handle_end(game)


def show_introduction(game):
    print("Now playing " + game.name)


def show_next_inject(inject):
    print(inject.label)
    print(inject.text)

    if inject.transitions:
        for i in range(0, len(inject.transitions)):
            print(str(i) + ": " + inject.transitions[i].label)
    else:
        print("0: Continue")


def handle_input(game, inject):
    answer = input()
    if answer == "stats":
        handle_stats(game)
        return inject.id
    elif answer == "q":
        exit()
    elif answer.isnumeric():
        return game.solve_inject(inject=inject, solution=int(answer))
    else:
        exit()
    print()
    return answer


def handle_stats(game):
    stats = game.variables
    visible_stats = game.get_visible_stats()
    print("## Visible stats ##")
    for var_name in visible_stats:
        print(str(var_name.name) + ": " + str(game.variables[var_name]))


def handle_end(game):
    game.end_game()
    print("You have finished the game. Thank you for playing!")


if __name__ == "__main__":
    play_game()

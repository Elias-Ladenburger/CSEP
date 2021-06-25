from domain.game_play.mock_interface import MockGameProvider


class MockPlayer:
    def __init__(self):
        game_provider = MockGameProvider()
        self._game = game_provider.get_branching_game()

    def play_game(self):
        self._show_introduction()
        next_inject = self._game.start_game()
        while next_inject:
            inject_slug = next_inject.slug
            self._show_next_inject(inject_slug)
            print("Please input the number that corresponds to your choice.")
            print("Write 'stats' to see your current stats.")
            print("Write 'q' to quit the game.")
            next_inject = self._handle_input(inject_slug=inject_slug)
        self._handle_end()

    def _show_introduction(self,):
        print("Now playing " + self._game.name)

    def _show_next_inject(self, inject_slug):
        inject = self._game.get_inject_by_slug(inject_slug)

        if not inject:
            exit()

        print(inject.label)
        print(inject.text)

        if inject.transitions:
            for i in range(0, len(inject.transitions)):
                print(str(i) + ": " + inject.transitions[i].label)
        else:
            print("0: Continue")

    def _handle_input(self, inject_slug):
        answer = input()
        if answer == "stats":
            self._handle_stats()
            return inject_slug
        elif answer == "q":
            exit()
        elif answer.isnumeric():
            return self._game.solve_inject(inject=inject_slug, solution=int(answer))
        else:
            exit()
        print()
        return answer

    def _handle_stats(self):
        visible_stats = self._game.get_visible_vars()
        print("## Visible stats ##")
        for var_name in visible_stats:
            print(str(var_name.name) + ": " + str(self._game._variables[var_name]))

    def _handle_end(self):
        self._game.end_game()
        print("You have finished the game. Thank you for playing!")


if __name__ == "__main__":
    player = MockPlayer()
    player.play_game()

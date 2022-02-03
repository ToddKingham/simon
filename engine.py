from random import randrange


class Simon:
    def __init__(self, num_of_buttons, simon_cb, player_cb, gameover_cb):
        self.num_of_buttons = num_of_buttons
        self.simon_callback = simon_cb
        self.player_callback = player_cb
        self.gameover_callback = gameover_cb
        self.test_mode = None
        self.num_of_rounds = None
        self.game_sequence = []
        self.player_error = None
        self.last_game = None
        self.longest_game = []

    def _next_button(self):
        if self.test_mode:
            return len(self.game_sequence) % self.num_of_buttons
        else:
            return randrange(0, self.num_of_buttons)

    def _simons_turn(self):
        self.game_sequence.append(self._next_button())
        self.simon_callback(self.game_sequence.copy())

    def _player_turn(self):
        for correct_choice in self.game_sequence:
            players_choice = self.player_callback(correct_choice)
            if players_choice != correct_choice:
                self.player_error = True
                break

    def _game_over(self):
        # copy the current game to the last game
        self.last_game = self.game_sequence.copy()
        if self.player_error:
            self.last_game.pop(-1)

        if len(self.last_game) >= len(self.longest_game):
            self.longest_game = self.last_game.copy()
        self.gameover_callback(not self.player_error)

    def _continue(self):
        return (len(self.game_sequence) < self.num_of_rounds) and (not self.player_error)

    def start_game(self, num_of_rounds=20, test_mode=False):
        self.test_mode = test_mode
        self.num_of_rounds = num_of_rounds
        self.game_sequence = []
        self.player_error = False

        while self._continue():
            self._simons_turn()
            self._player_turn()
        self._game_over()

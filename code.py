import keypad
import simpleio
from time import sleep, time as now
from constants import TEST_MODE, NUM_OF_ROUNDS, TICK, TIMEOUT, BUTTONS, START_BUTTON, SPEAKER
from engine import Simon
from hardware import Hardware
from helpers import has_expired


class Game:
    def __init__(self):
        self.is_game_active = False
        self.leds = tuple([Hardware.led(x['led']) for x in BUTTONS])
        self.switches = tuple([x['switch'] for x in BUTTONS])
        self.tones = tuple([x['tone'] for x in BUTTONS])
        self.start_button = Hardware.switch(START_BUTTON)
        self.correct_pin = None
        self.simon = Simon(len(self.leds), self.on_computer_turn, self.on_player_turn, self.on_game_end)
        self.on_bootup()

    def on_bootup(self):
        def x(_): _.value = not _.value
        list(map(x, self.leds))
        sleep(1)
        list(map(x, self.leds))

    def on_computer_turn(self, seq):
        sleep(TICK * 4)
        for i in seq:
            self.ping_led(i)
            sleep(TICK)

    def on_player_turn(self, correct=None):
        self.correct_pin = correct
        with keypad.Keys(
                self.switches,
                value_when_pressed=False,
                pull=True
        ) as keys:
            tick = now()
            choice = -1
            while True:
                # TIMEOUT LOGIC
                if has_expired(tick, TIMEOUT):
                    self.on_error()
                    return -1

                # KEY PRESS LISTENERS
                key_event = keys.events.get()
                if key_event:
                    # on press
                    if key_event.pressed:
                        choice = key_event.key_number
                        # correct choice
                        if choice == self.correct_pin:
                            self.ping_led(choice)
                        # incorrect choice
                        else:
                            self.on_error()
                    # on release
                    else:
                        return choice

    def ping_led(self, pin, error=False, t=TICK):
        led = self.leds[pin]
        if error:
            sound = SPEAKER['error_tone']
        else:
            sound = self.tones[pin]

        led.value = True
        simpleio.tone(SPEAKER['pin'], sound, t)
        led.value = False

    def on_error(self):
        self.ping_led(self.correct_pin, True, TICK * 5)

    def on_game_end(self, win):
        self.is_game_active = False
        if win:
            sleep(TICK)
            for x in range(0, len(self.leds)*8):
                self.ping_led(x % len(self.leds), t=TICK/5)

        print('LAST GAME', self.simon.last_game)
        print('LONGEST GAME', self.simon.longest_game)

    def wait_for_start(self):
        if not self.start_button.value and self.is_game_active is False:
            self.is_game_active = True

    def in_game_loop(self):
        if self.is_game_active:
            self.simon.start_game(NUM_OF_ROUNDS, TEST_MODE)


game = Game()

while True:
    game.wait_for_start()
    game.in_game_loop()

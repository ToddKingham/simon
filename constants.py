from board import SDA, SCL, D5, D6, D9, D10, D11, D12, D24, D25

TEST_MODE = False
NUM_OF_ROUNDS = 20
TICK = 0.25
TIMEOUT = 5
START_BUTTON = D24
SPEAKER = {"pin": D25, "error_tone": 100.0}
BUTTONS = (
    {"led": SDA, "switch": SCL, "tone": 1046.5},
    {"led": D5, "switch": D6, "tone": 1318.5},
    {"led": D9, "switch": D10, "tone": 1568.0},
    {"led": D11, "switch": D12, "tone": 1979.5}
)
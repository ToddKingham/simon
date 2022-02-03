import board
from digitalio import DigitalInOut, Pull, Direction


class Hardware:
    @staticmethod
    def pin(p):
        return getattr(board, p)

    @staticmethod
    def led(p):
        ld = DigitalInOut(Hardware.pin(p))
        ld.switch_to_output()
        return ld

    @staticmethod
    def switch(p):
        sw = DigitalInOut(Hardware.pin(p))
        sw.direction = Direction.INPUT
        sw.pull = Pull.UP
        return sw

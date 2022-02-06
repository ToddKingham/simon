from digitalio import DigitalInOut, Pull, Direction


class Hardware:
    @staticmethod
    def led(pin):
        ld = DigitalInOut(pin)
        ld.switch_to_output()
        return ld

    @staticmethod
    def switch(pin):
        sw = DigitalInOut(pin)
        sw.direction = Direction.INPUT
        sw.pull = Pull.UP
        return sw

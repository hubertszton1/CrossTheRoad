import test
from gpiozero import Button
from signal import pause

up_btn = Button(23)
down_btn = Button(17)
left_btn = Button(22)
right_btn = Button(27)


def up_pressed():
    return True
def down_pressed():
    print("DÃ“Å")
def left_pressed():
    print("LEWO")
def right_pressed():
    print("PRAWO")

up_btn.when_pressed = up_pressed
down_btn.when_pressed = down_pressed
left_btn.when_pressed = left_pressed
right_btn.when_pressed = right_pressed

pause()

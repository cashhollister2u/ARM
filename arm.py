import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import curses


kit = MotorKit(i2c=board.I2C())

# 200 steps is 360 degrees

def main(stdscr):
    # Clear screen
    stdscr.clear()
    stdscr.addstr(0, 0, "Use arrow keys to control the motor. Press 'q' to quit.")
    stdscr.refresh()

    # home
    position = 0

    # regulate smoothness of motor
    step_size = 7
    current_step = 0

    while True:
        key = stdscr.getch()

        if key == ord('q'):
            break

        # rotate left 
        elif key == curses.KEY_LEFT and position >= 0:
            while current_step <= step_size:
                time.sleep(0.01)
                position -= 1
                kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
                stdscr.addstr(1, 0, "Moving Left")
                current_step += 1
            current_step = 0 # reset step count

        # rotate right
        elif key == curses.KEY_RIGHT and position <= 150:
            while current_step <= step_size:
                time.sleep(0.01)
                position += 1
                kit.stepper1.onestep(style=stepper.DOUBLE)
                stdscr.addstr(1, 0, "Moving Right")
                current_step += 1
                
            current_step = 0 # reset step count

        stdscr.refresh()
        #time.sleep(0.01)

    # return home
    while position >= 0:
        position -= 1
        kit.stepper1.onestep(direction=stepper.BACKWARD)
        stdscr.addstr(1, 0, "resetting postion")
        time.sleep(0.01)

    # return home
    while position <= 0:
        position += 1
        kit.stepper1.onestep()
        stdscr.addstr(1, 0, "resetting postion")
        time.sleep(0.01)

    # cut power to motor
    kit.stepper1.release()
    stdscr.addstr(1, 0, "release motor")


# call main
if __name__ == "__main__":
    curses.wrapper(main)
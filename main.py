import time
from datetime import datetime
import pyautogui
import cv2
import numpy as np


def take_screenshot():
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


def is_red(screenshot):
    lower_red = np.array([0, 0, 200])
    upper_red = np.array([50, 50, 255])

    return cv2.inRange(screenshot, lower_red, upper_red).any()


def get_energy_level(screenshot):
    energy_level = crop_image(screenshot, (1876, 890), (1898, 1053))

    log_screenshot(f"energy_level_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png", energy_level)

    return energy_level


def get_time_of_day(screenshot):
    time_of_day = crop_image(screenshot, (1729, 122), (1885, 164))

    log_screenshot(f"time_of_day_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png", time_of_day)

    return time_of_day


def crop_image(screenshot, starting_position, ending_position):
    x, y = starting_position

    width = ending_position[0] - starting_position[0]
    height = ending_position[1] - starting_position[1]

    return screenshot[y:y + height, x:x + width]


def log_screenshot(filename, screenshot):
    cv2.imwrite(filename, screenshot)


def check_status():
    screenshot = take_screenshot()

    energy_level = get_energy_level(screenshot)
    time_of_day = get_time_of_day(screenshot)

    if not (is_red(energy_level) and is_red(time_of_day)):
        print("enough energy and time.")
        return True
    else:
        print(f"low energy or not enough time. Is energy enough: {is_red(energy_level)} is time enough: {is_red(time_of_day)}")
        return False


def main():
    while True:
        time.sleep(5)
        check_status()


if __name__ == "__main__":
    main()
import time
from datetime import datetime
import pyautogui
import cv2
import numpy as np


def take_screenshot():
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


def is_energy_low(energy_level):
    lower_red = np.array([0, 0, 200])
    upper_red = np.array([50, 50, 255])

    return cv2.inRange(energy_level, lower_red, upper_red).any()


def get_energy_level(screenshot):
    # Energy bar position
    start_point = (1876, 890)
    end_point = (1898, 1053)

    x, y = start_point
    width = end_point[0] - start_point[0]
    height = end_point[1] - start_point[1]

    energy_level = screenshot[y:y + height, x:x + width]

    cv2.imwrite(f"energy_level_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png", energy_level)

    return energy_level


def get_time_of_day(screenshot):
    time_of_day = crop_image(screenshot, (1729, 122), (1883, 153))

    cv2.imwrite(f"time_of_day_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png", time_of_day)

    return time_of_day


def crop_image(screenshot, starting_position, ending_position):
    x, y = starting_position

    width = ending_position[0] - starting_position[0]
    height = ending_position[1] - starting_position[1]

    return screenshot[y:y + height, x:x + width]


def main():
    screenshot = take_screenshot()

    energy_level = get_energy_level(screenshot)
    time_of_day = get_time_of_day(screenshot)

    if is_energy_low(energy_level):
        print("The specified region is red.")
    else:
        print("The specified region is not red.")


if __name__ == "__main__":
    time.sleep(5)
    main()
    while True:
        time.sleep(5)
        print(pyautogui.position())

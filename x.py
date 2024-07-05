import pyautogui
import keyboard

while True:
    keyboard.wait('h')
    pyautogui.moveTo(788, 479, 0.5)
    print(pyautogui.pixel(1854, 321))
    print(pyautogui.position())
    print(pyautogui.pixel(pyautogui.position().x, pyautogui.position().y))
import keyboard
import pyautogui as pg


def printer():        
    keyboard.wait('h')
    x, y = pg.position()
    photo = pg.screenshot(region=(x - 5, y - 5, 10, 10))
    photo.save('newFlag.png')

while True:    
    printer()

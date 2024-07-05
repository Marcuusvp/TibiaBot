import pyautogui as pg
import keyboard
import constants
import random

pg.useImageNotFoundException(False)

# keyboard.wait('h')
#print(pg.locateOnScreen('imgs/battle2.png', confidence=0.8))
# print(pg.pixel(x=1582, y=38))

def check_battle():
    return pg.locateOnScreen('imgs/battle.png', confidence=0.8, region=constants.REGION_BATTLE)

def kill_monster():
    while check_battle() == None:
        pg.press('space')
        if pg.pixel(x=1582, y=38) == (254, 0, 0) or pg.pixel(x=1582, y=38) == (255, 0, 0):
            while pg.pixel(x=1582, y=38) == (254, 0, 0) or pg.pixel(x=1582, y=38) == (255, 0, 0):
                pg.sleep(1)
                print('Atacando target')     
        print('procurando targets')
        

def get_loot():
    random.shuffle(constants.LIST_POSITION_LOOT)
    pg.PAUSE = 0.09
    for position in constants.LIST_POSITION_LOOT:
        pg.moveTo(position)
        pg.click(button="right")
    pg.PAUSE = 0.1

def execute_hotkey(hotkey):
    pg.press(hotkey)

def hole_up():
    pg.moveTo(788, 479)
    print('Movi o mouse pro centro')
    pg.sleep(2)

    pg.press('F10')
    pg.click()
    print('apertei F10')

def ladder_up():
    pg.moveTo(788, 479)
    pg.click(button="right")

# def ladder_up(anchor):
#     box = pyautogui.locateOnScreen(anchor, confidence=0.8)
#     if box:
#         x, y = pyautogui.center(box)
#         pyautogui.moveTo(x , y, 0.5)
#         pyautogui.click(button="right")

# def hole_up(anchor):
#     box = pyautogui.locateOnScreen(anchor, confidence=0.8)
#     if box:
#         x, y = pyautogui.center(box)
#         pyautogui.moveTo(x , y, 0.5)
#         pyautogui.press('F10')
#         pyautogui.click()

def rotate_skills():
    while not event_rotate_skills.is_set():
        for attack in constants.LIST_HOTKEY_ATTACKS:
            if event_rotate_skills.is_set():
                return
            if pyautogui.locateOnScreen('battle.png', confidence=0.8, region=constants.REGION_BATTLE):
                continue
            print('Executando: ', attack['hotkey'])
            pyautogui.press('space')
            pyautogui.press(attack["hotkey"])
            pyautogui.sleep(attack["delay"])

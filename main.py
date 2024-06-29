import pynput
import pyautogui
import threading
import random

from vida_mana import manager_suplies

pyautogui.useImageNotFoundException(False)

FULL_DEFENSIVE_HOTKEY = '-'
FULL_OFFENSIVE_HOTKEY = '='
USE_RING = 'F10'
list_hotkey_before = [FULL_OFFENSIVE_HOTKEY, USE_RING]
list_hotkey_after = [FULL_DEFENSIVE_HOTKEY, USE_RING]
EAT_FOOD_HOTKEY = 'F12'
LIST_POSITION_LOOT = [(706, 414), (780, 408), (841, 407), (849, 476), (849, 539), (779, 541), (720, 539), (716, 461)]
LIST_HOTKEY_ATTACKS = [{"hotkey":'F4', "delay": 6}]
LIST_HOTKEY_ATTACKS_EXEMPLO = [{"hotkey":'F4', "delay": 0.5}, {"hotkey":'F5', "delay": 2}, {"hotkey":'F6', "delay": 2}]
REGION_BATTLE = (1573, 25, 155, 37)

def rotate_skills():
    while not event_rotate_skills.is_set():
        for attack in LIST_HOTKEY_ATTACKS:
            if event_rotate_skills.is_set():
                return
            if pyautogui.locateOnScreen('battle.png', confidence=0.8, region=REGION_BATTLE):
                continue
            print('Executando: ', attack['hotkey'])
            pyautogui.press('space')
            pyautogui.press(attack["hotkey"])
            pyautogui.sleep(attack["delay"])


def execute_hotkey(hotkey):
    pyautogui.press(hotkey)

def get_loot():
    random.shuffle(LIST_POSITION_LOOT)
    pyautogui.PAUSE = 0.04
    for position in LIST_POSITION_LOOT:
        pyautogui.moveTo(position)
        pyautogui.click(button="right")
    pyautogui.PAUSE = 0.1


running = False
def key_code(key):
    global running
    if key == pynput.keyboard.Key.delete:
        print('Bot encerrado!')
        return False
    if hasattr(key, 'char') and key.char == 'f':
        if running == False:
            running = True
            global th_rotate_skills, event_rotate_skills, th_suplies, event_suplies
            event_suplies = threading.Event()
            th_suplies = threading.Thread(target=manager_suplies, args=(event_suplies, ))
            event_rotate_skills = threading.Event()
            th_rotate_skills = threading.Thread(target=rotate_skills)
            print('Iniciando a rotacção de skills')
            for hotkey in list_hotkey_before:
                execute_hotkey(hotkey)
            th_rotate_skills.start()
            th_suplies.start()
        else:
            running = False
            event_rotate_skills.set()
            event_suplies.set()
            th_rotate_skills.join()
            th_suplies.join()
            print('Parando rotação de skills')
            for hotkey in list_hotkey_after:
                execute_hotkey(hotkey)

    if hasattr(key, 'char') and key.char == 'r':
        print('Coletando loot')
        get_loot()
        execute_hotkey(EAT_FOOD_HOTKEY)
    
with pynput.keyboard.Listener(on_press=key_code) as listener:
    listener.join()
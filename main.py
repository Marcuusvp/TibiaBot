import pyautogui
import threading
import json
import constants
import actions
import signal
import sys
from pynput.keyboard import Controller as KeyboardController, GlobalHotKeys
from pynput.mouse import Controller as MouseController, Button
from vida_mana import manage_supplies
from auto_attack_thread import start_monitoring

# Inicializando controlador de teclado e mouse
keyboard_controller = KeyboardController()
mouse = MouseController()

pyautogui.useImageNotFoundException(False)

list_hotkey_before = [constants.FULL_OFFENSIVE_HOTKEY, constants.USE_RING]
list_hotkey_after = [constants.FULL_DEFENSIVE_HOTKEY, constants.USE_RING]
running = False
stop_event = threading.Event()
bot_running = False

def press_key(key):
    keyboard_controller.press(key)
    keyboard_controller.release(key)

def check_player_position(path):
    player_image = pyautogui.locateOnScreen(path, confidence=0.8, region=constants.REGION_MAP)
    if player_image:
        x, y = pyautogui.center(player_image)
        region_center_x = constants.REGION_MAP[0] + constants.REGION_MAP[2] // 2
        region_center_y = constants.REGION_MAP[1] + constants.REGION_MAP[3] // 2
        return abs(x - region_center_x) <= 2 and abs(y - region_center_y) <= 2
    return False

def go_to_flag(item):
    print(f"próximo endpoint ->: {item['path']}.")
    flag = pyautogui.locateOnScreen(item['path'], confidence=0.8, region=constants.REGION_MAP)

    if flag is None:
        return None
    
    if flag:
        x, y = pyautogui.center(flag)
        mouse.position = (x, y)
        mouse.click(Button.left, 1)
        print(f"localizei e cliquei no endpoint ->: {item['path']}.")      
        mouse.position = (788, 479)
        pyautogui.sleep(item['wait'])
        
        if check_player_position(item['path']):            
            return True
    return False

def perform_action(item):
    pyautogui.sleep(1)
    if item['zoom_in'] > 0:
        actions.zoom_in(item['zoom_in'])
        pyautogui.sleep(2)
        
    if item['zoom_out'] > 0:
        actions.zoom_out(item['zoom_out'])
        pyautogui.sleep(2)
    
    if item['up_hole'] > 0:
        actions.hole_up()
        pyautogui.sleep(3)

    if item['up_ladder'] > 0:
        actions.ladder_up()
        pyautogui.sleep(2)

    if item['up_ladder_ne'] > 0:
        actions.ladder_up_ne()
        pyautogui.sleep(2)
    
    if item['up_ladder_nw'] > 0:
        actions.ladder_up_nw()
        pyautogui.sleep(2)
    
    if item['down_hole'] > 0:
        actions.down_hole()
        pyautogui.sleep(2)

def fallback_action():
    press_key('w')
    pyautogui.sleep(1)
    mouse.position = (788, 479)
    press_key('f9')
    mouse.click(Button.left, 1)
    pyautogui.sleep(2)

def check_flag_position(path):
    flag = pyautogui.locateOnScreen(path, confidence=0.8, region=constants.REGION_MAP)
    if flag:
        x, y = pyautogui.center(flag)
        region_center_x = constants.REGION_MAP[0] + constants.REGION_MAP[2] // 2
        region_center_y = constants.REGION_MAP[1] + constants.REGION_MAP[3] // 2
        return abs(x - region_center_x) < 2 and abs(y - region_center_y) < 2
    return False

def run():
    global running, event_rotate_skills, th_rotate_skills, event_suplies, th_suplies, event_battle, th_battle, event_loot, th_loot, bot_running
    bot_running = True
    print("Bot iniciou...")
    with open(f'{constants.FOLDER_NAME}/infos.json', 'r') as file:
        data = json.loads(file.read())

    # Inicia a thread de monitoramento de vida e mana
    event_suplies = threading.Event()
    th_suplies = threading.Thread(target=manage_supplies, args=(event_suplies,))
    th_suplies.daemon = True
    th_suplies.start()

    i = 0
    while not stop_event.is_set() and i < len(data):
        item = data[i]

        actions.execute_hotkey(constants.EAT_FOOD_HOTKEY)
        if actions.check_ring():
            actions.execute_hotkey(constants.USE_RING)
        
        if actions.check_auto_chase():
            actions.execute_hotkey(constants.CHASE_TARGET_HOTKEY)
        
        actions.descartar_itens()

        flag = go_to_flag(item)

        while flag is None and i > 0 and not stop_event.is_set():
            previous_flag = data[i - 1]
            print(f"não encontrei a flag: {item['path']}, voltando para a anterior: {previous_flag['path']}")
            flag = go_to_flag(previous_flag)
            if flag is not None:
                item = previous_flag
                i -= 1
                break
            # else:
            #     i -= 1

        while flag == False and not stop_event.is_set():
            print(f"não cheguei no endpoint que queria, tentando de novo: {item['path']}.")

            event_battle, done_battle, th_battle = start_monitoring()
            while not done_battle.is_set() and not stop_event.is_set():
                pass
            th_battle.join()
            
            flag = go_to_flag(item)

        
        perform_action(item)
        if actions.check_auto_chase():
            actions.execute_hotkey(constants.CHASE_TARGET_HOTKEY)
        event_battle, done_battle, th_battle = start_monitoring()
        while not done_battle.is_set() and not stop_event.is_set():
            pass
        th_battle.join()

        i += 1
        if i >= len(data):
            i = 0  # Reset to the first flag

    # Para a thread de monitoramento de vida e mana
    event_suplies.set()
    th_suplies.join()
    bot_running = False
    print("Bot parado.")

def stop_bot():
    global stop_event, bot_running
    if bot_running:
        print("Bot parando...")
        stop_event.set()

def start_bot():
    global stop_event
    if not bot_running:
        stop_event = threading.Event()
        threading.Thread(target=run).start()

def signal_handler(sig, frame):
    print("Encerrando a aplicação...")
    stop_bot()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

hotkeys = {
    'p': stop_bot,
    '<ctrl>+h': start_bot
}

with GlobalHotKeys(hotkeys) as h:
    h.join()

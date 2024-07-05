import pyautogui
import threading
import keyboard
import constants
import json


from vida_mana import manage_supplies
from auto_attack_thread import start_monitoring
from auto_loot_thread import start_autoLoot

pyautogui.useImageNotFoundException(False)

list_hotkey_before = [constants.FULL_OFFENSIVE_HOTKEY, constants.USE_RING]
list_hotkey_after = [constants.FULL_DEFENSIVE_HOTKEY, constants.USE_RING]
running = False
stop_event = threading.Event()

def check_player_position():
    return pyautogui.locateOnScreen('imgs/point_player.png', confidence=0.8, region=constants.REGION_MAP)

def go_to_flag(path, wait):
    flag = pyautogui.locateOnScreen(path, confidence=0.8, region=constants.REGION_MAP)
    if flag:
        x, y = pyautogui.center(flag)
        pyautogui.moveTo(x, y, 0.5)
        pyautogui.click()
        pyautogui.sleep(wait)
        return True
    else:
        return False

def fallback_action():
    print("Realizando ação alternativa...")
    pyautogui.press('w')
    pyautogui.sleep(1)
    pyautogui.moveTo(788, 479, 0.5)
    pyautogui.press('f9')
    pyautogui.click()
    pyautogui.sleep(2)

def check_flag_position(path):
    flag = pyautogui.locateOnScreen(path, confidence=0.8, region=constants.REGION_MAP)
    if flag:
        x, y = pyautogui.center(flag)
        region_center_x = constants.REGION_MAP[0] + constants.REGION_MAP[2] // 2
        region_center_y = constants.REGION_MAP[1] + constants.REGION_MAP[3] // 2
        return abs(x - region_center_x) < 2 and abs(y - region_center_y) < 2  # 10 pixels de tolerância
    return False

def run():
    global running, event_rotate_skills, th_rotate_skills, event_suplies, th_suplies, event_battle, th_battle, event_loot, th_loot
    print("Bot iniciou...")
    with open(f'{constants.FOLDER_NAME}/infos.json', 'r') as file:
        data = json.loads(file.read())

    # Inicia a thread de monitoramento de vida e mana
    event_suplies = threading.Event()
    th_suplies = threading.Thread(target=manage_supplies, args=(event_suplies,))
    th_suplies.daemon = True
    th_suplies.start()

    while not stop_event.is_set():
        for i, item in enumerate(data):
            if stop_event.is_set():
                break

            constants.execute_hotkey(constants.EAT_FOOD_HOTKEY)

            success = go_to_flag(item['path'], item['wait'])
            if not success:
                if i > 0:
                    previous_flag = data[i - 1]['path']
                    print(f"Bandeira não encontrada. Tentando bandeira anterior: {previous_flag}")
                    success = go_to_flag(previous_flag, item['wait'])
                if not success and i < len(data) - 1:
                    next_flag = data[i + 1]['path']
                    print(f"Bandeira anterior não encontrada. Tentando próxima bandeira: {next_flag}")
                    success = go_to_flag(next_flag, item['wait'])
                if not success:
                    fallback_action()

            print(f"Fui para o endpoint ->: {item['path']}.")

            # Inicia a thread de batalha
            event_battle, done_battle, th_battle = start_monitoring()
            print(f"Entrei em modo de porradaria")
            while not done_battle.is_set() and not stop_event.is_set():
                pass
            th_battle.join()

            # Inicia a thread de loot
            # event_loot, done_loot, th_loot = start_autoLoot(['imgs/dead_troll.png'])
            # while not done_loot.is_set() and not stop_event.is_set():
            #     pass
            # th_loot.join()
            print(f"buscando loot...")

            if check_player_position():
                print(f"não cheguei no endpoint que queria, tentando de novo: {item['path']}. Iniciando ataque.")
                event_battle, done_battle, th_battle = start_monitoring()
                print(f"Entrei em modo de porradaria DE NOVO")
                while not done_battle.is_set() and not stop_event.is_set():
                    pass
                th_battle.join()
                # event_loot, done_loot, th_loot = start_autoLoot('imgs/dead_troll.png')
                # while not done_loot.is_set() and not stop_event.is_set():
                #     pass
                # th_loot.join()
                # print(f"buscando loot de novo...")
                go_to_flag(item['path'], item['wait'])
            
            print('pre checagem if up_hole')
            print(item['up_hole'])
            if item['up_hole'] == 1:
                print('Entrei no up_hole')
                # while not check_flag_position(item['path']):
                #     go_to_flag(item['path'], item['wait'])
                constants.hole_up()
                pyautogui.sleep(5)
                # hole_up('imgs/anchor.png')
            if item['up_ladder'] == 1:
                # while not check_flag_position(item['path']):
                #     go_to_flag(item['path'], item['wait'])
                constants.ladder_up()
                pyautogui.sleep(5)
                # ladder_up('imgs/escada_dir.png')

    # Para a thread de monitoramento de vida e mana
    event_suplies.set()
    th_suplies.join()

def stop_bot():
    print("Bot parando...")
    stop_event.set()

keyboard.add_hotkey('p', stop_bot)

keyboard.wait('h')
run()
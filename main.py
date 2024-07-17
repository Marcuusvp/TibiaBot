import pyautogui
import threading
import keyboard
import constants
import json
import actions

from vida_mana import manage_supplies
from auto_attack_thread import start_monitoring

pyautogui.useImageNotFoundException(False)

list_hotkey_before = [constants.FULL_OFFENSIVE_HOTKEY, constants.USE_RING]
list_hotkey_after = [constants.FULL_DEFENSIVE_HOTKEY, constants.USE_RING]
running = False
stop_event = threading.Event()

def check_player_position(path):
    # Localiza a imagem na região especificada
    player_image = pyautogui.locateOnScreen(path, confidence=0.8, region=constants.REGION_MAP)
    if player_image:
        # Obtém as coordenadas do centro da imagem localizada
        x, y = pyautogui.center(player_image)
        region_center_x = constants.REGION_MAP[0] + constants.REGION_MAP[2] // 2
        region_center_y = constants.REGION_MAP[1] + constants.REGION_MAP[3] // 2
        return abs(x - region_center_x) <= 2 and abs(y - region_center_y) <= 2
    return False

def go_to_flag(item):
    print(f"próximo endpoint ->: {item['path']}.")
    flag = pyautogui.locateOnScreen(item['path'], confidence=0.8, region=constants.REGION_MAP)
    if flag:
        x, y = pyautogui.center(flag)
        pyautogui.moveTo(x, y, 0.5)
        pyautogui.click()  
        print(f"localizei e cliquei no endpoint ->: {item['path']}.")      
        pyautogui.moveTo(788, 479)
        pyautogui.sleep(item['wait'])
        
        if check_player_position(item['path']):            
            return True
    return False

def perform_action(item):
        pyautogui.sleep(1)
        """Realiza a ação associada à bandeira."""
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
    # print("Realizando ação alternativa...")
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

            actions.execute_hotkey(constants.EAT_FOOD_HOTKEY)
            if actions.check_ring():
                # print('entrei no if ring')
                actions.execute_hotkey(constants.USE_RING)
            
            if actions.check_auto_chase():
                actions.execute_hotkey(constants.CHASE_TARGET_HOTKEY)
            
            actions.descartar_itens()

            go_to_flag(item)

            event_battle, done_battle, th_battle = start_monitoring()
                # print(f"Entrei em modo de porradaria DE NOVO")
            while not done_battle.is_set() and not stop_event.is_set():
                pass
            th_battle.join()

            while go_to_flag(item) == False:
                print(f"não cheguei no endpoint que queria, tentando de novo: {item['path']}.")
                go_to_flag(item)

                event_battle, done_battle, th_battle = start_monitoring()
                # print(f"Entrei em modo de porradaria DE NOVO")
                while not done_battle.is_set() and not stop_event.is_set():
                    pass
                th_battle.join()
            
            perform_action(item)
            # Inicia a thread de batalha
            event_battle, done_battle, th_battle = start_monitoring()
            # print(f"Entrei em modo de porradaria")
            while not done_battle.is_set() and not stop_event.is_set():
                pass
            th_battle.join()

    # Para a thread de monitoramento de vida e mana
    event_suplies.set()
    th_suplies.join()

def stop_bot():
    print("Bot parando...")
    stop_event.set()

keyboard.add_hotkey('p', stop_bot)

keyboard.wait('h')
run()
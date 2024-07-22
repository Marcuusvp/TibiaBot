import pyautogui as pg
import threading
import time
import keyboard
import constants
import logging
import actions


# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
pg.useImageNotFoundException(False)

# Definindo as regiões de batalha
BATTLE_REGIONS = [
    (1574, 39, 150, 19),
    (1574, 60, 151, 19),
    (1574, 82, 151, 19),
    (1574, 105, 151, 19),
    (1574, 126, 151, 19),
    (1574, 147, 151, 19)
]

def is_region_empty(region, result, index):
    screenshot = pg.screenshot(region=region)
    width, height = screenshot.size
    tolerance = 40  # Tolerância para a diferença entre valores RGB

    for x in range(width):
        for y in range(height):
            r, g, b = screenshot.getpixel((x, y))
            # Verifica se a diferença entre os valores RGB é maior que a tolerância
            if abs(r - g) > tolerance or abs(r - b) > tolerance or abs(g - b) > tolerance:
                print(f'Encontrei monstro na região: {region}')
                result[index] = actions.ignorar_monstro(region)
                return
    result[index] = True

def is_attacking():
    screenshot = pg.screenshot(region=constants.REGIAO_TARGET)
    width, height = screenshot.size
    tolerance = 20  # Tolerância para a cor de ataque vermelho
    attack_detected = False
    for x in range(width):
        for y in range(height):
            r, g, b = screenshot.getpixel((x, y))
            if abs(r - constants.RGB_ATTACK[0]) <= tolerance and \
               g == constants.RGB_ATTACK[1] and \
               b == constants.RGB_ATTACK[2]:
                attack_detected = True
                break
        if attack_detected:
            break
    return attack_detected

def monitor_and_click(stop_event, done_event):
    current_region = None
    count = 0
    inaccessible_regions = []  # Lista para armazenar regiões inacessíveis

    while not stop_event.is_set():
        if is_attacking():
            while is_attacking():                
                time.sleep(1)
                continue
            actions.get_loot()
            continue
        
        regions_with_monsters = []
        threads = []
        results = [None] * len(BATTLE_REGIONS)

        for index, region in enumerate(BATTLE_REGIONS):
            if region not in inaccessible_regions:
                thread = threading.Thread(target=is_region_empty, args=(region, results, index))
                threads.append(thread)
                thread.start()
        
        for thread in threads:
            thread.join()
        
        for index, region in enumerate(BATTLE_REGIONS):
            if not results[index]:
                regions_with_monsters.append(region)

        if regions_with_monsters:
            # Clica na última região onde há um monstro
            current_region = regions_with_monsters[0]
            center_x = current_region[0] + current_region[2] // 2
            center_y = current_region[1] + current_region[3] // 2
            pg.moveTo(center_x, center_y)
            pg.click()
            pg.moveTo(center_x + 100, center_y)

            # Verifica se estamos atacando e aguarda até que não estejamos mais
            while is_attacking():
                count += 1
                time.sleep(1)
                if count > 10:  # Lançar uma const aqui
                    center_x = current_region[0] + current_region[2] // 2
                    center_y = current_region[1] + current_region[3] // 2
                    pg.moveTo(center_x, center_y)
                    pg.click()
                    print(f'parei de atacar monstro inalcançavel na regiao: {current_region}')
                    inaccessible_regions.append(current_region)  # Adiciona a região à lista de inacessíveis
                    current_region = None
                    count = 0
                    break
            actions.get_loot()        
            count = 0  # Sai do loop interno ao remover a marcação

        else:
            current_region = None

        if len(regions_with_monsters) < 1:
            print('Não há mais monstros. Encerrando a thread...')
            break
    done_event.set()


def start_monitoring():
    stop_event = threading.Event()
    done_event = threading.Event()
    thread = threading.Thread(target=monitor_and_click, args=(stop_event, done_event))
    thread.daemon = True
    thread.start()
    return stop_event, done_event, thread

if __name__ == "__main__":
    stop_event, done_event, thread = start_monitoring()

    # Exemplo de controle de execução
    try:
        while not done_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        thread.join()

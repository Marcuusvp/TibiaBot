import pyautogui
import keyboard
import threading
import time
import logging

LIFE_REGION = (1766, 304, 92, 5)
MANA_REGION = (1766, 316, 92, 5)
LIFE_COLOR = (240, 97, 97) #MONITOR
MANA_COLOR = (83, 80, 217) #MONITOR
# LIFE_COLOR = (254, 112, 112) #NOTEBOOK
# MANA_COLOR = (101, 98, 239) #NOTEBOOK
MANA_FULL = (59, 79, 122)
#Point(x=1853, y=320)
WIDTH = 92

def calculate_width(percent):
    return int(WIDTH * percent / 100)

def pixel_matches_color(region, percent, color):
    result_percent = calculate_width(percent)
    x = region[0] + result_percent
    y = region[1] + region[3]
    return pyautogui.pixelMatchesColor(int(x), int(y), color, 10)

def manage_supplies(stop_event):
    while not stop_event.is_set():
        if not pixel_matches_color(LIFE_REGION, 30, LIFE_COLOR):
            pyautogui.press('F1')
            print(f"potei pq a vida ta baixa 30")
        if not pixel_matches_color(LIFE_REGION, 80, LIFE_COLOR):
            pyautogui.press('F3')
            print(f"curei pq a vida ta baixa 80")
        if not pixel_matches_color(MANA_REGION, 20, MANA_COLOR):
            pyautogui.press('F2')
            print(f"potei pq a mana ta baixa 20")
        # if pixel_matches_color(MANA_REGION, 90, MANA_COLOR):
        #     pyautogui.press('F3')
        #     print(f"Curei pq a mana ta alta 90%")
        time.sleep(1)  # Pequena pausa para evitar sobrecarga de CPU

def start_manage_supplies():
    stop_event = threading.Event()
    thread = threading.Thread(target=manage_supplies, args=(stop_event,))
    thread.daemon = True
    thread.start()
    return stop_event, thread

if __name__ == "__main__":
    stop_event, thread = start_manage_supplies()

    # Exemplo de controle de execução
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        thread.join()
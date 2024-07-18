import pyautogui
import threading
import time
import logging
from pynput.keyboard import Key, Controller as KeyboardController

# Constantes
LIFE_REGION = (1766, 304, 92, 5)
MANA_REGION = (1766, 316, 92, 5)
# LIFE_COLOR = (240, 97, 97)  # MONITOR
# MANA_COLOR = (83, 80, 217)  # MONITOR
LIFE_COLOR = (254, 112, 112) # NOTEBOOK
MANA_COLOR = (101, 98, 239)  # NOTEBOOK
MANA_FULL = (59, 79, 122)
WIDTH = 92

# Inicializando controlador de teclado
keyboard = KeyboardController()

def calculate_width(percent):
    return int(WIDTH * percent / 100)

def pixel_matches_color(region, percent, color):
    result_percent = calculate_width(percent)
    x = region[0] + result_percent
    y = region[1] + region[3]
    return pyautogui.pixelMatchesColor(int(x), int(y), color, 10)

def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

def manage_supplies(stop_event):
    while not stop_event.is_set():
        if not pixel_matches_color(LIFE_REGION, 30, LIFE_COLOR):
            press_key(Key.f1)
            print(f"Potei porque a vida está baixa (30%)")
        if not pixel_matches_color(LIFE_REGION, 60, LIFE_COLOR):
            press_key(Key.f3)
            print(f"Curei porque a vida está baixa (60%)")
        if not pixel_matches_color(MANA_REGION, 25, MANA_COLOR):
            press_key(Key.f2)
            print(f"Potei porque a mana está baixa (25%)")
        if pixel_matches_color(MANA_REGION, 95, MANA_COLOR):
            press_key(Key.f3)
            print(f"Curei porque a mana está alta (95%)")
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
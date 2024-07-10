import pyautogui
import threading
import keyboard
import time
import random
# from vida_mana import manage_supplies
from vida_mana import manage_supplies, start_manage_supplies

# Configurações
TRAINING_INTERVAL = 1 * 60  # 8 minutos em segundos
CLICK_POSITION = (788, 479)
F12_PRESS_COUNT = 3
MOVEMENT_KEYS = ['a', 'w', 's', 'd']

stop_event = threading.Event()
keyboard.wait('h')

def perform_training():
    while not stop_event.is_set():
        # Realiza a ação de treino
        pyautogui.moveTo(CLICK_POSITION)
        for _ in range(F12_PRESS_COUNT):
            pyautogui.press('F12')
            print('batendo food')
            time.sleep(0.5)  # Pequeno delay entre os cliques
        
        # Movimenta o personagem aleatoriamente para os quatro lados
        random.shuffle(MOVEMENT_KEYS)
        pyautogui.keyDown('ctrl')
        for key in MOVEMENT_KEYS:
            pyautogui.press(key)
            time.sleep(0.1)  # Pequeno delay entre os movimentos
        pyautogui.keyUp('ctrl')
        print(f"Movimento aleatório: {MOVEMENT_KEYS}")

        # Espera até o próximo ciclo de treino
        for _ in range(TRAINING_INTERVAL):
            if stop_event.is_set():
                break
            time.sleep(1)

def stop_bot():
    print("Parando o bot...")
    stop_event.set()

def main():
    # Inicia a thread de monitoramento de vida e mana
    stop_event, th_suplies = start_manage_supplies()

    # Inicia a thread de treino
    training_thread = threading.Thread(target=perform_training)
    training_thread.daemon = True
    training_thread.start()

    # Aguarda a tecla 'Esc' para parar o bot
    keyboard.wait('esc')
    stop_bot()

    # Para a thread de monitoramento de vida e mana
    stop_event.set()
    th_suplies.join()
    training_thread.join()

if __name__ == "__main__":
    main()
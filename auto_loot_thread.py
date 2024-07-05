import pyautogui as pg
import threading
import time
import constants

pg.useImageNotFoundException(False)


def find_and_click(image_paths, stop_event, done_event):
    clicked_locations = set()

    while not stop_event.is_set():
        new_locations = []
        
        for image_path in image_paths:
            try:
                location = pg.locateCenterOnScreen(image_path, confidence=0.5, region=constants.REGION_LOOTABLE)
                if location and location not in clicked_locations:
                    new_locations.append(location)
            except Exception as e:
                print(f"Erro ao tentar localizar a imagem {image_path}: {e}")

        if new_locations:
            for location in new_locations:
                pg.moveTo(location)
                pg.rightClick()
                clicked_locations.add(location)
                time.sleep(0.5)  # Pequena pausa entre cliques para evitar problemas de detecção
        
        
        # Aguarda um tempo antes de verificar novamente (ajuste conforme necessário)
        time.sleep(1)
        break
    
    done_event.set()

def start_autoLoot(image_paths):
    stop_event = threading.Event()
    done_event = threading.Event()
    thread = threading.Thread(target=find_and_click, args=(image_paths, stop_event, done_event))
    thread.daemon = True
    thread.start()
    return stop_event, done_event, thread

if __name__ == "__main__":
    image_paths = ['imgs/dead_troll.png']  # Adicione mais caminhos de imagens conforme necessário exemplo: ['deadTroll.png', 'deadGoblin.png']
    stop_event, done_event, thread = start_autoLoot(image_paths)

    # Exemplo de controle de execução
    try:
        while not done_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        thread.join()

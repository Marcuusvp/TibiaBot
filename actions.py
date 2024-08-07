import pyautogui as pg
import os
import random
import constants
from concurrent.futures import ThreadPoolExecutor, as_completed
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

pg.useImageNotFoundException(False)

# Inicializando controladores do mouse e teclado
mouse = MouseController()
keyboard = KeyboardController()

def check_ring():
    return pg.locateOnScreen('imgs/noRing.png', confidence=0.8, region=constants.RING_AREA)

def check_auto_chase():
    return pg.locateOnScreen('imgs/auto_chase.png', confidence=0.8, region=constants.AUTO_CHASE_AREA)

def check_battle():
    return pg.locateOnScreen('imgs/battle.png', confidence=0.8, region=constants.REGION_BATTLE)

def check_image(filename, region):
    if filename.endswith('.png'):
        if pg.locateOnScreen(f'ignored_Monsters/{filename}', confidence=0.8, region=region):
            return True
    return False

def ignorar_monstro(region):
    with ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir('ignored_Monsters'):
            futures.append(executor.submit(check_image, filename, region))
        
        for future in as_completed(futures):
            if future.result():
                return True
    
    return False

def get_loot():
    random.shuffle(constants.LIST_POSITION_LOOT)

    keyboard.press(Key.alt)

    for position in constants.LIST_POSITION_LOOT:
        mouse.position = position
        mouse.click(Button.left, 1)

    keyboard.release(Key.alt)
    mouse.position = (788, 479)

def execute_hotkey(hotkey):
    keyboard.press(hotkey)
    keyboard.release(hotkey)

def hole_up():
    mouse.position = (788, 479)
    print('Movi o mouse pro centro')
    pg.sleep(2)

    execute_hotkey(Key.f10)
    mouse.click(Button.left, 1)
    print('Apertei F10')

def ladder_up():
    mouse.position = (788, 479)
    mouse.click(Button.left)

def ladder_up_ne():
    mouse.position = (838, 389)
    mouse.click(Button.left)

def ladder_up_nw():
    mouse.position = (710, 405)
    mouse.click(Button.left)

def down_hole():
    execute_hotkey('w')

def zoom_in(times):
    zoom = pg.locateCenterOnScreen('imgs/zoomIn.png', region=constants.ZOOM_IN_REGION, confidence=0.8)
    if zoom is not None:
        for _ in range(times):
            mouse.position = zoom
            mouse.click(Button.left, 1)
            pg.sleep(0.1)
        mouse.position = (788, 479)
    else:
        print("Botão de zoom não encontrado na tela.")

def zoom_out(times):
    zoom = pg.locateCenterOnScreen('imgs/zoomOut.png', region=constants.ZOOM_OUT_REGION, confidence=0.8)
    if zoom is not None:
        for _ in range(times):
            mouse.position = zoom
            mouse.click(Button.left, 1)
            pg.sleep(0.1)
        mouse.position = (788, 479)
    else:
        print("Botão de zoom não encontrado na tela.")

def encontrar_imagem_na_regiao(imagem, regiao):
    posicao = pg.locateCenterOnScreen(imagem, region=regiao, confidence=0.8)
    return posicao

def descartar_itens():
    for item in os.listdir(constants.DISPOSABLE_ITENS_FOLDER):
        caminho_imagem = os.path.join(constants.DISPOSABLE_ITENS_FOLDER, item)
        
        if not caminho_imagem.lower().endswith(('.png')):
            continue
        
        posicao = encontrar_imagem_na_regiao(caminho_imagem, constants.REGIAO_LOOT_DISPOSABLE)
        
        if posicao:
            mouse.position = posicao
            keyboard.press(Key.ctrl)
            mouse.press(Button.left)
            mouse.position = (788, 479)
            mouse.release(Button.left)
            keyboard.release(Key.ctrl)
            return
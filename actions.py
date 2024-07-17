import pyautogui as pg
import keyboard
import constants
import random
import os
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

pg.useImageNotFoundException(False)
# Inicializando controladores do mouse e teclado
mouse = MouseController()
keyboard = KeyboardController()
# keyboard.wait('h')
#print(pg.locateOnScreen('imgs/battle2.png', confidence=0.8))
# print(pg.pixel(x=1582, y=38))
def check_ring():
    # print(pg.locateOnScreen('imgs/noRing.png', confidence=0.8, region=constants.RING_AREA))
    return pg.locateOnScreen('imgs/noRing.png', confidence=0.8, region=constants.RING_AREA)

def check_auto_chase():
    return pg.locateOnScreen('imgs/auto_chase.png', confidence=0.8, region=constants.AUTO_CHASE_AREA)

def check_battle():
    return pg.locateOnScreen('imgs/battle.png', confidence=0.8, region=constants.REGION_BATTLE)

def kill_monster():
    while check_battle() == None:
        pg.press('space')
        if pg.pixel(x=1582, y=38) == (254, 0, 0) or pg.pixel(x=1582, y=38) == (255, 0, 0):
            while pg.pixel(x=1582, y=38) == (254, 0, 0) or pg.pixel(x=1582, y=38) == (255, 0, 0):
                pg.sleep(1)
                print('Atacando target')     
        print('procurando targets')

def get_loot():
    random.shuffle(constants.LIST_POSITION_LOOT)
    
    # Pressionar a tecla 'alt'
    keyboard.press(Key.alt)
    
    # Clicar em cada posição na lista
    for position in constants.LIST_POSITION_LOOT:
        mouse.position = position
        mouse.click(Button.left, 1)
    
    # Soltar a tecla 'alt'
    keyboard.release(Key.alt)
    
    # Mover o mouse para a posição final
    mouse.position = (788, 479)

def execute_hotkey(hotkey):
    pg.press(hotkey)

def hole_up():
    pg.moveTo(788, 479)
    print('Movi o mouse pro centro')
    pg.sleep(2)

    pg.press('F10')
    pg.click()
    print('apertei F10')

def ladder_up():
    pg.moveTo(788, 479)
    pg.click(button="left")

def ladder_up_ne():
    pg.moveTo(838, 389)
    pg.click()

def ladder_up_nw():
    pg.moveTo(710, 405)
    pg.click()

def down_hole():
    pg.press('w')    

def zoom_in(times):
    zoom = pg.locateCenterOnScreen('imgs/zoomIn.png', region=constants.ZOOM_IN_REGION, confidence=0.8)
    if zoom is not None:
        for _ in range(times):
            pg.moveTo(zoom)
            pg.click()
            pg.sleep(0.1)# Pequena pausa para garantir que os cliques sejam registrados
        pg.moveTo(788, 479)
    else:
        print("Botão de zoom não encontrado na tela.")

def zoom_out(times):
    zoom = pg.locateCenterOnScreen('imgs/zoomOut.png', region=constants.ZOOM_OUT_REGION, confidence=0.8)
    if zoom is not None:
        for _ in range(times):
            pg.moveTo(zoom)
            pg.click()
            pg.sleep(0.1)# Pequena pausa para garantir que os cliques sejam registrados
        pg.moveTo(788, 479)
    else:
        print("Botão de zoom não encontrado na tela.")

def encontrar_imagem_na_regiao(imagem, regiao):
    # Procura pela imagem na região especificada da tela
    posicao = pg.locateCenterOnScreen(imagem, region=regiao, confidence=0.8)
    return posicao

def descartar_itens():
    # Itera sobre todos os arquivos na pasta disposable_itens
    for item in os.listdir(constants.DISPOSABLE_ITENS_FOLDER):
        caminho_imagem = os.path.join(constants.DISPOSABLE_ITENS_FOLDER, item)
        
        # Verifica se o arquivo é uma imagem
        if not caminho_imagem.lower().endswith(('.png')):
            continue
        
        # Encontra a imagem na região especificada
        posicao = encontrar_imagem_na_regiao(caminho_imagem, constants.REGIAO_LOOT_DISPOSABLE)
        
        if posicao:
            # Posiciona o mouse no centro da imagem
            pg.moveTo(posicao)
            
            # Segura a tecla Control, clica e arrasta o item para a posição de descarte
            pg.keyDown('ctrl')
            pg.mouseDown()
            pg.moveTo(788, 479)
            pg.mouseUp()
            pg.keyUp('ctrl')
            
            # Item descartado, saímos da função
            return


def rotate_skills():
    while not event_rotate_skills.is_set():
        for attack in constants.LIST_HOTKEY_ATTACKS:
            if event_rotate_skills.is_set():
                return
            if pyautogui.locateOnScreen('battle.png', confidence=0.8, region=constants.REGION_BATTLE):
                continue
            print('Executando: ', attack['hotkey'])
            pyautogui.press('space')
            pyautogui.press(attack["hotkey"])
            pyautogui.sleep(attack["delay"])

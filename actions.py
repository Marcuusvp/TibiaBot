import pyautogui as pg
import keyboard
import constants
import random
import os

pg.useImageNotFoundException(False)

# keyboard.wait('h')
#print(pg.locateOnScreen('imgs/battle2.png', confidence=0.8))
# print(pg.pixel(x=1582, y=38))
def check_ring():
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
    # pg.PAUSE = 0.05
    for position in constants.LIST_POSITION_LOOT:
        pg.moveTo(position)
        pg.click(button="right")
    pg.PAUSE = 0.03
    pg.moveTo(788, 479)

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
    pg.click(button="right")

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

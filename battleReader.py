import constants
import cv2
import pyautogui
import numpy as np
import pytesseract
import constants
import time
import keyboard

keyboard.wait('h')

LIFE_REGIONS = [
    (360, 27, 77, 14),
    (1130,27,84,13)
]
# BATTLE_REGIONS = [
#     (1574, 39, 150, 19),
#     (1574, 60, 151, 19),
#     (1574, 82, 151, 19),
#     (1574, 105, 151, 19),
#     (1574, 126, 151, 19),
#     (1574, 147, 151, 19)
# ]
# Defina o caminho para o executável Tesseract se necessário
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_region(region):
    # Captura a região da tela definida por region
    screenshot = pyautogui.screenshot(region=region)
    
    # Convertendo a imagem para um formato que o OpenCV possa usar
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    return screenshot

def recognize_text(image):
    # Usa pytesseract para reconhecer texto na imagem inteira
    text = pytesseract.image_to_string(image, lang='eng')
    if text == '':
        return None
    if "Mad Sheep" in text:
        return 'Mad Sheep'
    if "Spider" in text:
        return 'Aranha'
    else:
        return text

def main(battle_regions):
    for region in battle_regions:
        # Captura a imagem de cada região da Battle List
        region_image = capture_region(region)
        
        # Reconhece texto na imagem capturada
        recognized_text = recognize_text(region_image)
        print(f"Text in region {region}: {recognized_text}")

if __name__ == "__main__":
    main(LIFE_REGIONS)

main(LIFE_REGIONS)

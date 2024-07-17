import cv2
import pyautogui
import numpy as np
import pytesseract

# Defina o caminho para o executável Tesseract se necessário
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

IGNORED_MONSTERS = ["Ghoul"]  # Lista de monstros a serem ignorados

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
    for monster in IGNORED_MONSTERS:
        if monster in text:
            return None
    return text

def process_battle_regions(battle_regions):
    results = {}
    for region in battle_regions:
        # Captura a imagem de cada região da Battle List
        region_image = capture_region(region)
        
        # Reconhece texto na imagem capturada
        recognized_text = recognize_text(region_image)
        results[region] = recognized_text
        print(f"Text in region {region}: {recognized_text}")
    return results


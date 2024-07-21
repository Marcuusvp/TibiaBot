import cv2
import pyautogui
import numpy as np
import os
import uuid

IGNORED_MONSTERS_FOLDER = "ignored_Monsters"  # Pasta contendo imagens de monstros a serem ignorados

def capture_region(region):
    # Captura a região da tela definida por region
    screenshot = pyautogui.screenshot(region=region)
    # Convertendo a imagem para um formato que o OpenCV possa usar
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

def preprocess_image(image):
    # Converte para escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Aplica threshold binário
    _, binarized_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    
    # Define o ponto de corte (ajuste conforme necessário)
    crop_x_start = 15  # Posição X inicial para cortar a imagem
    cropped_image = binarized_image[:, crop_x_start:]
    
    # Salva a imagem binarizada e cortada na pasta raiz
    save_binary_image(cropped_image)
    return cropped_image

def save_binary_image(image):
    # Gera um nome de arquivo único
    filename = f"binary_image_{uuid.uuid4().hex}.png"
    filepath = os.path.join(os.getcwd(), filename)
    cv2.imwrite(filepath, image)

def load_ignored_monsters():
    ignored_monsters = []
    for filename in os.listdir(IGNORED_MONSTERS_FOLDER):
        if filename.endswith('.png'):
            filepath = os.path.join(IGNORED_MONSTERS_FOLDER, filename)
            image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            _, binarized_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
            ignored_monsters.append(binarized_image)
    return ignored_monsters

def detect_monster(image):
    ignored_monsters = load_ignored_monsters()
    for ignored_monster in ignored_monsters:
        if np.array_equal(image, ignored_monster):
            return True

    # Exemplo de detecção simples baseado em contornos
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Ajuste a área mínima conforme necessário
            return True
    
    return False

def process_battle_region(region):
    region_image = capture_region(region)
    preprocessed_image = preprocess_image(region_image)
    detected = detect_monster(preprocessed_image)
    return detected

process_battle_region((1574, 39, 150, 19))
process_battle_region((1574, 60, 151, 19))
process_battle_region((1574, 82, 151, 19))
process_battle_region((1574, 105, 151, 19))
process_battle_region((1574, 126, 151, 19))
process_battle_region((1574, 147, 151, 19))
# (1574, 39, 150, 19),
#     (1574, 60, 151, 19),
#     (1574, 82, 151, 19),
#     (1574, 105, 151, 19),
#     (1574, 126, 151, 19),
#     (1574, 147, 151, 19)
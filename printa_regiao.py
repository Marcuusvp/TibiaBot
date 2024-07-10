import pyautogui
import cv2
import numpy as np
import os
import uuid
import time
import keyboard

# Ajustar essas regiões para os novos locais onde os números são exibidos
# LIFE_REGION = (1868, 302, 48, 13)  # Ajuste conforme necessário
# MANA_REGION = (1868, 316, 48, 13)  # Ajuste conforme necessário
LIFE_REGION = (1766, 304, 92, 5)
MANA_REGION = (1766, 316, 92, 5)
keyboard.wait('h')

def capture_region(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

def get_pixel_color(image, width_percentage, height_percentage=0.5):
    height, width, _ = image.shape
    x = int(width * width_percentage)
    y = int(height * height_percentage)
    color = image[y, x]
    return color

def capture_and_print_colors():
    life_image = capture_region(LIFE_REGION)
    mana_image = capture_region(MANA_REGION)
    
    # Coordenadas para os pontos especificados (80%, 50%, 10% da largura e 50% da altura)
    width_percentages = [0.8, 0.5, 0.1]
    
    for width_percentage in width_percentages:
        life_color = get_pixel_color(life_image, width_percentage)
        mana_color = get_pixel_color(mana_image, width_percentage)
        
        print(f"Life region pixel color at {int(width_percentage*100)}% width: {life_color}")
        print(f"Mana region pixel color at {int(width_percentage*100)}% width: {mana_color}")

if __name__ == "__main__":
    while True:
        capture_and_print_colors()
        time.sleep(1)  # Adjust the sleep time as needed


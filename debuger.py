import pyautogui
import threading
import json
import constants
import actions
import signal
import sys
import keyboard
from auto_attack_thread import start_monitoring

while True:
    global running, event_rotate_skills, th_rotate_skills, event_suplies, th_suplies, event_battle, th_battle, event_loot, th_loot, bot_running
    keyboard.wait('h')
    event_battle, done_battle, th_battle = start_monitoring()
    while not done_battle.is_set():
        pass
    th_battle.join()
from scapy.all import *
import time
import random
# Функция для генерации случайного времени ожидания
def random_sleep():
    return random.randint(1000, 6000) / 1000  # Генерируем случайное число в секундах
from scapy.all import *
import time
import random

# Функция для генерации случайного времени ожидания
def random_sleep():
    return random.randint(1000, 6000) / 1000  # Генерируем случайное число в секундах

# Данные для PUT-запроса
put_data = "cat /etc/passwd"

# Создание HTTP PUT-запроса
http_request = (
    Ether(src="00:00:00:00:00:04", dst="fe:91:b3:92:f1:98")
    / IP(src="100.0.0.10", dst="100.0.0.45")
    / TCP(dport=80, sport=80, flags="S")  # Устанавливаем флаг SYN (начало установки соединения)
    / ("PUT / HTTP/1.1\r\n"
       "Host: 100.0.0.45\r\n"
       "Content-Type: application/x-www-form-urlencoded\r\n"
       f"Content-Length: {len(put_data)}\r\n"
       "\r\n"
       f"{put_data}")
)

# Отправка запроса
sendp(http_request, iface="h1-eth0")  # Отправляем пакет и ожидаем ответа
time.sleep(random_sleep())

# Симуляция отрицательного ответа на HTTP PUT-запрос
http_response = (
    Ether(src="00:00:00:00:00:08", dst="00:00:00:00:00:04")
    / IP(src="100.0.0.30", dst="100.0.0.10")
    / TCP(dport=80, sport=80, flags="RA")  # Устанавливаем флаг RST (отклонение соединения)
)

# Отправка отрицательного ответа
sendp(http_response, iface="h1-eth0")


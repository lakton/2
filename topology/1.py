from scapy.all import *
import time

# Создание HTTP POST-запроса
http_request = (
    Ether(src="00:00:00:00:00:04", dst="fe:91:b3:92:f1:98")
    / IP(src="100.0.0.10", dst="100.0.0.45")
    / TCP(dport=80, sport=20)
    / "POST / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 0\r\n\r\n"
)

# Отправка запроса
sendp(http_request, iface="h1-eth0")
time.sleep(5)

# Симуляция ответа на HTTP POST-запрос
http_response = (
    Ether(src="fe:91:b3:92:f1:98", dst="00:00:00:00:00:04")
    / IP(src="100.0.0.45", dst="100.0.0.10")
    / TCP(dport=20, sport=80)
    / "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, world!"
)

# Отправка ответа
sendp(http_response, iface="h1-eth0")

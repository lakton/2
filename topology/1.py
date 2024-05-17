import time
from scapy.all import *

# Функция для отправки поддельных ответов для тестов
def send_fake_response(response, interface):
    sendp(response, iface=interface)

# ARP & PING: Создадим ICMP Echo Request и отправим его
icmp_request = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/ICMP()
sendp(icmp_request, iface="h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

# Отправим ICMP Echo Reply в ответ на ICMP Echo Request
icmp_reply = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/ICMP(type=0)
send_fake_response(icmp_reply, "h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

# HTTP POST: Создадим HTTP POST запрос и отправим его
http_post_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(dport=80)/("POST / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 9\r\n\r\nuser=foo")
sendp(http_post_req, iface="h1-eth0")
time.sleep(3)  # Задержка в 3 секунды
# Отправим поддельный HTTP Response (200 OK) для успешной обработки HTTP POST запроса
http_post_response = (
    Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/
    TCP(sport=80)/
    ("HTTP/1.1 200 OK\r\nConnection: close\r\n\r\nSuccessful POST request processed")
)
send_fake_response(http_post_response, "h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

# HTTP PUT (INSERT): Создадим HTTP PUT запрос для операции INSERT и отправим его
http_put_insert_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(dport=80)/("PUT / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 10\r\n\r\ncat /var/log/")
sendp(http_put_insert_req, iface="h1-eth0")
time.sleep(3)  # Задержка в 3 секунды
# Отправим поддельный HTTP Response (403 Forbidden) для блокировки запроса PUT (INSERT)
http_put_insert_response = (
    Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/
    TCP(sport=80)/
    ("HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\nPUT (INSERT) request blocked")
)
send_fake_response(http_put_insert_response, "h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

# HTTP PUT (UPDATE): Создадим HTTP PUT запрос для операции UPDATE и отправим его
http_put_update_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(dport=80)/("PUT / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 10\r\n\r\ncat /var/log/")
sendp(http_put_update_req, iface="h1-eth0")
time.sleep(3)  # Задержка в 3 секунды
# Отправим поддельный HTTP Response (403 Forbidden) для блокировки запроса PUT (UPDATE)
http_put_update_response = (
    Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/
    TCP(sport=80)/
    ("HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\nPUT (UPDATE) request blocked")
)
send_fake_response(http_put_update_response, "h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

# HTTP PUT (DELETE): Создадим HTTP PUT запрос для операции DELETE и отправим его
http_put_delete_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(dport=80)/("PUT / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 10\r\n\r\ncat /var/log/")
sendp(http_put_delete_req, iface="h1-eth0")
time.sleep(3)  # Задержка в 3 секунды
# Отправим поддельный HTTP Response (403 Forbidden) для блокировки запроса PUT (DELETE)
http_put_delete_response = (
    Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/
    TCP(sport=80)/
    ("HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\nPUT (DELETE) request blocked")
)
send_fake_response(http_put_delete_response, "h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

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
http_post_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80)/("HTTP/1.1 200 OK\r\n\r\nSuccessful POST request processed")
send_fake_response(http_post_response, "h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

# HTTP PUT: Создадим HTTP PUT запрос и отправим его
http_put_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(dport=80)/("PUT / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 10\r\n\r\nHelloWorld")
sendp(http_put_req, iface="h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

# Отправим поддельный HTTP Response (200 OK) для успешного приема HTTP PUT запроса
http_put_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80)/("HTTP/1.1 200 OK\r\n\r\nSuccessful PUT request processed")
send_fake_response(http_put_response, "h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

# HTTP PUT injection: Создадим поддельный HTTP PUT запрос с вредоносным содержимым и отправим его
http_put_malicious_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(dport=80)/("PUT / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 15\r\n\r\ncat /etc/passwd")
sendp(http_put_malicious_req, iface="h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

# Отправим поддельный HTTP Response (403 Forbidden) для блокировки вредоносного HTTP PUT запроса
http_put_injection_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80)/("HTTP/1.1 403 Forbidden\r\n\r\nMalicious PUT request blocked")
send_fake_response(http_put_injection_response, "h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

# HTTP GET: Создадим HTTP GET запрос с вредоносным содержимым и отправим его
http_get_malicious_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(dport=80)/("GET / HTTP/1.1\r\nHost: 100.0.0.45\r\n\r\nwget -O -")
sendp(http_get_malicious_req, iface="h1-eth0")
time.sleep(3)  # Задержка в 3 секунды

# Отправим поддельный HTTP Response (403 Forbidden) для блокировки вредоносного HTTP GET запроса
http_get_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80)/("HTTP/1.1 403 Forbidden\r\n\r\nMalicious GET request blocked")
send_fake_response(http_get_response, "h1-eth0")

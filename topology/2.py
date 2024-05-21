from scapy.all import *

# Создание HTTP POST-ответа
http_response = Ether(src="fe:91:b3:92:f1:98", dst="00:00:00:00:00:04") / IP(src="100.0.0.45", dst="100.0.0.10") / TCP(dport=20, sport=80) / \
                "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, world!"

# Отправка ответа
sendp(http_response, iface="h1-eth0")

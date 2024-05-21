from scapy.all import *

# Определение целевого хоста и порта для TCP handshake
target_ip = "100.0.0.45"  # Замените на реальный IP-адрес целевого сервера
target_port = 80  # Замените на реальный порт целевого сервера

# Исходные IP и интерфейс отправителя
source_ip = "100.0.0.10"
source_interface = "h1-eth0"

# HTTP POST запрос
http_post_request = IP(src=source_ip, dst=target_ip) / TCP(sport=syn_ack_response[TCP].dport, dport=target_port, flags="PA") / \
                    "POST /submit HTTP/1.1\r\nHost: example.com\r\nContent-Length: 7\r\n\r\nmessage"

# Симулируем ответ на HTTP POST запрос
http_response = IP(src=target_ip, dst=source_ip) / TCP(sport=target_port, dport=syn_ack_response[TCP].dport, flags="PA") / \
                "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 13\r\n\r\nHello, World!"

# Отправляем запрос и получаем ответ
http_post_response = sr1(http_post_request, iface=source_interface)
if http_post_response:
    print("HTTP POST request sent successfully")
    print("Response:", http_post_response.show())
else:
    print("No response received")

# Отправляем HTTP ответ
send(http_response, iface=source_interface)

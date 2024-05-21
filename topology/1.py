from scapy.all import *

# Определение целевого хоста и порта для TCP handshake
target_ip = "100.0.0.45"  # Замените на реальный IP-адрес целевого сервера
target_port = 80  # Замените на реальный порт целевого сервера

# Исходные IP и интерфейс отправителя
source_ip = "100.0.0.10"
source_interface = "h1-eth0"

# Симулируем TCP handshake (отправляем SYN)
syn_packet = IP(src=source_ip, dst=target_ip) / TCP(sport=12345, dport=target_port, flags="S")

# Отправляем SYN пакет и получаем SYN/ACK
syn_ack_response = sr1(syn_packet, iface=source_interface)

if syn_ack_response:
    print("TCP Handshake: SYN sent and SYN/ACK received successfully")
    print("Response:", syn_ack_response.show())
else:
    print("No SYN/ACK response received")

# HTTP POST запрос
http_post_request = IP(src=source_ip, dst=target_ip) / TCP(sport=syn_ack_response[TCP].dport, dport=target_port, flags="PA") / \
                    "POST /submit HTTP/1.1\r\nHost: example.com\r\nContent-Length: 7\r\n\r\nmessage"

# Отправляем HTTP POST запрос и получаем ответ
http_post_response = sr1(http_post_request, iface=source_interface)

if http_post_response:
    print("HTTP POST request sent successfully")
    print("Response:", http_post_response.show())
else:
    print("No response received")

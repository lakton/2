from scapy.all import *

# Определение целевого хоста и порта для TCP handshake
target_ip = "192.168.1.100"  # Замените на реальный IP-адрес целевого сервера
target_port = 80  # Замените на реальный порт целевого сервера

# Исходные IP и интерфейс отправителя
source_ip = "100.0.0.10"
source_interface = "h1-eth0"

# Имитация TCP handshake
syn_packet = IP(src=source_ip, dst=target_ip) / TCP(sport=RandShort(), dport=target_port, flags="S")
syn_ack_response = sr1(syn_packet, iface=source_interface)

if syn_ack_response is None:
    print("No response received")
    exit()

# Ответ на SYN пакет с флагом ACK
ack_packet = IP(src=source_ip, dst=target_ip) / TCP(sport=syn_ack_response[TCP].dport, dport=target_port,
                                                    flags="A", ack=syn_ack_response[TCP].seq + 1, seq=syn_ack_response[TCP].ack)
send(ack_packet, iface=source_interface)

# Ответ на HTTP запрос
http_response = IP(src=target_ip, dst=source_ip) / TCP(sport=target_port, dport=syn_ack_response[TCP].dport, flags="PA") / \
                "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 13\r\n\r\nHello, World!"

send(http_response)

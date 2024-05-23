from scapy.all import IP, ICMP, TCP, UDP, send, sniff

# Отправка различных типов пакетов
icmp_packet = IP(dst="10.0.0.1")/ICMP()
tcp_packet = IP(dst="10.0.0.1")/TCP(dport=80)
udp_packet = IP(dst="10.0.0.1")/UDP(dport=53)
malicious_tcp_packet = IP(dst="10.0.0.1")/TCP(dport=10851) # Малicious TCP пакет

send(icmp_packet)
send(tcp_packet)
send(udp_packet)
send(malicious_tcp_packet)

# Функция для обработки захваченных пакетов
def packet_callback(packet):
    if packet.haslayer(ICMP):
        print(f"Получен ICMP пакет от {packet[IP].src} к {packet[IP].dst}")
    elif packet.haslayer(TCP):
        print(f"Получен TCP пакет от {packet[IP].src} к {packet[IP].dst} на порт {packet[TCP].dport}")
    elif packet.haslayer(UDP):
        print(f"Получен UDP пакет от {packet[IP].src} к {packet[IP].dst} на порт {packet[UDP].dport}")

# Захват пакетов
sniff(filter="ip", prn=packet_callback, count=10)

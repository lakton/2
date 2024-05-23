from scapy.all import IP, ICMP, TCP, UDP, send

# Функция для маскирования IP и портов
def mask_ip_and_ports(packet):
    # Здесь вы можете добавить свою собственную логику маскирования
    # В этом примере мы просто меняем исходный IP и порт на 100.0.0.1 и 12345
    packet[IP].src = "100.0.0.1"
    if TCP in packet:
        packet[TCP].sport = 45545
    elif UDP in packet:
        packet[UDP].sport = 45545

# Отправка различных типов пакетов
icmp_packet = IP(src="100.0.0.45", dst="10.0.0.1")/ICMP()
tcp_packet = IP(src="100.0.0.45", dst="10.0.0.1")/TCP(dport=80)
udp_packet = IP(src="100.0.0.25", dst="10.0.0.1")/UDP(dport=53)
malicious_tcp_packet = IP(src="100.0.0.11", dst="10.0.0.1")/TCP(dport=10851)

# Применяем маскирование к каждому пакету перед отправкой
mask_ip_and_ports(icmp_packet)
mask_ip_and_ports(tcp_packet)
mask_ip_and_ports(udp_packet)
mask_ip_and_ports(malicious_tcp_packet)

# Отправка пакетов
send(icmp_packet)
send(tcp_packet)
send(udp_packet)
send(malicious_tcp_packet)

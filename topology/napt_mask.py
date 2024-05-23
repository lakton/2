from scapy.all import IP, ICMP, send, sniff

# Отправка ICMP пакета от внутреннего хоста
internal_icmp_packet = IP(src="10.0.0.50", dst="100.0.0.10")/ICMP()
send(internal_icmp_packet)

# Функция для обработки захваченных пакетов
def icmp_packet_callback(packet):
    if packet.haslayer(ICMP):
        print(f"Получен ICMP пакет от {packet[IP].src} к {packet[IP].dst}")

# Захват ICMP пакетов
sniff(filter="icmp", prn=icmp_packet_callback, count=5)

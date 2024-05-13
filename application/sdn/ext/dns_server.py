from scapy.all import *

# IP адреса DNS серверов
dns_servers = ["100.0.0.20", "100.0.0.21", "100.0.0.22"]

# Фильтр для перехвата DNS запросов к виртуальному IP адресу
filter = "udp port 53 and ip dst 100.0.0.25"

def balanceDNS(pkt):
    # Проверяем, что пакет содержит DNS запрос и не является ответом на запрос
    if DNS in pkt and pkt[DNS].qr == 0:
        # Извлекаем имя запрошенного домена
        domain_name = pkt[DNSQR].qname.decode('utf-8')
        # Вычисляем хэш от имени домена
        domain_hash = hash(domain_name)
        # Вычисляем индекс сервера в кластере на основе хэша
        server_index = domain_hash % len(dns_servers)
        # Отправляем ответ на запрос на выбранный сервер
        response = IP(dst=dns_servers[server_index])/UDP(sport=53)/DNS(id=pkt[DNS].id, an=DNSRR(rrname=domain_name, rdata=dns_servers[server_index]))
        send(response, verbose=0)

# Запускаем перехват пакетов и балансировку нагрузки
sniff(filter=filter, prn=balanceDNS)

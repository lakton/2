from scapy.all import IP, ICMP, TCP, UDP, send

# Отправка различных типов пакетов
icmp_packet = IP(src="10.0.0.50", dst="100.0.0.45")/ICMP()
tcp_packet = IP(src="10.0.0.50", dst="100.0.0.45")/TCP(dport=80)
udp_packet = IP(src="10.0.0.50", dst="100.0.0.25")/UDP(dport=53)
malicious_tcp_packet = IP(src="10.0.0.50", dst="100.0.0.11")/TCP(dport=10851)

# Отправка пакетов через интерфейс napt-eth1
send(icmp_packet)
send(tcp_packet)
send(udp_packet)
send(malicious_tcp_packet)

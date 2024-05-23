from scapy.all import IP, ICMP, TCP, UDP, send

# Отправка различных типов пакетов
icmp_packet = IP(src="100.0.0.45", dst="100.0.0.1")/ICMP()
tcp_packet = IP(src="100.0.0.45", dst="100.0.0.1")/TCP(dport=80)
udp_packet = IP(src="100.0.0.25", dst="100.0.0.1")/UDP(dport=53)
icmp_packet1 = IP(src="100.0.0.1", dst="10.0.0.1")/ICMP()
tcp_packet1 = IP(src="100.0.0.1", dst="10.0.0.1")/TCP(dport=80)
udp_packet1 = IP(src="100.0.0.1", dst="10.0.0.1")/UDP(dport=53)
icmp_packet2 = IP(src="10.0.0.1", dst="10.0.0.50")/ICMP()
tcp_packet2 = IP(src="10.0.0.1", dst="10.0.0.50")/TCP(dport=80)
udp_packet2 = IP(src="10.0.0.1", dst="10.0.0.50")/UDP(dport=53)

# Отправка пакетов через интерфейс napt-eth1
send(icmp_packet)
send(tcp_packet)
send(udp_packet)

send(icmp_packet1)
send(tcp_packet1)
send(udp_packet1)

send(icmp_packet2)
send(tcp_packet2)
send(udp_packet2)

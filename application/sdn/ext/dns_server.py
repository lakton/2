from scapy.all import DNS, DNSQR, DNSRR, IP, UDP, send, sniff

def dns_responder(local_ip: str):
    def forward_dns(orig_pkt: IP):
        print(f"Forwarding DNS request for {orig_pkt[DNSQR].qname}")
        response = sr1(
            IP(dst='8.8.8.8') /
            UDP(dport=53) /
            DNS(rd=1, id=orig_pkt[DNS].id, qd=DNSQR(qname=orig_pkt[DNSQR].qname)),
            verbose=0,
        )
        resp_pkt = IP(dst=orig_pkt[IP].src, src=local_ip) / UDP(dport=orig_pkt[UDP].sport, sport=53) / DNS()
        resp_pkt[DNS] = response[DNS]
        send(resp_pkt, verbose=0)

    def get_response(pkt: IP):
        if DNS in pkt and pkt[DNS].opcode == 0 and pkt[DNS].ancount == 0:
            if "sdnithub.ru" in pkt[DNSQR].qname.decode():
                spoofed_resp = IP(dst=pkt[IP].src) / UDP(dport=pkt[UDP].sport) / \
                              DNS(id=pkt[DNS].id, an=DNSRR(rrname=pkt[DNSQR].qname, rdata=local_ip))
                send(spoofed_resp, verbose=0)
                print(f"Spoofed DNS Response Sent: {pkt[IP].src}")
            else:
                forward_dns(pkt)

    return get_response

# Настройки для каждого DNS-сервера
local_ips = ["100.0.0.20", "100.0.0.21", "100.0.0.22"]
iface = "lb1-eth2"  # Или ваш сетевой интерфейс по умолчанию

# Запуск DNS-серверов для каждого хоста
for ip in local_ips:
    sniff(filter="udp port 53", prn=dns_responder(ip), iface=iface)
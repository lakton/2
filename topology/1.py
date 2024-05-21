from scapy.all import *
import time

# Данные для POST-запроса
post_data = "param1=value1&param2=value2"

# Создание TCP-соединения (SYN)
syn = (
    Ether(src="00:00:00:00:00:04", dst="fe:91:b3:92:f1:98") /
    IP(src="100.0.0.10", dst="100.0.0.45") /
    TCP(dport=80, sport=12345, flags="S")
)

# Отправка SYN и получение SYN-ACK
syn_ack = srp1(syn, iface="h1-eth0")
time.sleep(1)

# Отправка ACK для завершения установки соединения
ack = (
    Ether(src="00:00:00:00:00:04", dst="fe:91:b3:92:f1:98") /
    IP(src="100.0.0.10", dst="100.0.0.45") /
    TCP(dport=80, sport=12345, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1)
)

sendp(ack, iface="h1-eth0")

# Создание и отправка HTTP POST-запроса
http_post_request = (
    Ether(src="00:00:00:00:00:04", dst="fe:91:b3:92:f1:98") /
    IP(src="100.0.0.10", dst="100.0.0.45") /
    TCP(dport=80, sport=12345, flags="PA", seq=ack.seq, ack=ack.ack) /
    (
        "POST / HTTP/1.1\r\n"
        "Host: sdnithub.com\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(post_data)}\r\n"
        "\r\n"
        f"{post_data}"
    )
)

sendp(http_post_request, iface="h1-eth0")
time.sleep(1)

# Симуляция ответа на HTTP POST-запрос
http_response = (
    Ether(src="fe:91:b3:92:f1:98", dst="00:00:00:00:00:04") /
    IP(src="100.0.0.45", dst="100.0.0.10") /
    TCP(dport=12345, sport=80, flags="PA", seq=ack.ack, ack=ack.seq + len(post_data) + len(
        "POST / HTTP/1.1\r\n"
        "Host: sdnithub.com\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(post_data)}\r\n"
        "\r\n"
    )) /
    "HTTP/1.1 200 OK\r\n"
    "Content-Length: 0\r\n"
    "\r\n"
)

sendp(http_response, iface="h1-eth0")
time.sleep(1)

# Завершение TCP-сессии (FIN)
fin = (
    Ether(src="00:00:00:00:00:04", dst="fe:91:b3:92:f1:98") /
    IP(src="100.0.0.10", dst="100.0.0.45") /
    TCP(dport=80, sport=12345, flags="FA", seq=ack.seq + len(post_data), ack=ack.ack + len(
        "HTTP/1.1 200 OK\r\n"
        "Content-Length: 0\r\n"
        "\r\n"
    ))
)

sendp(fin, iface="h1-eth0")

fin_ack = srp1(fin, iface="h1-eth0")
time.sleep(1)

final_ack = (
    Ether(src="00:00:00:00:00:04", dst="fe:91:b3:92:f1:98") /
    IP(src="100.0.0.10", dst="100.0.0.45") /
    TCP(dport=80, sport=12345, flags="A", seq=fin_ack.ack, ack=fin_ack.seq + 1)
)

sendp(final_ack, iface="h1-eth0")

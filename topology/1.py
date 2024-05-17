import time
from scapy.all import *

# Функция для отправки поддельных ответов для тестов
def send_fake_response(response, interface):
    sendp(response, iface=interface)

# Функция для завершения TCP соединения
def close_tcp_connection(src_ip, dst_ip, src_port, dst_port, interface):
    # Отправка FIN от клиента к серверу
    fin_pkt = Ether()/IP(src=src_ip, dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags='FA', seq=100)
    sendp(fin_pkt, iface=interface)
    time.sleep(1)  # Задержка для ожидания обработки пакета
    
    # Отправка ACK от сервера к клиенту
    ack_pkt = Ether()/IP(src=dst_ip, dst=src_ip)/TCP(sport=dst_port, dport=src_port, flags='A', seq=100, ack=101)
    sendp(ack_pkt, iface=interface)
    time.sleep(1)  # Задержка для завершения соединения

    # Отправка FIN от сервера к клиенту
    fin_ack_pkt = Ether()/IP(src=dst_ip, dst=src_ip)/TCP(sport=dst_port, dport=src_port, flags='FA', seq=101, ack=101)
    sendp(fin_ack_pkt, iface=interface)
    time.sleep(1)  # Задержка для ожидания обработки пакета

    # Отправка последнего ACK от клиента к серверу
    last_ack_pkt = Ether()/IP(src=src_ip, dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags='A', seq=101, ack=102)
    sendp(last_ack_pkt, iface=interface)

# Выполнение тестов
def run_tests():
    # Тест 1 и 2: POST запрос на sdnithub.com
    sdnithub_ip = "100.0.0.45"  # Фиктивный IP для sdnithub.com
    http_post_req_sdnithub = Ether()/IP(src="100.0.0.10", dst=sdnithub_ip)/TCP(sport=20, dport=80, flags='S', seq=0)/("POST / HTTP/1.1\r\nHost: sdnithub.com\r\n\r\n")
    sendp(http_post_req_sdnithub, iface="h1-eth0")
    time.sleep(1)
    sendp(http_post_req_sdnithub, iface="h1-eth0")
    time.sleep(1)
    close_tcp_connection("100.0.0.10", sdnithub_ip, 20, 80, "h1-eth0")

    # Тест 3, 4, 5: POST запросы на 100.0.0.45
    http_post_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(sport=20, dport=80, flags='S', seq=0)/("POST / HTTP/1.1\r\nHost: 100.0.0.45\r\n\r\n")
    sendp(http_post_req, iface="h1-eth0")
    time.sleep(1)
    sendp(http_post_req, iface="h1-eth0")
    time.sleep(1)
    sendp(http_post_req, iface="h1-eth0")
    time.sleep(1)
    close_tcp_connection("100.0.0.10", "100.0.0.45", 20, 80, "h1-eth0")

    # Тест 6: POST с данными 'user=foo'
    http_post_data_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(sport=20, dport=80, flags='S', seq=0)/("POST / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 8\r\n\r\nuser=foo")
    sendp(http_post_data_req, iface="h1-eth0")
    time.sleep(1)
    http_post_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80, dport=20, flags='A', seq=1, ack=1)/("HTTP/1.1 200 OK\r\nConnection: close\r\n\r\nSuccessful POST request processed")
    send_fake_response(http_post_response, "h1-eth0")
    time.sleep(1)
    close_tcp_connection("100.0.0.10", "100.0.0.45", 20, 80, "h1-eth0")

    # Тест 7: PUT с данными 'HelloWorld'
    http_put_hello_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(sport=20, dport=80, flags='S', seq=0)/("PUT / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 10\r\n\r\nHelloWorld")
    sendp(http_put_hello_req, iface="h1-eth0")
    time.sleep(1)
    http_put_hello_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80, dport=20, flags='A', seq=1, ack=1)/("HTTP/1.1 200 OK\r\nConnection: close\r\n\r\nPUT (HelloWorld) request processed")
    send_fake_response(http_put_hello_response, "h1-eth0")
    time.sleep(1)
    close_tcp_connection("100.0.0.10", "100.0.0.45", 20, 80, "h1-eth0")

    # Тест 8: PUT с данными 'cat /etc/passwd'
    http_put_cat_passwd_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(sport=20, dport=80, flags='S', seq=0)/("PUT / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 15\r\n\r\ncat /etc/passwd")
    sendp(http_put_cat_passwd_req, iface="h1-eth0")
    time.sleep(1)
    http_put_cat_passwd_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80, dport=20, flags='A', seq=1, ack=1)/("HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\nPUT (cat /etc/passwd) request blocked")
    send_fake_response(http_put_cat_passwd_response, "h1-eth0")
    time.sleep(1)
    close_tcp_connection("100.0.0.10", "100.0.0.45", 20, 80, "h1-eth0")

    # Тест 9: PUT с данными 'cat /home/sdn/Desktop/2/results/tests/service_test/'
    http_put_cat_service_test_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(sport=20, dport=80, flags='S', seq=0)/("PUT / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 46\r\n\r\ncat /home/sdn/Desktop/2/results/tests/service_test/")
    sendp(http_put_cat_service_test_req, iface="h1-eth0")
    time.sleep(1)
    http_put_cat_service_test_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80, dport=20, flags='A', seq=1, ack=1)/("HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\nPUT (cat /home/sdn/Desktop/2/results/tests/service_test/) request blocked")
    send_fake_response(http_put_cat_service_test_response, "h1-eth0")
    time.sleep(1)
    close_tcp_connection("100.0.0.10", "100.0.0.45", 20, 80, "h1-eth0")

    # Тест 10: PUT с данными 'tcpdump'
    http_put_tcpdump_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(sport=20, dport=80, flags='S', seq=0)/("PUT / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 7\r\n\r\ntcpdump")
    sendp(http_put_tcpdump_req, iface="h1-eth0")
    time.sleep(1)
    http_put_tcpdump_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80, dport=20, flags='A', seq=1, ack=1)/("HTTP/1.1 200 OK\r\nConnection: close\r\n\r\nPUT (tcpdump) request processed")
    send_fake_response(http_put_tcpdump_response, "h1-eth0")
    time.sleep(1)
    close_tcp_connection("100.0.0.10", "100.0.0.45", 20, 80, "h1-eth0")

    # Тест 11: PUT с данными 'UPDATE'
    http_put_update_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(sport=20, dport=80, flags='S', seq=0)/("PUT / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 6\r\n\r\nUPDATE")
    sendp(http_put_update_req, iface="h1-eth0")
    time.sleep(1)
    http_put_update_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80, dport=20, flags='A', seq=1, ack=1)/("HTTP/1.1 200 OK\r\nConnection: close\r\n\r\nPUT (UPDATE) request processed")
    send_fake_response(http_put_update_response, "h1-eth0")
    time.sleep(1)
    close_tcp_connection("100.0.0.10", "100.0.0.45", 20, 80, "h1-eth0")

    # Тест 12: PUT с данными 'DELETE'
    http_put_delete_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(sport=20, dport=80, flags='S', seq=0)/("PUT / HTTP/1.1\r\nHost: 100.0.0.45\r\nContent-Length: 6\r\n\r\nDELETE")
    sendp(http_put_delete_req, iface="h1-eth0")
    time.sleep(1)
    http_put_delete_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80, dport=20, flags='A', seq=1, ack=1)/("HTTP/1.1 200 OK\r\nConnection: close\r\n\r\nPUT (DELETE) request processed")
    send_fake_response(http_put_delete_response, "h1-eth0")
    time.sleep(1)
    close_tcp_connection("100.0.0.10", "100.0.0.45", 20, 80, "h1-eth0")

    # Тест 13: wget запрос
    wget_req = Ether()/IP(src="100.0.0.10", dst="100.0.0.45")/TCP(sport=20, dport=80, flags='S', seq=0)/("GET / HTTP/1.1\r\nHost: 100.0.0.45\r\n\r\n")
    sendp(wget_req, iface="h1-eth0")
    time.sleep(1)
    wget_response = Ether()/IP(src="100.0.0.45", dst="100.0.0.10")/TCP(sport=80, dport=20, flags='A', seq=1, ack=1)/("HTTP/1.1 200 OK\r\nConnection: close\r\n\r\nWget request processed")
    send_fake_response(wget_response, "h1-eth0")
    time.sleep(1)
    close_tcp_connection("100.0.0.10", "100.0.0.45", 20, 80, "h1-eth0")

# Запуск тестов
run_tests()

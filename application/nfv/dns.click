// ==================================
// lb1 click
// DNS Service Load Balancer
// ==================================

// AverageCounter
out_eth1 :: AverageCounter;
out_eth2 :: AverageCounter;
in_eth1 :: AverageCounter;
in_eth2 :: AverageCounter;

// Counter for classifier
// packets
pack_req_ex :: Counter;
pack_res_ex :: Counter;
pack_req_in :: Counter;
pack_res_in :: Counter;

// arp
arp_req_ex :: Counter;
arp_res_ex :: Counter;
arp_req_in :: Counter;
arp_res_in :: Counter;

// Service
service_count :: Counter;

// ICMP
icmp_count :: Counter;

// Dropped
drop_ex :: Counter;
drop_ex_ip :: Counter;
drop_in :: Counter;

// Device declaration
fr_ext :: FromDevice(lb1-eth1, METHOD LINUX, SNIFFER false);
to_ext :: Queue(200) -> out_eth1 -> pack_res_ex -> ToDevice(lb1-eth1);
fr_int :: FromDevice(lb1-eth2, METHOD LINUX, SNIFFER false);
to_int :: Queue(200) -> out_eth2 -> pack_res_in -> ToDevice(lb1-eth2);

arpr_ext :: ARPResponder(100.0.0.25 fe:91:b3:92:f1:98);
arpr_int :: ARPResponder(100.0.0.25 9a:c2:77:de:0f:6c);
arpq_ext :: ARPQuerier(100.0.0.25, fe:91:b3:92:f1:98);
arpq_int :: ARPQuerier(100.0.0.25, 9a:c2:77:de:0f:6c);
c_in,c_ex :: Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800, -);
c_ip_in :: IPClassifier(
                        dst 100.0.0.25 udp port 53,
                        dst 100.0.0.25 and icmp,
                        - );
//rewr :: IPRewriter(pattern 100.0.0.25 - 100.0.0.20 - 1 0);
rewr :: IPRewriter(weblb);
weblb :: RoundRobinIPMapper(
			100.0.0.25 - 100.0.0.20 - 1 0,
			100.0.0.25 - 100.0.0.21 - 1 0,
			100.0.0.25 - 100.0.0.22 - 1 0);

// Statistics for report
// pps
outrate :: Script(TYPE PASSIVE, return $(add $(out_eth1.rate) $(out_eth2.rate)))
inrate :: Script(TYPE PASSIVE, return $(add $(in_eth1.rate) $(in_eth2.rate)))

// packet req-resp
packreq_sum :: Script(TYPE PASSIVE, return $(add $(pack_req_ex.count) $(pack_req_in.count)))
packres_sum :: Script(TYPE PASSIVE, return $(add $(pack_res_ex.count) $(pack_res_in.count)))

// arp req-resp
arpreq_sum :: Script(TYPE PASSIVE, return $(add $(arp_req_ex.count) $(arp_req_in.count)))
arpres_sum :: Script(TYPE PASSIVE, return $(add $(arp_res_ex.count) $(arp_res_in.count)))

// drop sum
drop_sum :: Script(TYPE PASSIVE, return $(add $(drop_ex.count) $(drop_ex_ip.count) $(drop_in.count)))

fr_ext -> in_eth1 -> pack_req_ex -> c_in;
c_in[0] -> Print("Получен запрос DNS-пакета") -> arp_req_ex -> arpr_ext[0] -> to_ext;
c_in[1] -> Print("ARP-ответ для внешнего интерфейса") -> arp_res_ex -> [1]arpq_ext;
c_in[2] -> Print("Запрос DNS-пакета обработан и проверен заголовок IP") -> Strip(14) -> CheckIPHeader -> c_ip_in;
c_in[3] -> drop_ex -> Discard;

c_ip_in[0] -> Print("Запрос DNS для подсчета сервисов") -> service_count -> rewr[1] -> [0]arpq_int -> to_int;
c_ip_in[1] -> Print("Счетчик ICMP-пакетов") -> icmp_count -> ICMPPingResponder -> [0]arpq_ext -> to_ext;
c_ip_in[2] -> Print("Удаление внешнего IP-пакета") -> drop_ex_ip -> Discard;

fr_int -> in_eth2 -> pack_req_in -> c_ex;
c_ex[0] -> Print("Запрос DNS для внутреннего интерфейса") -> arp_req_in -> arpr_int[0] -> to_int; 
c_ex[1] -> Print("ARP-ответ для внутреннего интерфейса") -> arp_res_in -> [1]arpq_int;
c_ex[2] -> Print("Запрос DNS-пакета обработан и проверен заголовок IP") -> Strip(14) -> CheckIPHeader -> rewr[0] -> [0]arpq_ext -> to_ext;
c_ex[3] -> Print("Удаление внутреннего пакета") -> drop_in -> Discard;


DriverManager(wait, print > /home/sdn/Desktop/2/results/dns.report"

    =================== Отчет DNS ===================,

    Общее количество полученных и отправленных пакетов (pps):
        - Входящие: $(inrate)
        - Исходящие: $(outrate)

    Общее количество запросов и ответов DNS:
        - Запросы: $(packreq_sum)
        - Ответы: $(packres_sum)

    Общее количество запросов и ответов ARP:
        - Запросы (внешние): $(arpreq_sum)
        - Ответы (внешние): $(arpres_sum)

    Пакеты, отброшенные из-за ошибок:
        - Ошибки внешних пакетов: $(drop_ex.count)
        - Ошибки внешних IP-пакетов: $(drop_ex_ip.count)
        - Ошибки внутренних пакетов: $(drop_in.count)

    Пакеты ICMP:
        - Всего: $(icmp_count.count)

    ======================== Конец отчета ========================,

",stop);
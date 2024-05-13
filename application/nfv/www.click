// ==================================
// lb2 click
// HTTP Service Load Balancer
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
drop_in :: Counter;

// Device declaration
fr_ext :: FromDevice(lb2-eth1, METHOD LINUX, SNIFFER false);
to_ext :: Queue(200) -> out_eth1 -> pack_res_ex -> ToDevice(lb2-eth1);
fr_int :: FromDevice(lb2-eth2, METHOD LINUX, SNIFFER false);
to_int :: Queue(200) -> out_eth2 -> pack_res_in -> ToDevice(lb2-eth2);

// ARP Responder
arpr_ext :: ARPResponder(100.0.0.45 ae:cb:56:11:ce:44);
arpr_int :: ARPResponder(100.0.0.45 3e:2a:d4:cf:8c:e3);

// ARP Querier
arpq_ext :: ARPQuerier(100.0.0.45, ae:cb:56:11:ce:44);
arpq_int :: ARPQuerier(100.0.0.45, 3e:2a:d4:cf:8c:e3);

// Classifier internal and external
c_in,c_ex :: Classifier(12/0806 20/0001,	// ARP Request
			12/0806 20/0002,	// ARP Response
			12/0800, 		// IP Packet
			-); 			// the rest
c_ip_in :: IPClassifier(
			dst 100.0.0.45 tcp port 80, 	// http req
			dst 100.0.0.45 and icmp,	// icmp echo req
			- );

rewr :: IPRewriter(weblb);
weblb :: RoundRobinIPMapper(
			100.0.0.45 - 100.0.0.40 - 1 0,	// 1st webserver
			100.0.0.45 - 100.0.0.41 - 1 0,	// 2nd webserver
			100.0.0.45 - 100.0.0.42 - 1 0);	// 3rd webserver

// Statistics for report
// pps
outrate :: Script(TYPE PASSIVE, return $(add $(out_eth1.rate) $(out_eth2.rate)))
inrate :: Script(TYPE PASSIVE, return $(add $(in_eth1.rate) $(in_eth2.rate)))

// arp req-resp
arpreq_sum :: Script(TYPE PASSIVE, return $(add $(arp_req_ex.count) $(arp_req_in.count)))
arpres_sum :: Script(TYPE PASSIVE, return $(add $(arp_res_ex.count) $(arp_res_in.count)))

// packet req-resp
packreq_sum :: Script(TYPE PASSIVE, return $(add $(pack_req_ex.count) $(pack_req_in.count)))
packres_sum :: Script(TYPE PASSIVE, return $(add $(pack_res_ex.count) $(pack_res_in.count)))

// drop sum
drop_sum :: Script(TYPE PASSIVE, return $(add $(drop_ex.count) $(drop_in.count)))

fr_ext -> in_eth1 -> pack_req_ex -> c_in;
c_in[0] -> Print("Запрос ARP из внешней сети") -> arp_req_ex -> arpr_ext[0] -> to_ext;
c_in[1] -> Print("Ответ ARP из внешней сети") -> arp_res_ex -> [1]arpq_ext;
c_in[2] -> Print("Получен IP-пакет из внешней сети") -> Strip(14) -> CheckIPHeader -> c_ip_in;
c_in[3] -> Print("DROP ex") -> Discard;

c_ip_in[0] -> Print("Перенаправление на сервис из внешней сети") -> service_count -> rewr[1] -> [0]arpq_int -> to_int;
c_ip_in[1] -> Print("Ответ на ICMP-пакет из внутренней сети") -> icmp_count -> ICMPPingResponder -> [0]arpq_ext -> to_ext;
c_ip_in[2] -> Print("DROP ex") -> drop_ex -> Discard;

fr_int -> in_eth2 -> pack_req_in -> c_ex;
c_ex[0] -> Print("Запрос ARP из внутренней сети") -> arp_req_in -> arpr_int[0] -> to_int; 
c_ex[1] -> Print("Ответ ARP из внутренней сети") -> arp_res_in -> [1]arpq_int;
c_ex[2] -> Print("Получен IP-пакет из внутренней сети") -> Strip(14) -> CheckIPHeader -> rewr[0] -> [0]arpq_ext -> to_ext;
c_ex[3] -> Print("DROP in") -> drop_in -> Discard;

DriverManager(wait,  print > /home/sdn/Desktop/2/results/www.report "
    
    =================== Отчет HTTP Балансировщика ===================,

    Общее количество запросов и ответов ARP:
        - Запросы (внешние): $(arpreq_sum)
        - Ответы (внешние): $(arpres_sum)
        - Запросы (внутренние): $(arp_req_in.count)
        - Ответы (внутренние): $(arp_res_in.count)

    Общее количество запросов и ответов IP пакетов:
        - Запросы (внешние): $(pack_req_ex.count)
        - Ответы (внешние): $(pack_res_ex.count)
        - Запросы (внутренние): $(pack_req_in.count)
        - Ответы (внутренние): $(pack_res_in.count)

    Пакеты ICMP:
        - Внешние: $(icmp_count.count)

    Пакеты, отброшенные из-за ошибок:
        - Ошибки внешних пакетов: $(drop_ex.count)
        - Ошибки внутренних пакетов: $(drop_in.count)

    ======================== Конец отчета ========================,

",stop);

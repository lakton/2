// ==================================
// ips click
// Intrusion Prevention System
// ==================================

// Source code for ips

// AverageCounter
out_eth1 :: AverageCounter;
out_eth2 :: AverageCounter;
out_eth3 :: AverageCounter;
in_eth1 :: AverageCounter;
in_eth2 :: AverageCounter;

// Counter for classifier

// packets
pack_req_net :: Counter;
pack_res_net :: Counter;
pack_req_in :: Counter;
pack_res_in :: Counter;
pack_insp :: Counter;

// arp
arp_req_ex :: Counter;
arp_res_ex :: Counter;
//arp_req_in :: Counter;
//arp_res_in :: Counter;

// icmp
icmp_count :: Counter;

// service counter
service_count :: Counter;

// Device declaration
src_net :: FromDevice(ips-eth1, METHOD LINUX, SNIFFER false);
dst_net :: PrioSched -> out_eth1 -> pack_res_net -> ToDevice(ips-eth1);
src_lb :: FromDevice(ips-eth2, METHOD LINUX, SNIFFER false);
dst_lb :: PrioSched -> out_eth2 -> pack_res_in -> ToDevice(ips-eth2);
//src_insp :: FromDevice(s6-eth3, SNIFFER false);
dst_insp :: PrioSched -> out_eth3 -> pack_insp -> ToDevice(ips-eth3);


//FIRST STAGE CLASSIFIER
first_stage :: Classifier(12/0806 20/0001, //ARPreq
                          12/0806 20/0002, //ARPreply
                          12/0800,         //IP packet
                          -);

//SECOND STAGE CLASSIFIER
second_stage :: Classifier(23/01,       //ICMP packets
                           72/48545450, //HTTP PUT/GET packets
                           73/48545450, //HTTP POST
                           47/02,       //SYN
                           47/12,       //SYN ACK
                           47/10,       //ACK
                           47/04,       //RST
                           47/11,       //FIN ACK
                           -);

//THIRD STAGE
third_stage :: Classifier(//66/474554, //GET
                          66/504F5354,  //detect the word POST
                          66/505554,    //detect the word PUT
                          -);
//FOURTH STAGE
fourth_stage :: Classifier(209/636174202f6574632f706173737764,//catpasswd
                           209/636174202f7661722f6c6f672f,    //cat varlog
                           208/494E53455254,                  //INSERT
                           208/555044415445,                  //UPDATE
                           208/44454C455445,                  //DELETE
                           -);

// Statistics for report
// pps
outrate :: Script(TYPE PASSIVE, return $(add $(out_eth1.rate) $(out_eth2.rate) $(out_eth1.rate)))
inrate :: Script(TYPE PASSIVE, return $(add $(in_eth1.rate) $(in_eth2.rate)))

// packet req-resp
packreq_sum :: Script(TYPE PASSIVE, return $(add $(pack_req_net.count) $(pack_req_in.count)))
packres_sum :: Script(TYPE PASSIVE, return $(add $(pack_res_net.count) $(pack_res_in.count) $(pack_insp.count)))

// arp req-resp
// arpreq_sum :: Script(TYPE PASSIVE, return $(add $(arp_req_ex.count) $(arp_req_in.count)))
// arpres_sum :: Script(TYPE PASSIVE, return $(add $(arp_res_ex.count) $(arp_res_in.count)))

DriverManager(wait , print > ../../results/ips.report  "
                print > ips.report "===============ips Report=================",
                print >> ips.report "Input Packet rate (pps) : " $(inrate.run),
                print >> ips.report "Output Packet rate (pps) : " $(outrate.run),
                print >> ips.report " ",
                print >> ips.report "Total # of input packets : " $(packreq_sum.run),
                print >> ips.report "Total # of output packets : "$(packres_sum.run),
                print >> ips.report " ",
                print >> ips.report "Total # of ARP requests : " $(arp_req_ex.count),
                print >> ips.report "Total # of ARP response : " $(arp_res_ex.count),
                print >> ips.report " ",
                print >> ips.report "Total # of service packets : "$(service_count.count),
                print >> ips.report "Total # of ICMP packets : "$(icmp_count.count),
                print >> ips.report "Total # of dropped packets : No dropped packets, malicious packets sent to insp",
                print >> ips.report "=========================================",
              " stop);

//FORWARDER FROM INSIDE NETWORK
src_lb -> in_eth2 -> pack_req_in -> Print(Ответ из внутренней) -> Queue -> [0]dst_net;
//first_stage_int[0] -> arp_req_in -> Queue -> [0]dst_net;
//first_stage_int[1] -> arp_res_in -> Queue -> [0]dst_net;
//first_stage_int[2] -> Print(ReplyFrInside) -> Queue -> [0]dst_net;

//JUST STUPID FORWARDER. don't forget to comment
//src_net -> Queue -> [0]dst_lb;

//MAIN LOGIC
src_net -> in_eth1 -> pack_req_net -> service_count -> first_stage;
first_stage[0]
        -> Print("ARP запрос обработан и направлен на lb1")
	-> arp_req_ex
        -> Queue
        -> [0]dst_lb;
first_stage[1]
        -> Print("ARP ответ обработан и направлен на lb1")
        -> arp_res_ex
	-> Queue
        -> [1]dst_lb;
first_stage[2]
        -> Print("IP пакет обработан и направлен на второй этап")
        -> second_stage;
first_stage[3]
        -> Queue
        -> [0]dst_insp;
//=======================================================
second_stage[0]
        -> Print("Обработан ICMP пакет и направлен на lb1")
	-> icmp_count
        -> Queue
        -> [2]dst_lb;
second_stage[1]                 //HTTP
         -> Print("Обработан HTTP GET/PUT запрос и направлен на третий этап")
         -> third_stage;
second_stage[2]                 //HTTP
         -> Print("Обработан HTTP POST запрос и направлен на третий этап")
         -> third_stage;
second_stage[3]
        -> Print("Обработан SYN пакет и направлен на lb1")
        -> Queue
        -> [3]dst_lb;
second_stage[4]
        -> Print("Обработан SYN-ACK пакет и направлен на lb1")
        -> Queue
        -> [4]dst_lb;
second_stage[5]
        -> Print("Обработан ACK пакет и направлен на lb1")
        -> Queue
        -> [5]dst_lb;
second_stage[6]
        -> Print("Обработан RST пакет и направлен на lb1")
        -> Queue
        -> [6]dst_lb;
second_stage[7]
        -> Print("Обработан FIN-ACK пакет и направлен на lb1")
        -> Queue
        -> [7]dst_lb;
second_stage[8]
        -> Queue
        -> [1]dst_insp;
//==========================================
third_stage[0]
        -> Print("Обработан POST запрос и направлен на lb1")
        -> Queue
        -> [8]dst_lb;
third_stage[1]
	-> Print("Обработан PUT запрос и направлен на четвертый этап")
        -> fourth_stage;
third_stage[2]
        -> Queue
        -> [2]dst_insp;
//=========================================
fourth_stage[0]
        -> Print("Предотвращена попытка запроса на чтение пароля (cat /etc/passwd)")
        -> Queue
        -> [3]dst_insp;
fourth_stage[1]
        -> Print("Предотвращена попытка запроса на чтение логов (cat /var/log)")
        -> Queue
        -> [4]dst_insp;
fourth_stage[2]
        -> Print("Предотвращена попытка INSERT")
        -> Queue
        -> [5]dst_insp;
fourth_stage[3]
        -> Print("Предотвращена попытка UPDATE")
        -> Queue
        -> [6]dst_insp;
fourth_stage[4]
        -> Print("Предотвращена попытка DELETE")
        -> Queue
        -> [7]dst_insp;
fourth_stage[5]
        -> Queue
        -> [9]dst_lb;

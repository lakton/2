m_util="/home/sdn/Desktop/mininet/util/m"
test_dir="/home/sdn/Desktop/2/results/tests/service_test"

touch /home/sdn/Desktop/2/results/resultservice.log
chmod 755 /home/sdn/Desktop/2/results/resultservice.log
cp /dev/null /home/sdn/Desktop/2/results/resultservice.log

touch /home/sdn/Desktop/2/results/service.log
chmod 755 /home/sdn/Desktop/2/results/service.log
cp /dev/null /home/sdn/Desktop/2/results/service.log

touch /home/sdn/Desktop/2/results/servicedns.log
chmod 755 /home/sdn/Desktop/2/results/servicedns.log
cp /dev/null /home/sdn/Desktop/2/results/servicedns.log

touch /home/sdn/Desktop/2/results/servicewww.log
chmod 755 /home/sdn/Desktop/2/results/servicewww.log
cp /dev/null /home/sdn/Desktop/2/results/servicewww.log


#============================================================================
#DNS SERVER TEST
#H1
echo "h1 digging 100.0.0.25 for  " >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 20 dig @100.0.0.25   >> /home/sdn/Desktop/2/results/servicedns.log 2>&1
sleep 5
#H2
echo "h2 digging 100.0.0.25 for  " >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h2 timeout 20 dig @100.0.0.25   >> /home/sdn/Desktop/2/results/servicedns.log 2>&1
sleep 5
#H3
echo "h3 digging 100.0.0.25 for  " >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h3 timeout 20 dig @100.0.0.25   >> /home/sdn/Desktop/2/results/servicedns.log 2>&1
sleep 5
#H4
echo "h4 digging 100.0.0.25 for  " >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h4 timeout 20 dig @100.0.0.25   >> /home/sdn/Desktop/2/results/servicedns.log 2>&1
sleep 10
python3 $test_dir/servdnschecker.py

#============================================================================
#WWW SERVER TEST
echo "h1 curl  " >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 20 curl   -s -X POST -v >> /home/sdn/Desktop/2/results/servicewww.log 2>&1
sleep 5
echo "h2 curl  " >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h2 timeout 20 curl   -s -X POST -v >> /home/sdn/Desktop/2/results/servicewww.log 2>&1
sleep 5
echo "h3 curl  " >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h3 timeout 20 curl   -s -X POST -v >> /home/sdn/Desktop/2/results/servicewww.log 2>&1
sleep 5
echo "h4 curl  " >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h4 timeout 20 curl   -s -X POST -v >> /home/sdn/Desktop/2/results/servicewww.log 2>&1
sleep 10
python3 $test_dir/servwwwchecker.py


#============================================================================
#WWW LB ROUND ROBIN TEST 
echo "WWW LB ROUND ROBIN TEST" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util s7 tcpdump -i s7-eth1 -w $test_dir/71.pcap 2>&1 &
$m_util s7 tcpdump -i s7-eth2 -w $test_dir/72.pcap 2>&1 &
$m_util h1 timeout 20 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
sleep 20
$m_util h1 timeout 20 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
sleep 20
$m_util h1 timeout 20 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
sleep 20
$m_util h1 timeout 20 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
sleep 20
$m_util h1 timeout 20 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
sleep 20
$m_util h1 timeout 20 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
pkill tcp
python3 $test_dir/rrdnschecker.py
sleep 20

#============================================================================
#ips TEST

echo "ips TEST : Allowed packets" >> /home/sdn/Desktop/2/results/service.log 2>&1
echo "1. ARP & PING" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util s6 tcpdump -i s6-eth1 -w $test_dir/61.pcap 2>&1 &
$m_util s6 tcpdump -i s6-eth2 -w $test_dir/62.pcap 2>&1 &
$m_util s6 tcpdump -i s6-eth3 -w $test_dir/63.pcap 2>&1 &
$m_util h11 tcpdump -i h11-eth0 -w $test_dir/insptest1.pcap 2>&1 &
$m_util h1 ping 100.0.0.45 -c 10 >> /home/sdn/Desktop/2/results/service.log 2>&1 
pkill tcp
killall tcp
python3 $test_dir/analyzer1.py
sleep 5

echo "2. HTTP POST" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util s6 tcpdump -i s6-eth1 -w $test_dir/61.pcap 2>&1 &
$m_util s6 tcpdump -i s6-eth2 -w $test_dir/62.pcap 2>&1 &
$m_util s6 tcpdump -i s6-eth3 -w $test_dir/63.pcap 2>&1 &
$m_util h11 tcpdump -i h11-eth0 -w $test_dir/insptest2.pcap 2>&1 &
$m_util h1 timeout 20 curl 100.0.0.45 -X POST -v -d 'user=foo' >> /home/sdn/Desktop/2/results/service.log 2>&1
pkill tcp
killall tcp
python3 $test_dir/analyzer2.py
sleep 5

echo "3. HTTP PUT" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util s6 tcpdump -i s6-eth1 -w $test_dir/61.pcap 2>&1 &
$m_util s6 tcpdump -i s6-eth2 -w $test_dir/62.pcap 2>&1 &
$m_util s6 tcpdump -i s6-eth3 -w $test_dir/63.pcap 2>&1 &
$m_util h11 tcpdump -i h11-eth0 -w $test_dir/insptest3.pcap 2>&1 &
$m_util h1 timeout 20 curl 100.0.0.45 -X PUT -v -d 'HelloWorld' >> /home/sdn/Desktop/2/results/service.log 2>&1
pkill tcp
python3 $test_dir/analyzer3.py
sleep 5

echo "ips TEST : Blocked packets" >> /home/sdn/Desktop/2/results/service.log 2>&1
echo "4. HTTP PUT injection" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util s6 tcpdump -i s6-eth1 -w $test_dir/61.pcap 2>&1 &
$m_util s6 tcpdump -i s6-eth2 -w $test_dir/62.pcap 2>&1 &
$m_util s6 tcpdump -i s6-eth3 -w $test_dir/63.pcap 2>&1 &
$m_util h11 tcpdump -i h11-eth0 -w $test_dir/insptest4.pcap 2>&1 &
$m_util h1 timeout 15 curl 100.0.0.45 -X PUT -v -d \"cat /etc/passwd\" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 15 curl 100.0.0.45 -X PUT -v -d \"cat /home/sdn/Desktop/2/results/\" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 15 curl 100.0.0.45 -X PUT -v -d 'INSERT' >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 15 curl 100.0.0.45 -X PUT -v -d 'UPDATE' >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 15 curl 100.0.0.45 -X PUT -v -d 'DELETE' >> /home/sdn/Desktop/2/results/service.log 2>&1
kill tcp
python3 $test_dir/analyzer4.py
sleep 5

echo "5. HTTP GET" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util s6 tcpdump -i s6-eth1 -w $test_dir/61.pcap 2>&1 &
$m_util s6 tcpdump -i s6-eth2 -w $test_dir/62.pcap 2>&1 &
$m_util s6 tcpdump -i s6-eth3 -w $test_dir/63.pcap 2>&1 &
$m_util h11 tcpdump -i h11-eth0 -w $test_dir/insptest5.pcap 2>&1 &
$m_util h1 timeout 20 wget -O - 100.0.0.45 >> /home/sdn/Desktop/2/results/service.log 2>&1
pkill tcp
python3 $test_dir/analyzer5.py

#============================================================================

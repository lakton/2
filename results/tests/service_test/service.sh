m_util="/home/sdn/Desktop/mininet/util/m"
test_dir="/home/sdn/Desktop/2/results/tests/service_test"

# Clear or create log files
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
# DNS SERVER TEST
# H1
echo "h1 digging 100.0.0.25 for sdnithub1.ru" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 11 dig @100.0.0.25 sdnithub1.ru >> /home/sdn/Desktop/2/results/servicedns.log 2>&1
sleep 11
# H2
echo "h2 digging 100.0.0.25 for sdnithub2.ru" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h2 timeout 11 dig @100.0.0.25 sdnithub2.ru >> /home/sdn/Desktop/2/results/servicedns.log 2>&1
sleep 11
# H3
echo "h3 digging 100.0.0.25 for sdnithub3.ru" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h3 timeout 11 dig @100.0.0.25 sdnithub3.ru >> /home/sdn/Desktop/2/results/servicedns.log 2>&1
sleep 11
# H4
echo "h4 digging 100.0.0.25 for sdnithub1.ru" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h4 timeout 11 dig @100.0.0.25 sdnithub1.ru >> /home/sdn/Desktop/2/results/servicedns.log 2>&1
sleep 11
python3 $test_dir/servdnschecker.py

#============================================================================
# WWW SERVER TEST
echo "h1 curl sdnithub.ru" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 11 curl sdnithub1.ru -s -X POST -v >> /home/sdn/Desktop/2/results/servicewww.log 2>&1
sleep 11
echo "h2 curl sdnithub.ru" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h2 timeout 11 curl sdnithub2.ru -s -X POST -v >> /home/sdn/Desktop/2/results/servicewww.log 2>&1
sleep 11
echo "h3 curl sdnithub.ru" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h3 timeout 11 curl sdnithub3.ru -s -X POST -v >> /home/sdn/Desktop/2/results/servicewww.log 2>&1
sleep 11
echo "h4 curl sdnithub.ru" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h4 timeout 11 curl sdnithub1.ru -s -X POST -v >> /home/sdn/Desktop/2/results/servicewww.log 2>&1
sleep 11
python3 $test_dir/servwwwchecker.py

#============================================================================
# WWW LB ROUND ROBIN TEST
echo "WWW LB ROUND ROBIN TEST" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util lb2 tcpdump -i lb2-eth1 -w $test_dir/71.pcap 2>&1 &
$m_util lb2 tcpdump -i lb2-eth2 -w $test_dir/72.pcap 2>&1 &
$m_util h1 timeout 10 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
sleep 11
$m_util h1 timeout 10 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
sleep 11
$m_util h1 timeout 10 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
sleep 11
$m_util h1 timeout 10 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
sleep 11
$m_util h1 timeout 10 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
sleep 11
$m_util h1 timeout 10 curl 100.0.0.45 -X POST -s -v >> /home/sdn/Desktop/2/results/service.log 2>&1
pkill tcpdump
python3 $test_dir/rrdnschecker.py

#============================================================================
# IPS TEST

echo "ips TEST : Allowed packets" >> /home/sdn/Desktop/2/results/service.log 2>&1
echo "1. ARP & PING" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util ips tcpdump -i ips-eth1 -w $test_dir/61.pcap 2>&1 &
$m_util ips tcpdump -i ips-eth2 -w $test_dir/62.pcap 2>&1 &
$m_util ips tcpdump -i ips-eth3 -w $test_dir/63.pcap 2>&1 &
$m_util insp tcpdump -i insp-eth0 -w $test_dir/insptest1.pcap 2>&1 &
$m_util h1 ping 100.0.0.45 -c 10 >> /home/sdn/Desktop/2/results/service.log 2>&1
pkill tcpdump
python3 $test_dir/analyzer1.py
sleep 5

echo "2. HTTP POST" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util ips tcpdump -i ips-eth1 -w $test_dir/61.pcap 2>&1 &
$m_util ips tcpdump -i ips-eth2 -w $test_dir/62.pcap 2>&1 &
$m_util ips tcpdump -i ips-eth3 -w $test_dir/63.pcap 2>&1 &
$m_util insp tcpdump -i insp-eth0 -w $test_dir/insptest2.pcap 2>&1 &
$m_util h1 timeout 11 curl 100.0.0.45 -X POST -v -d 'user=foo' >> /home/sdn/Desktop/2/results/service.log 2>&1
pkill tcpdump
python3 $test_dir/analyzer2.py
sleep 5

echo "3. HTTP PUT" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util ips tcpdump -i ips-eth1 -w $test_dir/61.pcap 2>&1 &
$m_util ips tcpdump -i ips-eth2 -w $test_dir/62.pcap 2>&1 &
$m_util ips tcpdump -i ips-eth3 -w $test_dir/63.pcap 2>&1 &
$m_util insp tcpdump -i insp-eth0 -w $test_dir/insptest3.pcap 2>&1 &
$m_util h1 timeout 11 curl 100.0.0.45 -X PUT -v -d 'HelloWorld' >> /home/sdn/Desktop/2/results/service.log 2>&1
pkill tcpdump
python3 $test_dir/analyzer3.py
sleep 5

echo "ips TEST : Blocked packets" >> /home/sdn/Desktop/2/results/service.log 2>&1
echo "4. HTTP PUT injection" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util ips tcpdump -i ips-eth1 -w $test_dir/61.pcap 2>&1 &
$m_util ips tcpdump -i ips-eth2 -w $test_dir/62.pcap 2>&1 &
$m_util ips tcpdump -i ips-eth3 -w $test_dir/63.pcap 2>&1 &
$m_util insp tcpdump -i insp-eth0 -w $test_dir/insptest4.pcap 2>&1 &
$m_util h1 timeout 11 curl 100.0.0.45 -X PUT -v -d \"cat /etc/passwd\" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 11 curl 100.0.0.45 -X PUT -v -d \"cat /home/sdn/Desktop/2/results/\" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 11 curl 100.0.0.45 -X PUT -v -d 'INSERT' >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 11 curl 100.0.0.45 -X PUT -v -d 'UPDATE' >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util h1 timeout 11 curl 100.0.0.45 -X PUT -v -d 'DELETE' >> /home/sdn/Desktop/2/results/service.log 2>&1
pkill tcpdump
python3 $test_dir/analyzer4.py
sleep 5

echo "5. HTTP GET" >> /home/sdn/Desktop/2/results/service.log 2>&1
$m_util ips tcpdump -i ips-eth1 -w $test_dir/61.pcap 2>&1 &
$m_util ips tcpdump -i ips-eth2 -w $test_dir/62.pcap 2>&1 &
$m_util ips tcpdump -i ips-eth3 -w $test_dir/63.pcap 2>&1 &
$m_util insp tcpdump -i insp-eth0 -w $test_dir/insptest5.pcap 2>&1 &
$m_util h1 timeout 11 wget -O - 100.0.0.45 >> /home/sdn/Desktop/2/results/service.log 2>&1
pkill tcpdump
python3 $test_dir/analyzer5.py

#============================================================================

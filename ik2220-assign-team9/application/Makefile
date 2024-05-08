app:
	@sudo python3 /home/sdn/Desktop/SDN-NFV/applications/sdn/pox.py  /home/sdn/Desktop/2/ik2220-assign-team9/application/sdn/controller.py samples.pretty_log log.level --DEBUG >> /var/log/pox.log 2>&1 &
	@sudo /home/sdn/Desktop/fastclick/bin/click -f nfv/ips.click >> /var/log/ipsclick.log 2>&1 &
	@sudo /home/sdn/Desktop/fastclick/bin/click -f nfv/dns.click >> /var/log/dnsclick.log 2>&1 &
	@sudo /home/sdn/Desktop/fastclick/bin/click -f nfv/www.click >> /var/log/wwwclick.log 2>&1 &
	@sudo /home/sdn/Desktop/fastclick/bin/click -f nfv/nat.click >> /var/log/natclick.log 2>&1 &

clean:
	@sudo pkill pox
	@sudo killall click
	@sudo mn -c
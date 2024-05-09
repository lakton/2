app:
		@sudo python3 /home/sdn/Desktop/2/ik2220-assign-team9/application/sdn/pox.py controller samples.pretty_log log.level --DEBUG >> /var/log/pox.log 2>&1 & \
		@sudo /home/sdn/Desktop/fastclick/bin/click -f /home/sdn/Desktop/2/ik2220-assign-team9/application/nfv/ips.click >> /var/log/ipsclick.log 2>&1 
		@sudo /home/sdn/Desktop/fastclick/bin/click -f /home/sdn/Desktop/2/ik2220-assign-team9/application/nfv/dns.click >> /var/log/dnsclick.log 2>&1 
		@sudo /home/sdn/Desktop/fastclick/bin/click -f /home/sdn/Desktop/2/ik2220-assign-team9/application/nfv/www.click >> /var/log/wwwclick.log 2>&1 
		@sudo /home/sdn/Desktop/fastclick/bin/click -f /home/sdn/Desktop/2/ik2220-assign-team9/application/nfv/nat.click >> /var/log/natclick.log 2>&1 

clean:
		@echo -n "[MAKE] Killing POX..      " 
		@(sudo kill -s SIGINT $$(ps aux | grep pox | grep root | head -n 1 | awk '{print $$2}') 2>/dev/null  && echo "OK") || echo "POX not running!"
		@echo -n "[MAKE] Killing Click..    "
		@sudo pkill --signal SIGINT click && echo "OK" || echo "Click not running!"
		@echo -n "[MAKE] Killing SDN App..  "
		@(sudo kill -s SIGTERM $$(ps aux | grep sdn | grep root | head -n 1 | awk '{print $$2}')  2>/dev/null && echo "OK") || echo "SDN not running!"
		@sudo mn -c

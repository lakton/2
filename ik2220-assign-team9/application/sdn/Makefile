app:
	@sudo python3 pox.py controller samples.pretty_log log.level --DEBUG >> /var/log/pox.log 2>&1 &
clean:
	@sudo pkill pox
	@sudo killall click
	@sudo mn -c
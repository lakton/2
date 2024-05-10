from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Switch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import OVSSwitch
from mininet.node import RemoteController

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        # public zone
        sw1 = self.addSwitch( 'sw1', dpid ='1')
        h1 = self.addHost( 'h1', ip='100.0.0.10/24' )
        h2 = self.addHost( 'h2', ip='100.0.0.11/24' )
        fw1 = self.addSwitch( 'fw1', dpid = '2')

        # dmz
        sw2 = self.addSwitch( 'sw2', dpid ='3' )
        lb1 = self.addSwitch( 'lb1' , dpid ='4')
        sw3 = self.addSwitch( 'sw3', dpid ='5' )
        ips = self.addSwitch( 'ips' , dpid ='6')
        insp = self.addHost( 'insp', ip='100.0.0.30/24' )
        lb2 = self.addSwitch( 'lb2', dpid ='7' )
        sw4 = self.addSwitch( 'sw4' , dpid ='8')
        ds1 = self.addHost( 'ds1', ip='100.0.0.20/24' )
        ds2 = self.addHost( 'ds2', ip='100.0.0.21/24' )
        ds3 = self.addHost( 'ds3', ip='100.0.0.22/24' )
        ws1 = self.addHost( 'ws1', ip='100.0.0.40/24' )
        ws2 = self.addHost( 'ws2', ip='100.0.0.41/24' )
        ws3 = self.addHost( 'ws3', ip='100.0.0.42/24' )

        # private
        fw2 = self.addSwitch( 'fw2', dpid = '9')
        napt = self.addSwitch( 'napt' , dpid ='10')
        sw5 = self.addSwitch( 'sw5' , dpid ='11')
        h3 = self.addHost( 'h3', ip='10.0.0.50/24' )
        h4 = self.addHost( 'h4', ip='10.0.0.51/24' )

        # public link
        self.addLink( h1, sw1 )
        self.addLink( h2, sw1 )

        # middle public
        self.addLink( fw1, sw1 )
        self.addLink( fw1, sw2 )

        # dmz link
        self.addLink( sw2, lb1 )
        self.addLink( sw3, lb1 )
        self.addLink( sw2, ips )
        self.addLink( ips, lb2 )
        self.addLink( ips, insp )
        self.addLink( lb2, sw4 )
        self.addLink( sw3, ds1 )
        self.addLink( sw3, ds2 )
        self.addLink( sw3, ds3 )
        self.addLink( sw4, ws1 )
        self.addLink( sw4, ws2 )
        self.addLink( sw4, ws3 )

        # middle private
        self.addLink( sw2, fw2 )
        self.addLink( fw2, napt )
        self.addLink( napt, sw5 )

        # private link
        self.addLink( sw5, h3 )
        self.addLink( sw5, h4 )

if __name__ == "__main__":
    # Создание удаленного контроллера
    ctrl1 = RemoteController('c0', ip='192.168.200.101', port=6633)
    # Установка уровня логирования
    setLogLevel('info')
    # Создание экземпляра топологии
    topo = MyTopo()
    # Создание сети Mininet
    net = Mininet(
        topo=topo,
        switch=OVSSwitch,
        controller=ctrl1,
        autoSetMacs=True
    )
    # Добавление маршрута для хостов h3 и h4
    net.get("h3").cmd("route add default gw 10.0.0.1 h3-eth0")
    net.get("h4").cmd("route add default gw 10.0.0.1 h4-eth0")
    net.get("ds1").cmd("route add default gw 100.0.0.25 ds1-eth0")
    net.get("ds2").cmd("route add default gw 100.0.0.25 ds2-eth0")
    net.get("ds3").cmd("route add default gw 100.0.0.25 ds3-eth0")
    net.get("ds1").cmd("python3 /home/sdn/Desktop/2/application/sdn/ext/dns_server20.py &")
    net.get("ds1").cmd("python3 /home/sdn/Desktop/2/application/sdn/ext/dns_server21.py &")
    net.get("ds3").cmd("python3 /home/sdn/Desktop/2/application/sdn/ext/dns_server22.py &")
    net.get("ws1").cmd("route add default gw 100.0.0.45 ws1-eth0")
    net.get("ws2").cmd("route add default gw 100.0.0.45 ws2-eth0")
    net.get("ws3").cmd("route add default gw 100.0.0.45 ws3-eth0")
    net.get("ws1").cmd("python3 -m SimpleHTTPServer 80 >> /tmp/http.log &")
    net.get("ws2").cmd("python3 -m SimpleHTTPServer 80 >> /tmp/http.log &")
    net.get("ws3").cmd("python3 -m SimpleHTTPServer 80 >> /tmp/http.log &")
    net.get("h1").cmd("cp /dev/null /etc/resolv.conf")
    net.get("h1").cmd("echo 'nameserver 100.0.0.25' > /etc/resolv.conf")
    # Запуск сети
    net.start()
    CLI(net)  # Запуск интерактивной консоли Mininet




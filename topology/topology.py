from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        # public zone
        sw1 = self.addSwitch( 'sw1' )
        h1 = self.addHost( 'h1', ip='100.0.0.10/24' )
        h2 = self.addHost( 'h2', ip='100.0.0.11/24' )
        fw1 = self.addSwitch( 'fw1' )

        # dmz
        sw2 = self.addSwitch( 'sw2' )
        lb1 = self.addSwitch( 'lb1' )
        sw3 = self.addSwitch( 'sw3' )
        ips = self.addSwitch( 'ips' )
        insp = self.addHost( 'insp', ip='100.0.0.30/24' )
        lb2 = self.addSwitch( 'lb2' )
        sw4 = self.addSwitch( 'sw4' )
        ds1 = self.addHost( 'ds1', ip='100.0.0.20/24' )
        ds2 = self.addHost( 'ds2', ip='100.0.0.21/24' )
        ds3 = self.addHost( 'ds3', ip='100.0.0.22/24' )
        ws1 = self.addHost( 'ws1', ip='100.0.0.40/24' )
        ws2 = self.addHost( 'ws2', ip='100.0.0.41/24' )
        ws3 = self.addHost( 'ws3', ip='100.0.0.42/24' )

        # private
        fw2 = self.addSwitch( 'fw2' )
        napt = self.addSwitch( 'napt' )
        sw5 = self.addSwitch( 'sw5' )
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

topos = { 'mytopo': ( lambda: MyTopo() ) }

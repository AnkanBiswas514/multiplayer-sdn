
from mininet.topo import Topo

class GameTopo(Topo):
    def build(self):
        server = self.addHost('h1', ip='10.0.0.1/24')
        player1 = self.addHost('h2', ip='10.0.0.2/24')
        player2 = self.addHost('h3', ip='10.0.0.3/24')

        s1 = self.addSwitch('s1', protocols='OpenFlow13')

        self.addLink(server, s1)
        self.addLink(player1, s1)
        self.addLink(player2, s1)

topos = {'game': lambda: GameTopo()}

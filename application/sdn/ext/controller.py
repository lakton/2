"""
learning switch and firewall 
https://www.coursera.org/course/sdn1
http://kickstartsdn.com/
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.util import str_to_bool
import time

from pox.lib.addresses import EthAddr
from pox.lib.addresses import IPAddr
from pox.lib.packet import *

log = core.getLogger()

HARD_TIMEOUT = 30
IDLE_TIMEOUT = 30

flood_delay = 0
i = 0
#flag = 0

class LearningFirewall (EventMixin):
    def __init__(self, connection, transparent):
        # Коммутатор, к которому мы будем добавлять возможности обучающегося L2-коммутатора
        self.macToPort = {}
        self.connection = connection
        self.transparent= transparent
        self.listenTo(connection)
        self.firewall = {}
        self.flag = 0
        self.hold_down_expired = flood_delay == 0
        self.stateful = {}

    def AddRule(self, dpidstr, dst=0, dst_port=0, value=True):
        self.firewall[(dpidstr, dst, dst_port, )] = value
        log.debug("Добавление правила брандмауэра в %s: %s %s", dpidstr, dst, dst_port)

    def CheckRule(self, dpidstr, dst=0, dst_port=0):
        try:
            entry = self.firewall[(dpidstr, dst, dst_port)]
            if entry == True:
                log.debug("Правило %s найдено в %s-%s: FORWARD", dst, dpidstr, dst_port)
            else:
                log.debug("Правило %s найдено в %s- %s: DROP", dst, dpidstr, dst_port)
                return entry
        except KeyError:
            log.debug("Правило %s !НЕ! найдено в %s-%s: DROP", dst, dpidstr, dst_port)
            return False

    def _handle_PacketIn(self, event):
        global i
        # разбор входного пакета
        packet = event.parse()

        def flood(message=None):
            msg = of.ofp_packet_out()
            if time.time() - self.connection.connect_time >= flood_delay:
                if self.hold_down_expired is False:
                    self.hold_down_expired = True
                    log.info("%s: Истек срок удержания флуда - флудим", event.dpid)
                if message is not None:
                    log.debug(message)
                msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            else:
                pass
            msg.data = event.ofp
            msg.in_port = event.port
            self.connection.send(msg)

        def drop(duration=None):
            if duration is not None:
                if not isinstance(duration, tuple):
                    duration = (duration, duration)
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet)
                msg.idle_timeout = duration[0]
                msg.hard_timeout = duration[1]
                msg.buffer_id = event.ofp_buffer_id
                self.connection.send(msg)
            elif event.ofp.buffer_id is not None:
                msg = of.ofp_packet_out()
                msg.buffer_id = event.ofp.buffer_id
                msg.in_port = event.port
                self.connection.send(msg)

        # обновление сопоставления mac и порта
        self.macToPort[packet.src] = event.port
        dpidstr = dpidToStr(event.connection.dpid)
        arp = packet.find('arp')
        if arp is not None:
            print("arp not none")
            # log.debug("%s"%arp.protodst)
            if arp.protodst in [IPAddr('100.0.0.20'), IPAddr('100.0.0.21'), IPAddr('100.0.0.22'), IPAddr('100.0.0.40'),
                                IPAddr('100.0.0.41'), IPAddr('100.0.0.42'), IPAddr('100.0.0.30')]:
                print("Destination Host Unreachable")
                return

        ip = packet.find('ipv4')
        if ip is not None:
            udp = ip.find('udp')
            if udp is not None:
                self.stateful[i] = (ip.id, ip.srcip, ip.dstip, udp.srcport, udp.dstport)
                i = i + 1
                log.debug("ЭТО UDP")
                if self.CheckRule(dpidstr, packet.dst, udp.dstport) == False and self.CheckRule(dpidstr, packet.src,
                                                                                               udp.srcport) == False:
                    log.debug("Устройство %s и его IP-назначения: %s-%s" % (
                    dpidstr, packet.dst, udp.dstport))
                    drop()
                    self.flag = 1
                    return

            tcp = ip.find('tcp')
            if tcp is not None:
                self.stateful[i] = (ip.id, ip.srcip, ip.dstip, tcp.srcport, tcp.dstport)
                i = i + 1
                log.debug("ЭТО TCP")

                if self.CheckRule(dpidstr, packet.dst, tcp.dstport) == False and self.CheckRule(dpidstr, packet.src,
                                                                                               tcp.srcport) == False:
                    log.debug("Устройство %s и его IP-назначения: %s-%s" % (
                    dpidstr, packet.dst, tcp.dstport))
                    drop()
                    self.flag = 1
                    return
            icmp = ip.find('icmp')
            if icmp is not None:
                self.stateful[i] = (ip.id, ip.srcip, ip.dstip, icmp.code, icmp.type)
                i = i + 1
                log.debug('icmp is not none %s' % icmp.type)
                if self.CheckRule(dpidstr, packet.dst, icmp.type) == False:
                    log.debug("Устройство %s и его IP-назначения: %s-%s" % (
                    dpidstr, packet.dst, icmp.type))
                    drop()
                    self.flag = 1
                    return

        else:
            icmp = packet.find('icmp')
            if icmp is not None:
                # self.stateful[i] = (icmp.type, icmp.srcip, icmp.dstip, udp.srcport,udp.dstport)
                i = i + 1
                log.debug('icmp is not none %s' % icmp.type)
                if self.CheckRule(dpidstr, packet.dst, icmp.type) == False:
                    log.debug("Устройство %s и его IP-назначения: %s-%s" % (
                    dpidstr, packet.dst, icmp.type))
                    drop()
                    self.flag = 1
                    return

        if self.flag == 1:
            return
        if not self.transparent:
            if packet.type == packet.LLDP_TYPE or packet.type == 0x86DD:
                drop()
                return

        if packet.dst.is_multicast:
            flood()
        else:
            if packet.dst not in self.macToPort:
                flood("Порт для %s неизвестен -- флудим" % (packet.dst,))
            else:
                # installing flow
                outport = self.macToPort[packet.dst]
                if outport == event.port:
                    log.warning("Тот же порт для пакета от %s -> %s на %s. Drop." %
                                (packet.src, packet.dst, outport), dpidToStr(event.dpid))
                    return
                log.debug("Установка потока(flow) для %s.%i -> %s.%i" % (packet.src, event.port, packet.dst, outport))
                log.debug("Это dpid %s" % dpidToStr(event.dpid))
                msg = of.ofp_flow_mod()
                msg.match.dl_src = packet.src
                msg.match.dl_dst = packet.dst
                msg.idle_timeout = IDLE_TIMEOUT
                msg.hard_timeout = HARD_TIMEOUT
                msg.actions.append(of.ofp_action_output(port=outport))
                msg.buffer_id = event.ofp.buffer_id
                self.connection.send(msg)


class LearningFirewall1(LearningFirewall):
    def __init__(self, connection, transparent):
        super().__init__(connection, transparent)
        # правила доступа к демилитаризованной зоне и частной зоне:
        # Доступны следующие службы: 
        # a) dns-сервер по адресу 100.0.0.25:53 
        # b) http-сервер по адресу 100.0.0.45:80 
        # c) icmp ping-запрос и ответ на виртуальные ip этих серверов.
        # dns и http сервер ping запрос-ответ
        self.AddRule('00-00-00-00-00-02', EthAddr('0a:b9:f7:7e:59:6b'), 8, True)
        self.AddRule('00-00-00-00-00-02', EthAddr('00:00:00:00:00:02'), 0, True)
        self.AddRule('00-00-00-00-00-02', EthAddr('92:4a:f4:04:75:54'), 8, True)
        self.AddRule('00-00-00-00-00-02', EthAddr('00:00:00:00:00:01'), 0, True)
        # остальное генерирует ошибку icmp, если DmZ пингуется

        # dns сервер udp запрос на 53 порт.
        self.AddRule('00-00-00-00-00-02', EthAddr('0a:b9:f7:7e:59:6b'), 53, True)

        # http сервер tcp запрос на порт 80
        self.AddRule('00-00-00-00-00-02', EthAddr('92:4a:f4:04:75:54'), 80, True)

        # пингование хоста с хостом
        self.AddRule('00-00-00-00-00-02', EthAddr('00:00:00:00:00:01'), 8, True)
        self.AddRule('00-00-00-00-00-02', EthAddr('00:00:00:00:00:02'), 8, True)
        self.AddRule('00-00-00-00-00-02', EthAddr('fa:dd:38:74:98:c8'), 0, True)
        self.AddRule('00-00-00-00-00-02', EthAddr('fa:dd:38:74:98:c8'), 8, True)
        self.AddRule('00-00-00-00-00-02', EthAddr('00:00:00:00:00:01'), 0, True)
        self.AddRule('00-00-00-00-00-02', EthAddr('00:00:00:00:00:02'), 0, True)

        self.AddRule('00-00-00-00-00-02', EthAddr('00:00:00:00:00:05'), 8, False)

    def _handle_PacketIn(self, event):
        log.debug("Правила для брандмауэра 1.")
        super()._handle_PacketIn(event)


class LearningFirewall2(LearningFirewall):
    def __init__(self, connection, transparent):
        super().__init__(connection, transparent)
        # правила доступа к демилитаризованной зоне и частной зоне:
        # Доступны следующие службы: 
        # a) dns-сервер по адресу 100.0.0.25:53 
        # b) http-сервер по адресу 100.0.0.45:80 
        # c) icmp ping-запрос и ответ на виртуальные ip этих серверов.
        # dns и http сервер ping запрос-ответ
        self.AddRule('00-00-00-00-00-09', EthAddr('0a:b9:f7:7e:59:6b'), 8, True)
        self.AddRule('00-00-00-00-00-09', EthAddr('0a:b9:f7:7e:59:6b'), 0, True)
        self.AddRule('00-00-00-00-00-09', EthAddr('92:4a:f4:04:75:54'), 8, True)
        self.AddRule('00-00-00-00-00-09', EthAddr('92:4a:f4:04:75:54'), 0, True)
        # остальное генерирует ошибку icmp, если DmZ пингуется

        # dns сервер udp запрос на 53 порт.
        self.AddRule('00-00-00-00-00-09', EthAddr('0a:b9:f7:7e:59:6b'), 53, True)

        # http сервер tcp запрос на порт 80
        self.AddRule('00-00-00-00-00-09', EthAddr('92:4a:f4:04:75:54'), 80, True)

        # пингование хоста с хостом
        self.AddRule('00-00-00-00-00-09', EthAddr('0a:b9:f7:7e:59:6b'), 8, True)
        self.AddRule('00-00-00-00-00-09', EthAddr('92:4a:f4:04:75:54'), 8, True)

        self.AddRule('00-00-00-00-00-09', EthAddr('00:00:00:00:00:05'), 8, False)

    def _handle_PacketIn(self, event):
        log.debug("Правила для брандмауэра 2.")
        super()._handle_PacketIn(event)


class LearningSwitch(EventMixin):

    def __init__(self):
        self.macToPort = {}
        self.listenTo(core.openflow)

    def _handle_ConnectionUp(self, event):
        log.debug("Connection %s" % (event.connection,))
        LearningSwitch1(event.connection, False)


def launch():
    core.registerNew(LearningSwitch)


class LearningSwitch1 (EventMixin):
    def __init__(self, connection, transparent):
        # Коммутатор, к которому мы будем добавлять возможности обучающегося L2-коммутатора
        self.macToPort = {}
        self.connection = connection
        self.listenTo(connection)
        self.transparent = transparent
        self.firewall = {}

    def AddRule(self, dpidstr, dst=0, dst_port=0, value=True):
        self.firewall[(dpidstr, dst, dst_port, )] = value
        log.debug("Добавление правила брандмауэра в %s: %s %s", dpidstr, dst, dst_port)

    def CheckRule(self, dpidstr, dst=0, dst_port=0):
        try:
            entry = self.firewall[(dpidstr, dst, dst_port)]
            if entry == True:
                log.debug("Правило %s найдено в %s-%s: ПРОХОД", dst, dpidstr, dst_port)
            else:
                log.debug("Правило %s найдено в %s- %s: ОТБРОС", dst, dpidstr, dst_port)
                return entry
        except KeyError:
            log.debug("Правило %s НЕ найдено в %s-%s: ОТБРОС", dst, dpidstr, dst_port)
            return False

    def _handle_PacketIn(self, event):
        # разбор входящего пакета
        packet = event.parsed
        # обновление отображения MAC-адресов на порты
        self.macToPort[packet.src] = event.port
        dpidstr = dpidToStr(event.connection.dpid)
        arp = packet.find('arp')
        if arp is not None:
            # log.debug("%s"%arp.protodst)
            if arp.protodst in [IPAddr('100.0.0.20'), IPAddr('100.0.0.21'), IPAddr('100.0.0.22'), IPAddr('100.0.0.40'),
                                IPAddr('100.0.0.41'), IPAddr('100.0.0.42'), IPAddr('100.0.0.30')]:
                print("Destination Host Unreachable")
                return

        if packet.dst.is_multicast:
            flood()
        else:
            if packet.dst not in self.macToPort:
                flood("Порт для %s неизвестен -- флудим" % (packet.dst,))
            else:
                # установка потока
                outport = self.macToPort[packet.dst]
                if outport == event.port:
                    log.warning("Тот же порт для пакета от %s -> %s на %s. Drop." %
                                (packet.src, packet.dst, outport), dpidToStr(event.dpid))
                    return
                log.debug("Установка потока(flow) для %s.%i -> %s.%i" % (packet.src, event.port, packet.dst, outport))
                log.debug("Это dpid %s" % dpidToStr(event.dpid))
                msg = of.ofp_flow_mod()
                msg.match.dl_src = packet.src
                msg.match.dl_dst = packet.dst
                msg.idle_timeout = IDLE_TIMEOUT
                msg.hard_timeout = HARD_TIMEOUT
                msg.actions.append(of.ofp_action_output(port=outport))
                msg.buffer_id = event.ofp.buffer_id
                self.connection.send(msg)

                
class learning_switch(EventMixin):
    def __init__(self, transparent):
        super().__init__()
        self.listenTo(core.openflow)
        self.transparent = transparent

    def _handle_ConnectionUp(self, event):
        log.debug("Connection %s" % (event.connection,))
        if event.dpid in [2, 9]:
            log.debug("Брандмауэры подключаются")
            if event.dpid == 2:
                log.debug("Брандмауэр 1 подключен")
                LearningFirewall1(event.connection, self.transparent)
            else:
                log.debug("Брандмауэр 2 подключен")
                LearningFirewall2(event.connection, self.transparent)
        elif event.dpid in [1, 3, 5, 8, 11]:
            log.debug("Коммутаторы подключены")
            LearningSwitch(event.connection, False)
        else:
            log.debug("(Fast)Click подключен")
            # DOING NOTHING

    def _handle_ConnectionDown(self, event):
        # ConnectionDown(event.connection,event.dpid)
        log.info("Коммутатор %s выключен.", dpidToStr(event.dpid))


def launch(transparent=False, hold_down=flood_delay):
    # Запускает коммутатор L2 с обучением.
    try:
        global flood_delay
        flood_delay = int(str(hold_down), 10)
        assert flood_delay >= 0
    except:
        raise RuntimeError("Ожидалось, что задержка будет числом")
    core.registerNew(learning_switch, str_to_bool(transparent))


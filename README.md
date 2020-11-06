# Mise en œuvre des fonctionnalités de sécurité réseau d'un switch

[[_TOC_]]

## Todos

* Configuration de deux serveurs DHCP (Légitime, Pirate)
    * [x] (A) Serveur légitime
    * [x] (A) Serveur attaquant
* 4 scénarios d'attaques
    * [ ] (G) CAM Flooding (script Python)
    * [x] (A) DHCP Snooping
    * [ ] (B) Port Stealing (script Python)
    * [x] ARP Spoofing (script Python)
* 3 mise en place de protection
    * [ ] (G,B) Port security
    * [x] (A) DHCP Snooping
    * [ ] Dynamic ARP inspection
* Pour chaque scénarios
    * [ ] Difficulté de mise en place
    * [ ] Description
    * [ ] GIF et vérificiations

## Tableau d'addressage

| Name     | IP            | Gateway      | Description |
|----------|---------------|--------------|-------------|
| VM1      | 192.168.33.1  | -            | Gateway     |
| VM2      | 192.168.33.10 | 192.168.33.1 | Victime     |
| Attacker | 192.168.33.11 | 192.168.33.1 | Attaquant   |

## Schéma d'infrastructure

![](./images/schema.png)

## 3.1 CAM Flooding, port-stealing et mise en œuvre de contre-mesures

### Rappels théoriques

#### Table CAM (Content Addressable Memory)

Table de référence d'un Switch qui fait la relation entre une adresse MAC et un numéro de port, et contient également les paramètres VLAN associés.

#### CAM Flooding Attack / Attaque par saturation

L'attaque exploite les limitations matérielles et de mémoire de la table CAM du Switch. Elle consiste à envoyer de (très) nombreuses trames Ethernet au Switch. Chaque trame envoyée possède une adresse MAC source différente (généralement erronnée), dans le but de remplir l'intégralité de l'espace disponible de la table CAM.

Une fois la table remplie, le trafic réseau est flood sur tous les ports car étant donné que la table CAM ne peut plus stocker d'adresses MAC, elle n'est plus en mesure de déterminer quelle adresse MAC de destination correspond à quel paquet envoyé. Le Switch agit alors comme un Hub.

#### Port stealing Attack / Attaque par vol de port 

L'attaquant utilise l'adresse MAC de la victime pour garnir la table CAM du Switch avec le couple :
- Adresse MAC de la Victime
- Port de la machine de l'attaquant

Ainsi l'attaquant recevra tous les paquets destinés à la victime puisque le Switch pensera alors qu'il transmet lesdits paquets à la victime (puisqu'utilisant le port renseigné par l'attaquant.)

#### CAM Flooding à l'aide de scapy

Afin de réaliser ce scénario d'attaque, il suffira simplement d'avoir une machine
dans le lan et relié au switch que l'on veut corrompre et transformer en hub. A la suite
de l'attaque, le switch enverra tout l'incoming trafic sur tous les ports sans chercher
à faire de correspondance, exactement comme le ferait un hub.

Le bout de code python se trouve ici : [scripts/cam_flooding.py](scripts/cam_flooding.py)

* 1 er terminal
```
scp cam_flooding.py user@10.1.1.204:/home/user/
ssh user@10.1.1.204
```

* 2 ème terminal
```
telnet 10.1.1.189:32771
SW2> enable
```

* Résultat final
![cam_flooding_proof](./images/cam_flooding.gif)

## 3.2 Mise en œuvre de la mesure de protection DHCP snooping

### Insertion d'un rogue DHCP server sur un réseau local

On insert un autre serveur DHCP sur le réseau local qui répondra plus rapidement
que le serveur DHCP légitime. En conséquence les clients reçevront la configuration
de l'attaquant. Lui permettant ainsi de rediriger le traffic des clients vers lui,
en changeant la gateway du bail DHCP. Il peut ensuite forward tout le traffic à la
gateway légitime, pour devenir homme du milieu.

### Configuration des serveurs DHCP

Pour réaliser le scénario d'attaque, nous allons configurer deux serveurs DHCP.
Un sur la VM1 qui sera notre serveur légitime, l'autre sur l'attaquant.
Pour que l'attaquant réponde plus rapidement nous l'avons branché sur le deuxième
switch, comme dans le schéma suivant:

![](./images/dhcp.png)

* https://linuxhint.com/dhcp_server_centos8/

Configuration du serveur DHCP légitime sur la VM1

* ip statique

```
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"
BOOTPROTO="dhcp"
DEFROUTE="yes"
NAME="ens3"
UUID="2a1f80f8-a2f9-4701-a035-4cad8fdbef0a"
DEVICE="ens3"
ONBOOT="yes"
```

* `/etc/dhcp/dhcpd.conf`

```
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
authoritative;

subnet 192.168.33.0 netmask 255.255.255.0 {
    range 192.168.33.10 192.168.15.200;
    option routers 192.168.33.1;
    option subnet-mask 255.255.255.0;
    option domain-name-servers 1.1.1.1, 8.8.8.8;
}
```

Configuration de l'interface en DHCP sur la VM2

```
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"
BOOTPROTO="dhcp"
DEFROUTE="yes"
NAME="ens3"
UUID="2a1f80f8-a2f9-4701-a035-4cad8fdbef0a"
DEVICE="ens3"
ONBOOT="yes"
```

On recupère bien la configuration DHCP sur la VM2

```
Nov 06 06:14:14 VM2 NetworkManager[798]: <info>  [1604661254.0881] dhcp4 (ens3): activation: beginning transaction (timeout in 45 seconds)
Nov 06 06:14:14 VM2 NetworkManager[798]: <info>  [1604661254.1389] dhcp4 (ens3):   address 192.168.33.10
Nov 06 06:14:14 VM2 NetworkManager[798]: <info>  [1604661254.1389] dhcp4 (ens3):   plen 24
Nov 06 06:14:14 VM2 NetworkManager[798]: <info>  [1604661254.1389] dhcp4 (ens3):   expires in 594 seconds
Nov 06 06:14:14 VM2 NetworkManager[798]: <info>  [1604661254.1390] dhcp4 (ens3):   nameserver '1.1.1.1'
Nov 06 06:14:14 VM2 NetworkManager[798]: <info>  [1604661254.1390] dhcp4 (ens3):   nameserver '8.8.8.8'
Nov 06 06:14:14 VM2 NetworkManager[798]: <info>  [1604661254.1390] dhcp4 (ens3):   gateway 192.168.33.1
```

On ping bien la VM1 depuis la VM2

```
[root@VM2 ~]# ping 192.168.33.1
PING 192.168.33.1 (192.168.33.1) 56(84) bytes of data.
64 bytes from 192.168.33.1: icmp_seq=1 ttl=64 time=4.56 ms
64 bytes from 192.168.33.1: icmp_seq=2 ttl=64 time=11.5 ms
```

Configuration du serveur attaquant

```
ip addr add 192.168.34.1/24 dev ens3
ip addr add 192.168.33.11/24 dev ens3
```

* `/etc/dhcp/dhcpd.conf`

```
default-lease-time 60;
max-lease-time 60;
ddns-update-style none;
authoritative;

subnet 192.168.34.0 netmask 255.255.255.0 {
    range 192.168.34.10 192.168.34.200;
    option routers 192.168.34.1;
    option subnet-mask 255.255.255.0;
    option domain-name-servers 1.1.1.1, 8.8.8.8;
}
```

Notre victime, la VM2 récupère bien l'addresse en 192.168.34.10, dans le réseau de l'attaquant.

```
Nov 06 06:53:51 VM2 NetworkManager[2094]: <info>  [1604663631.4571] device (ens4): state change: ip-config -> ip-check (reason 'none', sys-iface-state: 'assume')
Nov 06 06:53:51 VM2 NetworkManager[2094]: <info>  [1604663631.4577] dhcp4 (ens3):   address 192.168.34.10
Nov 06 06:53:51 VM2 NetworkManager[2094]: <info>  [1604663631.4577] dhcp4 (ens3):   plen 24
Nov 06 06:53:51 VM2 NetworkManager[2094]: <info>  [1604663631.4577] dhcp4 (ens3):   expires in 60 seconds
Nov 06 06:53:51 VM2 NetworkManager[2094]: <info>  [1604663631.4577] dhcp4 (ens3):   nameserver '1.1.1.1'
Nov 06 06:53:51 VM2 NetworkManager[2094]: <info>  [1604663631.4578] dhcp4 (ens3):   nameserver '8.8.8.8'
Nov 06 06:53:51 VM2 NetworkManager[2094]: <info>  [1604663631.4578] dhcp4 (ens3):   gateway 192.168.34.1
Nov 06 06:53:51 VM2 NetworkManager[2094]: <info>  [1604663631.4929] dhcp4 (ens3): state changed expire -> bound
```

On ping internet depuis la victime.

```
[root@VM2 ~]# ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
--- 1.1.1.1 ping statistics ---
```

Il ne passe pas car nous n'avons pas activé le forwarding d'IP.

Il faudrais aussi que le réseau 192.168.34.0/24 soit routé sur internet.

Mais on reçoit bien les pings sur notre serveur attaquant.

```
[root@attacker ~]# tcpdump -i ens3 -n -nn -e src 192.168.34.10
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on ens3, link-type EN10MB (Ethernet), capture size 262144 bytes
06:57:49.640171 00:50:00:00:04:00 > 00:50:00:00:05:00, ethertype IPv4 (0x0800), length 98: 192.168.34.10 > 1.1.1.1: ICMP echo request, id 2339, seq 7, length 64
06:57:50.664248 00:50:00:00:04:00 > 00:50:00:00:05:00, ethertype IPv4 (0x0800), length 98: 192.168.34.10 > 1.1.1.1: ICMP echo request, id 2339, seq 8, length 64
06:57:51.688878 00:50:00:00:04:00 > 00:50:00:00:05:00, ethertype IPv4 (0x0800), length 98: 192.168.34.10 > 1.1.1.1: ICMP echo request, id 2339, seq 9, length 64
06:57:52.712402 00:50:00:00:04:00 > 00:50:00:00:05:00, ethertype IPv4 (0x0800), length 98: 192.168.34.10 > 1.1.1.1: ICMP echo request, id 2339, seq 10, length 64
06:57:53.028359 00:50:00:00:04:00 > 00:50:00:00:05:00, ethertype ARP (0x0806), length 60: Reply 192.168.34.10 is-at 00:50:00:00:04:00, length 46
```

### Mise en oeuvre de DHCP snooping

* Sur le premier switch

```
SW1>enable
SW1#conf t
SW1(config)#ip dhcp snooping
SW1(config)#ip dhcp snooping vlan 1
SW1(config)#int Ethernet0/0
SW1(config-if)#ip dhcp snooping trust
SW1(config-if)#exit
SW1(config)#int Ethernet0/2
SW1(config-if)#ip dhcp snooping trust
SW1(config-if)#exit
SW1(config)#exit
```

* Sur le deuxième switch

```
SW2>enable
SW2#conf t
SW2(config)#ip dhcp snooping
SW2(config)#ip dhcp snooping vlan 1
SW2(config)#int Ethernet0/2
SW2(config-if)#ip dhcp snooping trust
SW2(config-if)#exit
SW2(config)#exit
```

On démare les serveurs DHCP

```
[root@M1 ~]# systemctl start dhcpd
```

```
[root@attacker ~]# ip addr add 192.168.34.1/24 dev ens3
[root@attacker ~]# ip addr add 192.168.33.11/24 dev ens3
[root@attacker ~]# systemctl start dhcpd
```

On récupère bien le réseau dupuis les ports "trusts" sur la VM2.

```
Nov 06 07:28:43 VM2 NetworkManager[782]: <info>  [1604665723.5102] dhcp4 (ens3): activation: beginning transaction (timeout in 45 seconds)
Nov 06 07:28:44 VM2 NetworkManager[782]: <info>  [1604665724.5579] dhcp4 (ens3):   address 192.168.33.10
Nov 06 07:28:44 VM2 NetworkManager[782]: <info>  [1604665724.5581] dhcp4 (ens3):   plen 24
Nov 06 07:28:44 VM2 NetworkManager[782]: <info>  [1604665724.5581] dhcp4 (ens3):   expires in 60 seconds
Nov 06 07:28:44 VM2 NetworkManager[782]: <info>  [1604665724.5582] dhcp4 (ens3):   nameserver '1.1.1.1'
Nov 06 07:28:44 VM2 NetworkManager[782]: <info>  [1604665724.5582] dhcp4 (ens3):   nameserver '8.8.8.8'
Nov 06 07:28:44 VM2 NetworkManager[782]: <info>  [1604665724.5582] dhcp4 (ens3):   gateway 192.168.33.1
```

# Mise en œuvre des fonctionnalités de sécurité réseau d'un switch

[[_TOC_]]

## Todos

* Configuration de deux serveurs DHCP (Légitime, Pirate)
    * [ ] (A) Serveur légitime
    * [ ] (A) Serveur attaquant
* 4 scénarios d'attaques
    * [ ] (G) CAM Flooding (script Python)
    * [ ] (A) DHCP Snooping
    * [ ] (B) Port Stealing (script Python)
    * [x] ARP Spoofing (script Python)
* 3 mise en place de protection
    * [ ] (G,B) Port security
    * [ ] (A) DHCP Snooping
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
**Table CAM (Content Addressable Memory)**

Table de référence d'un Switch qui fait la relation entre une adresse MAC et un numéro de port, et contient également les paramètres VLAN associés.

**CAM Flooding Attack / Attaque par saturation**

L'attaque exploite les limitations matérielles et de mémoire de la table CAM du Switch. Elle consiste à envoyer de (très) nombreuses trames Ethernet au Switch. Chaque trame envoyée possède une adresse MAC source différente (généralement erronnée), dans le but de remplir l'intégralité de l'espace disponible de la table CAM.

Une fois la table remplie, le trafic réseau est flood sur tous les ports car étant donné que la table CAM ne peut plus stocker d'adresses MAC, elle n'est plus en mesure de déterminer quelle adresse MAC de destination correspond à quel paquet envoyé. Le Switch agit alors comme un Hub.

**Port stealing Attack / Attaque par vol de port :**

L'attaquant utilise l'adresse MAC de la victime pour garnir la table CAM du Switch avec le couple :
- Adresse MAC de la Victime
- Port de la machine de l'attaquant

Ainsi l'attaquant recevra tous les paquets destinés à la victime puisque le Switch pensera alors qu'il transmet lesdits paquets à la victime (puisqu'utilisant le port renseigné par l'attaquant.)

## 3.2 Mise en œuvre de la mesure de protection DHCP snooping

### Insertion d'un rogue DHCP server sur un réseau local

-

### Configuration des serveurs DHCP

* https://linuxhint.com/dhcp_server_centos8/

Configuration du serveur DHCP légitime sur la VM1


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

On recupère bien la configuration DHCP sur le VM2

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


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

## Configuration des serveurs DHCP

* https://linuxhint.com/dhcp_server_centos8/

## CAM Flooding, port-stealing et mise en œuvre de contre-mesures
**Table CAM (Content Addressable Memory)**

Table de référence d'un Switch qui fait la relation entre une adresse MAC et un numéro de port, et contient également les paramètres VLAN associés.

**CAM Flooding Attack / Attaque par saturation**

L'attaque exploite les limitations matérielles et de mémoire de la table CAM du Switch. Elle consiste à envoyer de (très) nombreuses trames Ethernet au Switch. Chaque trame envoyée possède une adresse MAC source différente (généralement erronnée), dans le but de remplir l'intégralité de l'espace disponible de la table CAM.

Une fois la table remplie, le trafic réseau est flood sur tous les ports car étant donné que la table CAM ne peut plus stocker d'adresses MAC, elle n'est plus en mesure de déterminer quelle adresse MAC de destination correspond à quel paquet envoyé. Le Switch agit alors comme un Hub.

**Port stealing Attack / Attaque par vol de port :**

L'attaquant utilise l'adresse MAC de la victime pour garnir la table CAM du Switch avec le couple adresse MAC victime/Port de la machine de l'attaquant.




# Mise en œuvre des fonctionnalités de sécurité réseau d'un switch

[[_TOC_]]

## Todos

* Configuration de deux serveurs DHCP (Légitime, Pirate)
    * [ ] Serveur légitime
    * [ ] Serveur attaquant
* 4 scénarios d'attaques
    * [ ] CAM Flooding (script Python)
    * [ ] DHCP Snooping
    * [ ] Port Stealing (script Python)
    * [x] ARP Spoofing (script Python)
* 3 mise en place de protection
    * [ ] Port security
    * [ ] DHCP Snooping
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

## CAM Flooding, port-stealing et mise en œuvre de contre-mesures
**Table CAM (Content Addressable Memory)**

Table de référence d'un Switch qui fait la relation entre une adresse MAC et un numéro de port.

**CAM Flooding Attack / Attaque par saturation**

L'attaque consiste à envoyer de (très) nombreuses trames Ethernet au Switch. Chaque trame envoyée possède une adresse MAC source différente, dans le but de remplir l'intégralité de l'espace disponible de la table CAM.

**Port stealing Attack / Attaque par vol de port :**

L'attaquant utilise l'adresse MAC de la victime pour garnir la table CAM du Switch avec le couple adresse MAC victime/Port de la machine de l'attaquant.

## 

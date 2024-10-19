# Configuration de l'adresse IP et activation de l'interface réseau

```bash
ip address add [adresse_IP]/24 dev ethx
ip link set up dev ethx
```

- `ip address add` : Ajoute une adresse IP sur l'interface réseau `ethx`.
- `ip link set up` : Active l'interface réseau `ethx`.

## Vérifications:

```bash
ip a    # Affiche les interfaces réseau et leurs configurations (IP, état, etc.)
ip r    # Affiche la table de routage
ip n    # Affiche la table de voisinage (ARP)
ping -c2 [adresse]    # Ping pour tester la connectivité (ici, 2 paquets envoyés)
```

## Configuration du fichier `/etc/network/interfaces`
Éditez le fichier `/etc/network/interfaces` pour configurer la connexion réseau permanente (statique ou DHCP).

```bash
nano /etc/network/interfaces
```

### Pour une adresse IP statique:
```bash
auto ethx
iface ethx inet static
  address [adresse_IP]
  netmask 255.255.255.0
  gateway [adresse_passerelle]
```

- `auto ethx` : Active automatiquement l'interface `ethx` au démarrage.
- `iface ethx inet static` : Définit la configuration IP statique.

### Pour une adresse DHCP:
```bash
auto ethx
iface ethx inet dhcp
```

## Activer le routage IP
Éditez `/proc/sys/net/ipv4/ip_forward` pour activer le routage IP.

```bash
nano /proc/sys/net/ipv4/ip_forward
```

Assurez-vous que cette ligne est décommentée dans le fichier de configuration de sysctl:

```bash
nano /etc/sysctl.conf
```

```text
net.ipv4.ip_forward = 1
```

Appliquez les changements avec:

```bash
sysctl -p
```

## Configuration du serveur DHCP
### 1. Fichier de configuration par défaut du serveur ISC DHCP:
```bash
nano /etc/default/isc-dhcp-server
```

Modifiez l'interface à écouter:

```bash
INTERFACESv4="ethx"
```

### 2. Configuration du serveur DHCP (Plage d’adresses, options):
```bash
nano /etc/dhcp/dhcpd.conf
```

Exemple de configuration:

```text
subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.10 192.168.1.100;
  option routers 192.168.1.1;
  option domain-name-servers 8.8.8.8, 8.8.4.4;
}
```

- `range` : La plage d’adresses IP que le serveur DHCP attribuera.
- `option routers` : L'adresse IP du routeur/passerelle.
- `option domain-name-servers` : Serveurs DNS à utiliser.

### 3. Vérification des logs:
Les logs relatifs au serveur DHCP se trouvent dans:

```bash
tail -f /var/log/syslog
```

### 4. Client DHCP:
Pour demander une IP via DHCP sur une interface spécifique:

```bash
dhclient ethx
```

## Configuration du routage manuel
Dans `/etc/network/interfaces`, vous pouvez ajouter des routes manuellement avec ces commandes:

```bash
up ip route add default via [adresse_passerelle]
up ip route add [adresse_réseau]/24 via [adresse_passarelle]
up ip route add [network/mask] via [gateway]
```

## Utilisation des protocoles TCP/UDP
### Serveur TCP:
```bash
nc -l [port]
```

### Serveur UDP:
```bash
nc -l -u [port]
```

## Option RFC 3442 (Routes statiques classless)
Ajoutez cette option dans votre fichier `dhcpd.conf` pour définir des routes statiques classless selon la RFC 3442.

```text
option rfc3442-classless-static-routes code 121 = array of unsigned integer 8;
```

## Flush d'adresse IP
Si vous souhaitez supprimer les configurations IP d'une interface:

```bash
ip a flush dev ethx
```

## Récapitulatif IP, passerelle, et masque:
- **IP** : Adresse IP (e.g. `192.168.1.10`)
- **Passerelle** : Adresse de la passerelle (routeur) (e.g. `192.168.1.1`)
- **Masque** : Masque de sous-réseau (e.g. `255.255.255.0`)

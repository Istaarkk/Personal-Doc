# IP Address Configuration and Network Interface Activation

```bash
ip address add [IP_address]/24 dev ethx
ip link set up dev ethx
```

- `ip address add`: Adds an IP address to the network interface `ethx`.
- `ip link set up`: Brings the `ethx` network interface up.

## Verification Commands:

```bash
ip a    # Displays network interfaces and their configurations (IP, state, etc.)
ip r    # Shows the routing table
ip n    # Shows the neighbor table (ARP)
ping -c2 [address]    # Ping to test connectivity (here, 2 packets sent)
```

## Configuration of `/etc/network/interfaces`
Edit the `/etc/network/interfaces` file to configure permanent network settings (static or DHCP).

```bash
nano /etc/network/interfaces
```

### For a Static IP Address:
```bash
auto ethx
iface ethx inet static
  address [IP_address]
  netmask 255.255.255.0
  gateway [gateway_address]
```

- `auto ethx`: Automatically brings up the `ethx` interface at boot.
- `iface ethx inet static`: Defines a static IP configuration.

### For a DHCP Configuration:
```bash
auto ethx
iface ethx inet dhcp
```

## Enabling IP Forwarding
Edit `/proc/sys/net/ipv4/ip_forward` to enable IP routing.

```bash
nano /proc/sys/net/ipv4/ip_forward
```

Ensure this line is uncommented in the sysctl configuration file:

```bash
nano /etc/sysctl.conf
```

```text
net.ipv4.ip_forward = 1
```

Apply the changes with:

```bash
sysctl -p
```

## DHCP Server Configuration
### 1. Default Configuration File for the ISC DHCP Server:
```bash
nano /etc/default/isc-dhcp-server
```

Modify the interface to listen on:

```bash
INTERFACESv4="ethx"
```

### 2. DHCP Server Configuration (IP Range, Options):
```bash
nano /etc/dhcp/dhcpd.conf
```

Example configuration:

```text
subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.10 192.168.1.100;
  option routers 192.168.1.1;
  option domain-name-servers 8.8.8.8, 8.8.4.4;
}
```

- `range`: The range of IP addresses the DHCP server will assign.
- `option routers`: The IP address of the router/gateway.
- `option domain-name-servers`: DNS servers to use.

### 3. Checking Logs:
DHCP server logs can be found in:

```bash
tail -f /var/log/syslog
```

### 4. DHCP Client:
To request an IP address via DHCP for a specific interface:

```bash
dhclient ethx
```

## Manual Routing Configuration
In `/etc/network/interfaces`, you can manually add routes using these commands:

```bash
up ip route add default via [gateway_address]
up ip route add [network_address]/24 via [gateway_address]
up ip route add [network/mask] via [gateway]
```

## Using TCP/UDP Protocols
### TCP Server:
```bash
nc -l [port]
```

### UDP Server:
```bash
nc -l -u [port]
```

## RFC 3442 Option (Classless Static Routes)
Add this option in your `dhcpd.conf` file to define classless static routes according to RFC 3442.

```text
option rfc3442-classless-static-routes code 121 = array of unsigned integer 8;
```

## Flushing IP Address
If you want to remove IP configurations from an interface:

```bash
ip a flush dev ethx
```

## IP, Gateway, and Subnet Mask Summary:
- **IP**: IP Address (e.g., `192.168.1.10`)
- **Gateway**: The gateway (router) address (e.g., `192.168.1.1`)
- **Subnet Mask**: Subnet mask (e.g., `255.255.255.0`)

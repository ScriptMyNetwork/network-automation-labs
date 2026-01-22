# LAB006 – Internet Router Configuration (ISP-CE)

This document describes the **baseline configuration** for the internet-facing router used in LAB006.  
The router provides upstream connectivity between the Palo Alto firewall and the EVE-NG cloud network.

---

## Device Role

- Acts as **ISP / Internet Edge (CE)**
- Provides default route toward EVE-NG cloud
- Connects directly to the Palo Alto firewall outside interface

---

## Interface Summary

| Interface | Purpose | IP Address |
|---------|--------|-----------|
FastEthernet0/0 | Management / Cloud Network | DHCP |
Ethernet1/0 | Connection to Palo Alto Firewall | 100.64.0.2/24 |

---

## Router Configuration

### Enter Configuration Mode

```text
enable
configure terminal
Set Hostname
hostname ISP-CE
Configure Management / Cloud Interface
interface FastEthernet0/0
 ip address dhcp
 description Internet
 no shutdown
 exit
This interface connects to the EVE-NG management/cloud network and receives its IP address via DHCP.

Configure Interface Toward Palo Alto Firewall
interface Ethernet1/0
 ip address 100.64.0.2 255.255.255.0
 description To-PaloAlto
 no shutdown
 exit
This interface connects to:

Palo Alto outside interface (ethernet1/2)

Subnet: 100.64.0.0/24

Configure Default Route
ip route 0.0.0.0 0.0.0.0 192.168.204.2
Important:
The next-hop IP (192.168.204.2) must be the default gateway of the EVE-NG Linux host.

To find this value, run the following command on the EVE-NG host (VMware / VirtualBox):

ip a
Use the gateway associated with the cloud-facing interface.

Save Configuration
end
write memory
Validation Checklist
After configuration, verify:

Router can ping public IPs (e.g., 8.8.8.8)

Palo Alto outside interface can reach 100.64.0.2

Palo Alto can ping the internet using source interface

NAT translations occur correctly on the firewall

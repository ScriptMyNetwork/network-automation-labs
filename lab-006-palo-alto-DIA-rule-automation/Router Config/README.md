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

# Set Hostname
hostname ISP-CE

# Configure Management / Cloud Interface
interface FastEthernet0/0
 ip address dhcp
 description Internet
 no shutdown
 exit

# Configure Interface Toward Palo Alto Firewall
interface Ethernet1/0
 ip address 100.64.0.2 255.255.255.0
 description To-PaloAlto
 no shutdown
 exit

# Configure Default Route
ip route 0.0.0.0 0.0.0.0 192.168.204.2

#Important:
#The next-hop IP (192.168.204.2) must be the default gateway of the EVE-NG Linux host.
#To find this value, run the following command on the EVE-NG host (VMware / VirtualBox):
  "ip a"
#Use the gateway associated with the cloud-facing interface.

# Save Configuration
end
write memory

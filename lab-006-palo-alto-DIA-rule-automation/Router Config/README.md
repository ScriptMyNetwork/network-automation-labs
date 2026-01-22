en

conf t

hostname ISP-CE

int fa0/0  #Managent Cloud Connected Interface
 ip add dhcp
 description Internet
 no shut
 exit

int e1/0  #Connected to PA firewall
 ip add 100.64.0.2 255.255.255.0
 description To-LAN
 no shut
 exit

ip route 0.0.0.0 0.0.0.0 192.168.204.2   

#default route IP should be default Gateway IP of the EVE NG Linux VM. Find this by running "ip a" on the EVE NG host in VMWare/Virtual Box

end

write mem

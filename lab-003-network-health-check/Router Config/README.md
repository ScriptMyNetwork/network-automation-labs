! Follow below template 

enable
configure terminal

hostname R* ! Depending on which router you are configuring

username admin privilege 15 secret <YOUR PASSWORD>

line vty 0 4
 login local
 transport input ssh
exit

ip ssh version 2

int Eth 0/1 ! Interface connected to L2 switch

ip add 10.0.0.x 255.255.255.0 ! x - Depending on router you can choose what to set - ensure same is defined in devices.yaml

!! Assign IP Addressess to the P2P links between routers and configure routing of your choice - Static/OSPF/EIGRP .etc

! In this example I configured static routes and added loopbacks for each router

end
write memory

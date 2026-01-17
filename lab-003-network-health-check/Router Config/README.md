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

!! Assign IP Addressess to the P2P links between routers and configure routing of your choice - Static/OSPF/EIGRP .etc

! In this example I configured static routes and added loopbacks for each router

end
write memory

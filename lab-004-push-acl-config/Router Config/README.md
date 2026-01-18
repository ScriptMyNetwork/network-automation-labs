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

end
write memory

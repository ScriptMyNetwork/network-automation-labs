! Follow below template

enable configure terminal

hostname R* ! Depending on which router you are configuring

username admin privilege 15 secret

line vty 0 4 login local transport input ssh exit

ip ssh version 2

int Eth 0/1 ! Interface connected to L2 switch

ip add 10.0.0.x 255.255.255.0 ! x - Depending on router you can choose what to set - ensure same is defined in devices.yaml

end 

write memory

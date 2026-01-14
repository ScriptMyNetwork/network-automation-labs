Topology Diagram - Linux VM has 2 NICs;

1 - Static IP for Router management;

2 - DHCP Connected to Management cloud for itnernet connectivity - this helps to install necessary libraries;

[Ubuntu VM]
    |        (lab network)
[L2 Switch]
   /  \
[R1] [R2]

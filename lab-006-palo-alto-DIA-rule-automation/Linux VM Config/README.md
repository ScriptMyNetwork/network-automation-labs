## Linux VM Setup

Identify Interfaces

ip link
ip addr

Assumptions:

Inside interface (connected to L2 switch): ens3

Management / cloud interface: ens4

2. Configure Static IP on Inside Interface
sudo ip addr add 53.150.0.10/24 dev ens3
sudo ip link set ens3 up
Verify:

ip addr show ens3

3. Enable DHCP on Management Interface (Temporary)
sudo dhclient ens4

Verify internet access (temporary):

ping -c 3 8.8.8.8

4. Update System and Install Required Packages

sudo apt update
sudo apt install -y \
  python3 \
  python3-pip \
  python3-venv \
  git \
  curl \
  wget \
  unzip

Verify:

python3 --version
pip3 --version

5. Create Lab Directories

mkdir -p ~/network-automation-labs/lab006-DIA
cd ~/network-automation-labs/lab006-DIA

6. Create and Activate Python Virtual Environment

python3 -m venv venv
source venv/bin/activate

Upgrade pip:

pip install --upgrade pip

7. Install Python Libraries

pip install requests pyyaml

Verify:

pip list

8. Copy Automation Files

Using WinSCP, copy the following files into:

~/network-automation-labs/lab006-DIA/
Files:
pa_dia.py
config.yaml

Verify:

ls -l

9. Disable Management Interface (ens4)

After copying files and installing packages, disable the management/cloud interface:

sudo ip link set ens4 down

Verify:

ip link show ens4

Expected:

state DOWN

10. Set Default Gateway to Palo Alto Firewall

Remove any existing default routes:

sudo ip route del default

Add firewall as default gateway:

sudo ip route add default via 53.150.0.1 dev ens3

Verify:

ip route

Expected:

default via 53.150.0.1 dev ens3

11. Configure DNS Servers

Edit resolver configuration:

sudo nano /etc/resolv.conf

Replace entire contents with:

nameserver 1.1.1.1
nameserver 8.8.8.8
Fix permissions:

sudo chmod 644 /etc/resolv.conf

(Optional) Prevent overwrite:

sudo chattr +i /etc/resolv.conf

12. Validate Connectivity

DNS resolution:

nslookup github.com

Firewall-routed internet access:

curl https://github.com

Blocked site test:

curl https://google.com

Expected:

GitHub: allowed

Google: blocked (after security policy applied)

13. Final State Verification

ip addr
ip route
ip link show ens4

Confirm:

ens4 is DOWN

Default route via 53.150.0.1

DNS resolves correctly

Outcome
At this point:

Linux VM has static inside IP

No direct internet bypass exists

All traffic flows through Palo Alto

Automation environment is ready

All steps below apply to **PAN-OS 10.1** and are intended to be completed **before** running any automation scripts.

---

## Environment Summary

| Component | Value |
|---------|------|
Inside Interface | ethernet1/1 |
Outside Interface | ethernet1/2 |
Inside IP | 53.150.0.1/24 |
Outside IP | 100.64.0.1/24 |
Inside Zone | inside |
Outside Zone | outside |
Virtual Router | default |
DNS Servers | 1.1.1.1, 8.8.8.8 |

---

## Step 1 – Interface Configuration

### Inside Interface (ethernet1/1)

- Interface Type: Layer3
- IP Address: `53.150.0.1/24`
- Virtual Router: `internet`
- Security Zone: `inside`
- Management Profile: Create New and ensure Ping, HTTP and HTTPS are enabled

### Outside Interface (ethernet1/2)

- Interface Type: Layer3
- IP Address: `100.64.0.1/24`
- Virtual Router: `internet`
- Security Zone: `outside`
- Management Profile: Ensure ping is enabled

> **Important:** Both interfaces must be attached to the **same virtual router** for routing and NAT to function correctly.

---

## Step 2 – Zone Configuration

Create the following zones:

### Inside Zone
- Name: `inside`
- Type: Layer3
- Interface: `ethernet1/1`
- Virtual System: `vsys1`

### Outside Zone
- Name: `outside`
- Type: Layer3
- Interface: `ethernet1/2`
- Virtual System: `vsys1`

> Zone names are **case-sensitive** and must match exactly across policy and automation.

---

## Step 3 – Virtual Router Configuration

### Static Default Route

Navigate to:  
**Network → Virtual Routers → Add → internet → Static Routes**

Create a default route:

- Destination: `0.0.0.0/0`
- Interface: `ethernet1/2`
- Next Hop Address: `100.64.0.2` (upstream router)

This route sends all internet-bound traffic toward the upstream router.

---

## Step 4 – Source NAT Configuration (DIA)

Navigate to:  
**Policies → NAT**

Create a new NAT rule.

### General Tab
- Name: `nat-inside-to-internet`

---

### Original Packet

- Source Zone: `inside`
- Destination Zone: `outside`
- Destination Interface: `ethernet1/2`
- Source Address: `53.150.0.0/24`
- Destination Address: `any`
- Service: `any`

---

### Translated Packet

#### Source Address Translation
- Translation Type: **Dynamic IP and Port**
- Address Type: **Interface Address**
- Interface: `ethernet1/2`
- IP Address: `100.64.0.1/24`

#### Destination Address Translation
- Translation Type: **None**

> **Key Detail:**  
> The translated source address must be the **outside interface IP**, not the inside IP or a pool, to enable correct outbound NAT.

---

## Step 5 – Security Policy: Allow DNS Traffic

DNS must be explicitly allowed for:
- FQDN resolution
- Internet access
- FQDN-based security rules to function

Navigate to:  
**Policies → Security**

Create a rule **above any deny rules**.

### DNS Allow Rule

- Name: `allow-dns`
- From Zone: `inside`
- To Zone: `outside`
- Source Address: `53.150.0.0/24`
- Destination Address:
  - `1.1.1.1`
  - `8.8.8.8`
- Application: `any`
- Service:
  - `udp/53`
  - `tcp/53`
- Action: `allow`
- Log at Session End: Enabled

> Both **UDP and TCP 53** are required for reliable DNS resolution.

---

## Step 6 – Commit Configuration

After completing:
- Interfaces
- Zones
- Virtual router
- NAT
- DNS security policy

Perform a **commit**.

Verify:
- Interfaces are up
- NAT hit counters increase
- DNS queries are logged

---

## Validation Checklist

Before proceeding with automation, confirm:

- Linux host can ping `53.150.0.1`
- Linux host can resolve DNS queries
- Traffic logs show DNS traffic hitting `allow-dns`
- NAT translations are visible for DNS traffic
- Default route is active on the virtual router

---

## Outcome

At the end of this configuration:

- The firewall supports outbound internet access
- DNS is explicitly permitted
- NAT is correctly applied for DIA traffic
- The environment is ready for **policy automation**

This configuration provides a **secure, deterministic baseline** for automated security policy enforcement.

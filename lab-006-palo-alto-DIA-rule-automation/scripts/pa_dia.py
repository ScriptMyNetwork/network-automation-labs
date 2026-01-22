import requests
import yaml
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_cfg():
    with open("config.yaml") as f:
        return yaml.safe_load(f)

def api_call(host, params):
    url = f"https://{host}/api/"
    r = requests.get(url, params=params, verify=False, timeout=15)
    if r.status_code != 200 or 'status="success"' not in r.text:
        print("API ERROR:")
        print(r.text)
        sys.exit(1)
    return r.text

def get_key(host, user, pwd):
    params = {
        "type": "keygen",
        "user": user,
        "password": pwd
    }
    r = requests.get(f"https://{host}/api/", params=params, verify=False)
    return r.text.split("<key>")[1].split("</key>")[0]

def set_config(host, key, xpath, element):
    params = {
        "type": "config",
        "action": "set",
        "key": key,
        "xpath": xpath,
        "element": element
    }
    api_call(host, params)

def main():
    cfg = load_cfg()
    pa = cfg["pa"]
    vsys = cfg["vsys"]

    key = get_key(pa["host"], pa["username"], pa["password"])

    # Address object
    ao = cfg["objects"]["linux_subnet"]
    set_config(
        pa["host"], key,
        f"/config/devices/entry/vsys/entry[@name='{vsys}']/address",
        f"<entry name='{ao['name']}'><ip-netmask>{ao['value']}</ip-netmask></entry>"
    )

    # FQDN object
    fq = cfg["objects"]["allowed_fqdn"]
    set_config(
        pa["host"], key,
        f"/config/devices/entry/vsys/entry[@name='{vsys}']/address",
        f"<entry name='{fq['name']}'><fqdn>{fq['fqdn']}</fqdn></entry>"
    )

    # Service object
    svc = cfg["objects"]["service"]
    set_config(
        pa["host"], key,
        f"/config/devices/entry/vsys/entry[@name='{vsys}']/service",
        f"""
        <entry name="{svc['name']}">
          <protocol>
            <tcp>
              <port>{svc['port']}</port>
            </tcp>
          </protocol>
        </entry>
        """
    )

    # Security rule
    pol = cfg["policy"]
    set_config(
        pa["host"], key,
        f"/config/devices/entry/vsys/entry[@name='{vsys}']/rulebase/security/rules",
        f"""
        <entry name="{pol['name']}">
          <from><member>{cfg['zones']['inside']}</member></from>
          <to><member>{cfg['zones']['outside']}</member></to>
          <source><member>{ao['name']}</member></source>
          <destination><member>{fq['name']}</member></destination>
          <service><member>{svc['name']}</member></service>
          <application><member>any</member></application>
          <action>allow</action>
        </entry>
        """
    )

    # Commit
    params = {
        "type": "commit",
        "cmd": "<commit></commit>",
        "key": key
    }
    api_call(pa["host"], params)

    print("SUCCESS: Objects and policy created and committed.")

if __name__ == "__main__":
    main()

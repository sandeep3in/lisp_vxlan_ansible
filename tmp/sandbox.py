from rich.pretty import pprint

vrfs = [
        [
            {
                "handoffs": [
                    {
                        "handoff_interface_local": "TenGigabitEthernet 1/0/1",
                        "handoff_ip_address": "192.168.220.2/30",
                        "handoff_vlan": 2020,
                        "remote_device": "fusion1-isr4451"
                    },
                    {
                        "handoff_interface_local": "TenGigabitEthernet 1/0/2",
                        "handoff_ip_address": "192.168.220.6/30",
                        "handoff_vlan": 2021,
                        "remote_device": "fusion1-isr4452"
                    }
                ],
                "vrf": "VN1"
            },
            {
                "handoffs": [
                    {
                        "handoff_interface_local": "TenGigabitEthernet 1/0/3",
                        "handoff_ip_address": "192.168.220.10/30",
                        "handoff_vlan": 2022,
                        "remote_device": "fusion1-isr4451"
                    }
                ],
                "vrf": "VN2"
            }
        ],
        [
            {
                "handoffs": [
                    {
                        "handoff_interface_local": "TenGigabitEthernet 1/0/1",
                        "handoff_ip_address": "192.168.220.14/30",
                        "handoff_vlan": 2023,
                        "remote_device": "fusion1-isr4451"
                    },
                    {
                        "handoff_interface_local": "TenGigabitEthernet 1/0/2",
                        "handoff_ip_address": "192.168.220.18/30",
                        "handoff_vlan": 2024,
                        "remote_device": "fusion1-isr4452"
                    }
                ],
                "vrf": "VN1"
            },
            {
                "handoffs": [
                    {
                        "handoff_interface_local": "TenGigabitEthernet 1/0/3",
                        "handoff_ip_address": "192.168.220.22/30",
                        "handoff_vlan": 2025,
                        "remote_device": "fusion1-isr4451"
                    }
                ],
                "vrf": "VN2"
            }
        ]
    ]

flat_vrfs = {}
for device_vrf in vrfs:
   for vrf in device_vrf:
       pprint(vrf["vrf"])
       if flat_vrfs.get(vrf["vrf"]) is None:
          flat_vrfs[vrf["vrf"]] = vrf["handoffs"]
          pprint(flat_vrfs[vrf["vrf"]])
       else:
           print("HERE")
           pprint(flat_vrfs[vrf["vrf"]])
           # pprint(type(flat_vrfs[vrf["vrf"]]))
           # pprint(vrf["handoffs"])
           for item in vrf["handoffs"]:
               print("ITEM")
               pprint(item)
               flat_vrfs[vrf["vrf"]] = flat_vrfs[vrf["vrf"]].append(item)
    print("THIS")
    pprint(flat_vrfs)

pprint(flat_vrfs)

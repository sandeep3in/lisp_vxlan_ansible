##### Authors: Sandeep Joseph and Jose Bogarin

# LISP/VXLAN fabric Ansible playbook

## Introduction
This is the Ansible playbook for automating LISP/VXLAN fabric. In the past, the LISP/VXLAN fabric was only deployed with the Cisco DNA Center. The playbook can be used for deployment who would want to create a LISP/VXLAN fabric without using the Cisco DNAC. 
The playbook takes care of the following scenario:

- Border and Control plane on a single device 
- Only supports IP transit
- Support for fusion automation. Supported fusion devices are Cisco routers and Switches.
- Fusion automation can be skipped in the playbook
- Multiple fabric edges with multiple L3 and L2 instance-id
- No support in the playbook to support additional features such as Multicast 

The following topology is supported and validated:

![image](https://github.com/sandeep3in/multiple-vxlan-lisp/assets/84372117/d96eff9f-e898-4955-93b3-95caa00eedbd)

The border can be dual-homed to the fusion in a full mesh topology or it could be partial mesh between the fusion and the border node. The playbook supports and understands full mesh or partial mesh topology between the border and the fusion.

The topology is defined in a file as a variable that will be discussed later.

## Pre-requisite
To run the Ansible playbook the following pre-requisite needs to be met:
- Ansible installed 
  [Ansible installation support](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#control-node-requirements)
- usage of ipaddr jinja filter [ipaddr jijna filter support](https://docs.ansible.com/ansible/latest/collections/ansible/utils/docsite/filters_ipaddr.html)  
- Knowledge of LISP/VXLAN fabric- Border/Control plane and fabric edge- [Config guide of LISP/VXLAN](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lisp_vxlan/b-179-lisp-vxlan-fabric-cg/lisp-vxlan-overview.html)
- [SSH support on the network devices-](https://www.cisco.com/c/en/us/support/docs/security-vpn/secure-shell-ssh/4145-ssh.html) 

## Variable definitions 
The Ansible controller will need the IP address of the devices to do an SSH and configure the devices. 
This file is known as the inventory file and is defined in the "hosts.yml" file under the main directory:

```yaml
root@ubutu-ansible:/multiple-vxlan-lisp# ls
group_vars  hosts_old.yml  hosts.yml  host_vars  playbooks  poetry.lock  pyproject.toml  README.md  tmp

root@ubutu-ansible:/multiple-vxlan-lisp_change# cat hosts.yml
net:
  hosts:
    fusion1-isr4451:
      ansible_host: 9.201.201.14
      fusion: true
    fusion2-isr4451:
      ansible_host: 9.253.253.12
      fusion: true
    border1-9500:
      ansible_host: 9.253.253.10
      border: true
      control_plane: true
    border2-9500:
      ansible_host: 9.253.253.14
      border: true
      control_plane: true
    edge1-9300:
      ansible_host: 9.253.253.11
      edge: true
```
The IP address in the "host.yml" file is the address used by the Ansible controller to do an ssh to the device. This IP address can be any address on the device which should be reachable to the Ansible controller.
Please note that the above file is for illustration, please modify the file as per the topology used. The fusion device is optional, modify the "hosts.yml" file if the automation of the fusion is not needed. 

the next variable to be defined is the group variable. The group variables are where the fabric definitions are defined.
```yaml
root@ubutu-ansible:/multiple-vxlan-lisp_change/group_vars# pwd
/multiple-vxlan-lisp/group_vars
root@sand-ubutu-ansible:/multiple-vxlan-lisp/group_vars# cat all.yml
ansible_connection: ansible.netcommon.network_cli
ansible_user: sand # username to login to the network device
ansible_password: sand # password for the network device
ansible_become: yes
ansible_become_method: enable
ansible_network_os: cisco.ios.ios
key: Cisco # Authentication key for authenticating the map server.
dhcp_excluded_lower: 1 
dhcp_excluded_upper: 50
border_bgp_as: 65015 # BGP AS number of the border node
fusion_bgp_as: 65005 # BGP AS number of the fusion  node

# defintions of L3 and L2 instances
l3_instances:
  4099:  #L3 instance-id number
    vrf: VN1  #vrf name
    l2:
      - instance_id: 8188  #L2 instance-id number
        vlan: 1024 # VLAN number 
        mac_address: 0000.0c9f.f821 # mac address of the gateway
        gateway: 192.168.2.1 # Anycast gateway
        dhcp_server_address: 192.168.2.2 # Helper address for the anycast gateway
        network_prefix: 192.168.2.0/24   
      - instance_id: 8189
        vlan: 1025
        mac_address: 0000.0c9f.f822
        gateway: 192.168.3.1
        dhcp_server_address: 192.168.3.2
        network_prefix: 192.168.3.0/24

  4100:
    vrf: VN2
    l2:
      - instance_id: 8190
        vlan: 1026
        mac_address: 0000.0c9f.f823
        gateway: 192.168.4.1
        dhcp_server_address: 192.168.4.2
        network_prefix: 192.168.4.0/24

```
The next variable that needs to be defined is the host variable, the host variable includes the loopback address used as RLOC in LISP and the BGP configurations required between the border and fusion node. if fusion automation is not required the ansible playbook will use the configuration from the border node to create the respective BGP configuration on the border node.
```yaml
root@ubutu-ansible:/multiple-vxlan-lisp_change/host_vars# pwd
/multiple-vxlan-lisp_change/host_vars
root@ubutu-ansible:/multiple-vxlan-lisp_change/host_vars# ls
border1-9500.yml  border2-9500.yml  edge1-9300.yml  fusion1-isr4451.yml  fusion2-isr4451.yml

root@ubutu-ansible:/multiple-vxlan-lisp_change/host_vars# cat border1-9500.yml
loopback0_interface_ip: 9.253.253.10 # Loopback interface ip address
vrfs:
    - vrf: VN1
      handoffs:
        - handoff_vlan: 2020
          handoff_ip_address: 192.168.220.2/30
          handoff_interface: GigabitEthernet1/0/9
          remote_device: fusion1-isr4451

        - handoff_vlan: 2021
          handoff_ip_address: 192.168.220.6/30
          handoff_interface: GigabitEthernet1/0/8
          remote_device: fusion2-isr4451

    - vrf: VN2
      handoffs:
        - handoff_vlan: 2022
          handoff_ip_address:  192.168.220.10/30
          handoff_interface: GigabitEthernet1/0/9
          remote_device: fusion1-isr4451

        - handoff_vlan: 2023
          handoff_ip_address:  192.168.220.14/30
          handoff_interface: GigabitEthernet1/0/8
          remote_device: fusion2-isr4451

root@ubutu-ansible:/multiple-vxlan-lisp_change/host_vars# cat edge1-9300.yml
loopback0_interface_ip: 9.253.253.11 # Loopback interface ip address
```
The playbook supports automation of  fusion device if the fusion device is a Cisco IOS Router/Switch, in case the upstream device is a non-cisco platform or a Cisco firewall, then the fusion device can be excluded when running the playbook. To exclude the fusion platform  remove the fusion device details from the inventory file which is the "hosts.yml" file.

```yaml
root@ubutu-ansible:/multiple-vxlan-lisp_change/host_vars# cat  fusion1-isr4451.yml
type: switch # defines the fusion device, can take the keyword "switch" or "router"
vrfs:
  - vrf: VN1
    handoffs:
      - handoff_ip_address: 192.168.220.1/30
        handoff_vlan: 2020
        handoff_interface: ten1/0/5
        remote_device: border1-9500

      - handoff_ip_address: 192.168.220.17/30
        handoff_vlan: 2024
        handoff_interface: ten1/0/6
        remote_device: border2-9500
  - vrf: VN2
    handoffs:
      - handoff_ip_address: 192.168.220.9/30
        handoff_vlan: 2022
        handoff_interface: ten 1/0/5
        remote_device: border1-9500

      - handoff_ip_address: 192.168.220.25/30
        handoff_vlan: 2025
        handoff_interface: ten1/0/6
        remote_device: border2-9500

```

## Playbooks
Once the host variables are defined, the next is to run the playbook. The playbooks are located in the "playbooks" folder. 

```yaml
root@sand-ubutu-ansible:/multiple-vxlan-lisp_change/playbooks# pwd
/multiple-vxlan-lisp_change/playbooks

root@sand-ubutu-ansible:/multiple-vxlan-lisp_change/playbooks# ls
border-bgp.yml       border-l2-l3-overlay.yml  configure.yml         edge-l2-l3-overlay.yml  files           fusion-bgp.yml  misc       test_filter.yml
border-external.yml  border-pub-sub.yml        edge-l2-flooding.yml  edge-pub-sub.yml        filter_plugins  lookup_plugins  templates

root@sand-ubutu-ansible:/multiple-vxlan-lisp_change/playbooks# cat configure.yml
- name: Configure overlay
  hosts: all
  gather_facts: true
  vars:
    - skip_deploy: false

  tasks:
    - name: Configure Border L2/L3 Overlay
      ansible.builtin.include_tasks:
        file: border-l2-l3-overlay.yml
      when: border is defined and border is true

    - name: Configure Pub/Sub for Border
      ansible.builtin.include_tasks:
        file: border-pub-sub.yml
      when: border is defined and border is true

    - name: Configure Border External
      ansible.builtin.include_tasks:
        file: border-external.yml
      when: border is defined and border is true

    - name: Configure Border BGP
      ansible.builtin.include_tasks:
        file: border-bgp.yml
      when: border is defined and border is true

    - name: Configure Edge L2/L3 Overlay
      ansible.builtin.include_tasks:
        file: edge-l2-l3-overlay.yml
      when: edge is defined and edge is true

    - name: Configure Edge L2 Flooding on overlay
      ansible.builtin.include_tasks:
        file: edge-l2-flooding.yml
      when: edge is defined and edge is true

    - name: Configure Pub/Sub for Edge
      ansible.builtin.include_tasks:
        file: edge-pub-sub.yml
      when: edge is defined and edge is true

    - name: Configure Fusion BGP
      ansible.builtin.include_tasks:
        file: fusion-bgp.yml
      when: fusion is defined and fusion is true
```

All the playbooks are consolidated in the "configure.yml" file. The playbooks will create the respective configuration for the devices and then finally provisions the configurations on the devices. It's presumed the topology definitions defined by the user are accurate and hence no validations are done on the user input. In the case of any errors in the user input the playbook would error out while provisioning the configuration on the devices. The playbook follows the same logic as used in Cisco DNA center to create the configuration first and then provision the configuration on the devices.

To validate the configuration created by the playbook, look up the "files" folder  to verify the configuration created for Border/CP/Edge and the Fusion. The configuration is grouped based on the functionality such as BGP configuration, pub-sub configuration, etc.

``` yaml

root@ubutu-ansible:/multiple-vxlan-lisp_change/playbooks/files# pwd
/multiple-vxlan-lisp_change/playbooks/files

root@ubutu-ansible:/multiple-vxlan-lisp_change/playbooks/files# ls
border1-9500  border2-9500  edge1-9300  edge2-9300  fusion1-isr4451  fusion2-isr4451

root@ubutu-ansible:/multiple-vxlan-lisp_change/playbooks/files# cd border1-9500/
root@ubutu-ansible:/multiple-vxlan-lisp_change/playbooks/files/border1-9500# ls
border-bgp.conf  border-dynamic-external.conf  border-l2-l3-overlay.conf  border-pub-sub.conf
```

To run the playbook, navigate to the playbook folder and run the following CLI:

```yaml
    ansible-playbook  -i <path to the inventory file > <main playbook >
e.g:ansible-playbook  -i /multiple-vxlan-lisp_change/hosts_old.yml configure.yml 
 ```
Once the playbook is run successfully, you should see a success message, indicating a successful run.

```yaml


PLAY RECAP ****************************************************************************************************************************************************************************************
border1-9500               : ok=23   changed=4    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
border2-9500               : ok=23   changed=4    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
edge1-9300                 : ok=17   changed=2    unreachable=0    failed=0    skipped=5    rescued=0    ignored=0
fusion1-isr4451            : ok=7    changed=1    unreachable=0    failed=0    skipped=7    rescued=0    ignored=0
fusion2-isr4451            : ok=7    changed=2    unreachable=0    failed=0    skipped=7    rescued=0    ignored=0

```

# Conclusion and Acknowledgements

In case of any issues in running the playbook reach out to an SDA TME for support.

This work wouldn't have been possible without the support of the following people.
- Paul Nguyen- Manager SDA TME
- Kedar karmarkar- Principal TME 

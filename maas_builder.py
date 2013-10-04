#!/usr/bin/env python
# Author: Peter M. Petrakis <peter.petrakis@gmail.com>
# Program: virsh only, provision maas server using "nodes list" as basis
# Usage: maas_builder.py maas_profile node_list.json
import sys
import subprocess
import json

if len(sys.argv) != 3:
 print "usage... maas_builder.py maas_profile node_list.json"
 exit(1)

POWER = {'power_driver'  : 'kvm',
         'power_address' : 'qemu+tcp://10.193.36.101/system',
         'power_user'    : 'ubuntu'}

# XXX this uses the new power_params format LP: #1235404
CMD  = """maas-cli {maas_profile} nodes new architecture="{architecture}" \
hostname="{hostname}" \
mac_addresses="{mac_addresses}" \
power_type="{power_type}" \
power_parameters_power_driver="{power_driver}" \
power_parameters_power_address="{power_address}" \
power_parameters_power_user="{power_user}" \
power_parameters_power_id='{power_id}'"""

nodes = open(sys.argv[2], 'r').read()
nodes = json.loads(nodes)

for node in nodes:
  macs = []
  for mac in node['macaddress_set']:
    macs.append(mac['mac_address'])
 
  # parse file
  tmp = {'architecture'   : node['architecture'],
        'hostname'        : node['hostname'],
        'power_type'      : node['power_type'],
        'mac_addresses'   : list(macs)[0], # XXX format multiple macs
        'power_type'      : node['power_type'],
       }

  tmp = dict( {'maas_profile': sys.argv[1]}.items() + tmp.items())
 
  if node['power_type'] == 'virsh':
    power_id = node['hostname'].split('.')
    if len(power_id) > 1:
      power_id = power_id[0]
  
  tmp = dict(tmp.items() + POWER.items() + {'power_id': power_id}.items())
  if tmp['power_type'] == 'virsh':
    cmd = CMD.format(**tmp).split(' ')
    cmd = ' '.join(cmd)
    subprocess.call(cmd, shell=True)
      
print "...done"

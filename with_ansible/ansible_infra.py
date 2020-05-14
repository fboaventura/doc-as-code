#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create an infrastructure diagram from an Ansible hosts file

This script will read and parse an Ansible hosts definition file, identify the
hosts and groups and search for the `link_to` variable, in order to identify which
host is linked to which and draw the proper map.
"""

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager

from diagrams import Diagram, Edge

import sys
sys.path.insert(1, '../')
from helpers import get_host, get_node    # noqa


loader = DataLoader()
inventory = InventoryManager(loader=loader, sources='hosts.yml')
variables = VariableManager(loader=loader, inventory=inventory)


graph_attr = {
    "fontsize": "32",
    "fontcolor": "#1D3B52",
    "bgcolor": "white"
}
ignore = ('all', 'ungrouped')
nodes = []

with Diagram('fboaventura.dev', show=True, filename='ansible_fboaventura_dev',
             outformat='png', direction="LR", graph_attr=graph_attr) as diag:

    edge = Edge(color="#1D3B52", style='solid', forward=True)

    for host in inventory.get_hosts():
        hostname = host.get_vars()['inventory_hostname']
        group = host.get_vars()['group_names'][0]
        node = get_node(group, hostname)
        nodes.append({'hostname': hostname, 'node': node})

    for cluster in inventory.get_groups_dict():
        if cluster not in ignore:
            for host in inventory.get_hosts(str(cluster)):
                host_node = get_host(nodes, str(host))['node']
                link_to = host.get_vars()['link_to']
                if len(link_to) > 1:
                    for destination in link_to:
                        link_node = get_host(nodes, destination)['node']
                        host_node.connect(link_node, edge)
                else:
                    str(host)

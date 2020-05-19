#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create an infrastructure diagram from a docker-compose file

This script will read and parse a docker-compose definition file, identify the
hosts and groups and search for the `depends_on` variable, in order to identify which
host is linked to which and draw the proper map.
"""
from ruamel.yaml import YAML
from diagrams import Diagram, Edge

import sys
sys.path.insert(1, '../')
from helpers import get_node, get_host    # noqa


def docker_main():
    yaml = YAML()
    with open('docker-compose.yml', 'r') as f:
        dckr = yaml.load(f)

    services = dckr['services']

    graph_attr = {
        "fontsize": "32",
        "fontcolor": "#1D3B52",
        "bgcolor": "white"
    }
    ignore = ('all', 'ungrouped')
    nodes = []

    with Diagram('fboaventura.dev - Docker', show=False, filename='docker_fboaventura_dev',
                 outformat='png', direction="LR", graph_attr=graph_attr):

        edge = Edge(color="#1D3B52", style='solid', forward=True)

        for node in services:
            if 'deploy' in services[node]:
                how_many = services[node]['deploy']['replicas']
            else:
                how_many = 1

            i = 0
            while i < how_many:
                hostname = node.split('_')[1] if '_' in node else node
                group = node.split('_')[0] if '_' in node else node
                host_node = get_node(group, hostname)
                link_to = services[node]['depends_on']
                nodes.append({'hostname': hostname, 'node': host_node, 'link_to': link_to})
                i += 1

        for host in nodes:
            host_node = host['node']
            link_to = host['link_to']
            if len(link_to) > 1:
                for destination in link_to:
                    link_node = get_host(nodes, destination)['node']
                    host_node.connect(link_node, edge)
            else:
                str(node)


if __name__ == '__main__':
    docker_main()

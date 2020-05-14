#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create an infrastructure diagram from an Ansible hosts file

This script will read and parse an Ansible hosts definition file, identify the
hosts and groups and search for the `link_to` variable, in order to identify which
host is linked to which and draw the proper map.
"""

from diagrams.onprem.database import Postgresql, Mariadb, Mysql
from diagrams.onprem.inmemory import Memcached, Redis
from diagrams.onprem.queue import Celery, Rabbitmq, Activemq, Kafka
from diagrams.onprem.network import Nginx, Apache, Caddy, Haproxy
from diagrams.onprem.compute import Server


def get_node(group: str, hostname: str):
    """
    Return the node based on the group it belongs to
    :param group: the group to which the host belongs to
    :param hostname: hostname of the host
    :return: node object
    """

    to_search = group.lower().strip()
    if to_search.startswith('nginx'):
        return Nginx(hostname)
    elif to_search.startswith('apache'):
        return Apache(hostname)
    elif to_search.startswith('caddy'):
        return Caddy(hostname)
    elif to_search.startswith('haproxy'):
        return Haproxy(hostname)
    elif to_search.startswith('memcached'):
        return Memcached(hostname)
    elif to_search.startswith('postgres'):
        return Postgresql(hostname)
    elif to_search.startswith('mariadb'):
        return Mariadb(hostname)
    elif to_search.startswith('mysql'):
        return Mysql(hostname)
    elif to_search.startswith('rabbitmq'):
        return Rabbitmq(hostname)
    elif to_search.startswith('celery'):
        return Celery(hostname)
    elif to_search.startswith('activemq'):
        return Activemq(hostname)
    elif to_search.startswith('kafka'):
        return Kafka(hostname)
    elif to_search.startswith('redis'):
        return Redis(hostname)
    else:
        return Server(hostname)


def get_host(node_list: list, hostname: str) -> dict:
    """
    Find the hostname into a list of dicts
    :param node_list: list of dicts containing the hostname and node object
    :param hostname: hostname to be found
    :return: the dict that represents the object being searched
    """

    return next((_ for _ in node_list if _['hostname'] in hostname), None)

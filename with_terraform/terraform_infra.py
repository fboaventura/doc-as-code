#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create an infrastructure diagram from a docker-compose file

This script will read and parse a docker-compose definition file, identify the
hosts and groups and search for the `depends_on` variable, in order to identify which
host is linked to which and draw the proper map.
"""

import hcl2
from loguru import logger as log
from diagrams import Diagram, Edge

import sys
sys.path.insert(1, '../')
from helpers import get_node, get_host    # noqa

to_map_objects = [
    'docker_container',
    'aws_instance',
    'azurerm_linux_virtual_machine',
    'azurerm_windows_virtual_machine',
    'google_compute_instance',
]

with open('fboaventuradev.tf', 'r') as f:
    confs = hcl2.load(f)

# TODO: Make python read an output file from terraform
#   and parse it into diagrams code file


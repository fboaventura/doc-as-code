#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Frederico Freire Boaventura <frederico@boaventura.net>'

from diagrams import Diagram, Cluster
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Memcached, Redis
from diagrams.onprem.queue import Celery, Rabbitmq
from diagrams.onprem.network import Nginx, Haproxy

graph_attr = {
    "fontsize": "32",
    "fontcolor": "#1D3B52",
    "bgcolor": "white"
}

# Cria o Diagrama base do nosso mapa
with Diagram('fboaventura.dev', direction='LR', filename='simple_fboaventura_dev',
             outformat='png', graph_attr=graph_attr) as diag:
    # Adiciona os nós no mapa
    ingress = Haproxy('loadbalancer')
    webserver = Nginx('django')
    db = Postgresql('database')
    memcached = Memcached('sessions')

    # Criamos um cluster para os componentes do Celery, que trabalham em conjunto
    with Cluster('Celery'):
        beat = Celery('beat')
        workers = [Celery('worker1'), Celery('worker2')]
        flower = Celery('flower')
        broker = Rabbitmq('broker')
        logs = Redis('logs')

    # Montamos o mapa de relacionamentos entre os nós
    ingress >> webserver
    webserver >> broker
    beat >> broker
    workers >> beat
    webserver >> db
    db >> broker
    webserver >> memcached
    broker >> logs
    workers >> logs
    flower >> beat
    flower >> workers
    beat >> logs

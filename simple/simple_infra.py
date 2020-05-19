#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simple_infra.py
==========================
Este módulo é uma prova de conceito cujo objetivo é gerar um diagrama representando
a infraestrutura necessária para suportar uma aplicação em Django.
Este diagrama é gerado com os objetos do diagrama adicionados de forma manual.
"""

from diagrams import Diagram, Cluster
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Memcached, Redis
from diagrams.onprem.queue import Celery, Rabbitmq
from diagrams.onprem.network import Nginx, Haproxy


def simple_main():
    # graph_attr é a lista de parâmetros utilizados na construção do diagrama.
    graph_attr = {
        "fontsize": "32",
        "fontcolor": "#1D3B52",
        "bgcolor": "white"
    }

    # Cria o Diagrama base do nosso mapa
    with Diagram('fboaventura.dev', direction='LR', filename='simple_fboaventura_dev',
                 outformat='png', graph_attr=graph_attr, show=False) as diag:
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


if __name__ == '__main__':
    simple_main()

# -*- coding: utf-8 -*-
from Acquisition import aq_parent

import datetime


def ordenacao_agenda(obj, event):
    """Ordenacao por id dentro de uma agenda."""
    # Forcamos a data manualmente pois quando nao alterada
    # ele mantem o default_factory como valor padrao (o que muda todos os dias)
    date = [int(p) for p in obj.getId().split('-')]
    obj.date = datetime.date(*date)

    # Ordena objetos
    parent = aq_parent(obj)
    parent.orderObjects('id', reverse=False)

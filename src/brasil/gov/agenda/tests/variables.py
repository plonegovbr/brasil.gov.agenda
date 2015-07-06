# # -*- coding: utf-8 -*-
"""Variáveis para os testes robots"""

from datetime import date
from datetime import timedelta


def adiciona_mes(dt):
    """Retorna um dia do mês posterior"""
    dt1 = dt.replace(day=1)
    return dt1 + timedelta(days=32)


def subtrai_mes(dt):
    """Retorna um dia do mês anterior"""
    return dt.replace(day=1) - timedelta(days=1)

HOJE = date.today()
DIA_ATUAL = str(HOJE.day)
MES_ATUAL = str(HOJE.month)
ANO_ATUAL = str(HOJE.year)

DIA_MES_ANTERIOR = subtrai_mes(HOJE)
MES_ANTERIOR = str(DIA_MES_ANTERIOR.month)
DIA_DOIS_MESES_ANTERIORES = subtrai_mes(DIA_MES_ANTERIOR)
DOIS_MESES_ANTERIORES = str(DIA_DOIS_MESES_ANTERIORES.month)

DIA_MES_POSTERIOR = adiciona_mes(HOJE)
MES_POSTERIOR = str(DIA_MES_ANTERIOR.month)
DIA_DOIS_MESES_POSTERIORES = adiciona_mes(DIA_MES_POSTERIOR)
DOIS_MESES_POSTERIORES = str(DIA_DOIS_MESES_POSTERIORES.month)

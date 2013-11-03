***************************************************************
`Brasil.gov.br: Agenda de Membros do Governo Brasileiro`
***************************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
-----------

Este pacote provê tipos de conteúdo necessários a gestão de Agendas de membros
do Governo Brasileiro.


Estado deste pacote
---------------------

O **brasil.gov.agenda** tem testes automatizados e, a cada alteração em seu
código os testes são executados pelo serviço Travis. 

O estado atual dos testes pode ser visto nas imagens a seguir:

.. image:: https://secure.travis-ci.org/plonegovbr/brasil.gov.agenda.png?branch=master
    :target: http://travis-ci.org/plonegovbr/brasil.gov.agenda

.. image:: https://coveralls.io/repos/plonegovbr/brasil.gov.agenda/badge.png?branch=master
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.agenda


Instalação
------------

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``brasil.gov.agenda`` à lista de eggs da instalação::

        [buildout]
        ...
        eggs =
            brasil.gov.agenda

2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Acesse o painel de controle e instale o produto
**Brasil.gov.br: Agenda de Membros do Governo Brasileiro**.

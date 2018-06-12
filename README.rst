************************************************
.gov.br: Agenda de Membros do Governo Brasileiro
************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
-----------

Este pacote provê tipos de conteúdo necessários a gestão de Agendas de membros do Governo Brasileiro conforme disposto na `Lei 12.813, de 16 de Maio de 2013 <http://www.planalto.gov.br/ccivil_03/_Ato2011-2014/2013/Lei/L12813.htm>`_ artigos 2o. e 11o.

Estado deste pacote
---------------------

O **brasil.gov.agenda** tem testes automatizados e, a cada alteração em seu
código os testes são executados pelo serviço Travis.

O estado atual dos testes pode ser visto nas imagens a seguir:

.. image:: http://img.shields.io/pypi/v/brasil.gov.agenda.svg
    :target: https://pypi.python.org/pypi/brasil.gov.agenda

.. image:: https://img.shields.io/travis/plonegovbr/brasil.gov.agenda/master.svg
    :target: http://travis-ci.org/plonegovbr/brasil.gov.agenda

.. image:: https://img.shields.io/codacy/grade/77956b9df8a34087bc7ac4079f0e2ae3.svg
    :target: https://www.codacy.com/app/hvelarde/brasil.gov.agenda

.. image:: https://img.shields.io/coveralls/plonegovbr/brasil.gov.agenda/master.svg
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.agenda

Instalação
----------

Para habilitar a instalação deste produto em um ambiente que utilize o buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e adicionar o pacote ``brasil.gov.agenda`` à lista de eggs da instalação::

        [buildout]
        ...
        eggs =
            brasil.gov.agenda

2. Após alterar o arquivo de configuração é necessário executar ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Acesse o painel de controle e instale o produto **Brasil.gov.br: Agenda de Membros do Governo Brasileiro**.

Atualização de 1.x a 2.x
------------------------

.. Warning::
    Só atualize para a versão 2.x do pacote depois de atualizar à versão mais recente da branch 1.x.

As atualizações da versão 1.x à 2.x só são suportadas das versões mais recentes de cada branch.
Antes de atualizar confira que você está efetivamente utilizando a última versão da branch 1.x e que não existem upgrade steps pendentes de serem aplicados.

Desenvolvimento
---------------

Utilizamos `webpack <https://webpack.js.org/>`_ para gerenciar o conteúdo estático do tema,
tomando vantagem das diversas ferramentas e plugins disponíveis para suprir nossas necessidades.

Utilizamos a receita de buildout `sc.recipe.staticresources <https://github.com/simplesconsultoria/sc.recipe.staticresources>`_ para integrar o `webpack`_ no Plone.

Ao desenvolver os temas iniciamos o watcher do `webpack`_ e trabalhamos somente na pasta "webpack" alterando os arquivos;
o `webpack`_ se encarrega de processar e gerar os arquivos em seu endereço final.

Este pacote adiciona os seguintes comandos na pasta bin do buildout para processar automaticamente os recursos estáticos:

.. code-block:: console

    $ bin/env-brasilgovagenda

Este comando adiciona no terminal o node do buildout no PATH do sistema,
dessa forma voce pode trabalhar com webpack conforme a documentação oficial.

.. code-block:: console

    $ bin/watch-brasilgovagenda

Este comando instrui ao webpack para esperar por qualquer mudança nos arquivos SASS e gera a versão minificada do CSS para a aplicação.

.. code-block:: console

    $ bin/debug-brasilgovagenda

Este comando faz o mesmo que o comando watch, mas não minifica o CSS final.
Utilizado para debugar a geração do CSS.

.. code-block:: console

    $ bin/build-brasilgovagenda

Este comando cria o CSS minificado, mas não espera por mudanças.

Fazendo releases com o zest.releaser
------------------------------------

Os recursos estáticos do pacote são gerados usando o `webpack`_ e não são inclusos no VCS.
Se você está fazendo release usando o zest.releaser, você precisa fazer `upload manual dos arquivos no PyPI <https://github.com/zestsoftware/zest.releaser/issues/261>`_ ou você vai criar uma distribuição quebrada:

* execute ``longtest`` e ``fullrelease``, como de costume
* responda "não" para evitar o upload ao PyPI e continue normalmente
* faça checkout na tag do release que você está liberando
* execute ``bin/build-brasilgovagenda`` para criar os recursos estáticos
* crie os arquivos da distribuição usando ``python setup.py sdist bdist_wheel``, como de costume
* faça o upload manual dos arquivos usando ``twine upload dist/*``

Em caso de erro você terá que criar um novo release pois o PyPI Warehouse `não permite reutilizar um nome de arquivo <https://upload.pypi.org/help/#file-name-reuse>`_.

Changelog
---------

1.0b2 (2014-02-16)
^^^^^^^^^^^^^^^^^^

  * Oculta upgrade steps
    [ericof]

  * Ajustes de estilo no pacote.
    [ericof]

  * Corrige o problema com AgendaDiaria utilizando o campo date diretamente
    do default_factory ao inves de armazenar o valor dentro do objeto.
    [ericof]

  * Revisão do tile agenda (closes `#23`_).
    [rodfersou]

  * Correções gerais no tile de agenda (closes `#12`_).
    [rodfersou]

  * Acertos no portlet de busca (closes `#18`_).
    [dbarbato]


1.0b1 (2013-12-12)
^^^^^^^^^^^^^^^^^^

  * Backend do tile da agenda (closes `#12`_).
    [rodfersou]

  * Template e CSS do tile agenda (closes `#12`_).
    [rennan]


1.0a3 (2013-11-18)
^^^^^^^^^^^^^^^^^^
  * Exibe a mensagem de "Sem compromissos oficiais." apenas se
    nao tivermos compromissos e o campo atualizacao nao
    estiver preenchido
    [ericof]

  * A visão padrão de Agenda agora exibe a AgendaDiaria
    do dia se estiver publicada ou a mais recente.
    [ericof]

  * Título de AgendaDiaria fica no formato
    "Agenda de <autoridade> para <data>"
    [ericof]

  * Adicionado indice location ao portal_catalog
    [ericof]


1.0a2 (2013-11-04)
^^^^^^^^^^^^^^^^^^

  * Campo atualização do tipo AgendaDiaria agora é RichText
    [ericof]

  * Adiciona validação para data de AgendaDiaria
    [ericof]

  * Implementa relatório de coverage dos testes
    [hvelarde]

1.0a1 (2013-10-29)
^^^^^^^^^^^^^^^^^^

  * Estilização de css, templates e portlets laterais (closes `#3`_).
    [felipeduardo]

  * Exibicao dos campos na view de agenda diaria (closes `#1`_).
    [dbarbato]

  * Versão inicial do pacote.
    [ericof]

.. _`#1`: https://github.com/plonegovbr/brasil.gov.agenda/issues/1
.. _`#3`: https://github.com/plonegovbr/brasil.gov.agenda/issues/3
.. _`#12`: https://github.com/plonegovbr/brasil.gov.agenda/issues/12
.. _`#18`: https://github.com/plonegovbr/brasil.gov.agenda/issues/18
.. _`#23`: https://github.com/plonegovbr/brasil.gov.agenda/issues/23

Changelog
---------

1.1.1 (2017-11-08)
^^^^^^^^^^^^^^^^^^

- Corrige testes de Robot Framework.
  [hvelarde]


1.1 (2017-07-07)
^^^^^^^^^^^^^^^^

- plone.app.contenttypes usa a pinagem do Plone (atualmente 1.1.1)
  [idgserpro]


1.0.1 (2016-03-04)
^^^^^^^^^^^^^^^^^^

- A lista de dependências do pacote foi atualizada.
  [hvelarde]

- Corrige problema de compatibilidade com o plone.dexterity > 2.2.3;
  o pacote agora é compatível com o Plone > 4.3.3 (closes `#32`_).
  [hvelarde]


1.0 (2015-09-03)
^^^^^^^^^^^^^^^^

* Teste robot para navegação entre meses do portlet de calendário extendido.
  [idgserpro]

* Melhora estrutura de internacionalização, code-analysis e adiciona tradução
  em inglês.
  [idgserpro]

* Corrige css de impressão indicando que as regras só devem ser aplicadas se o tipo for Agenda Diária (closes `#37`_).
  [idgserpro]

* Corrige bug de navegação entre meses no portlet de calendário extendido após alteração de melhorias.
  [dbarbato]


1.0rc2 (2014-12-05)
^^^^^^^^^^^^^^^^^^^

* Altera indexação da data de publicação para funcionar com busca facetada.
  ``AgendaDiaria`` retorna agora a data de inicio do evento ao invés da data de publicação.
  [rodfersou]

* Adiciona ``Agenda``, ``AgendaDiaria`` e ``Compromisso`` aos tipos de conteúdo linkables no TinyMCE.
  [hvelarde]

* Corrige Portlet Calendário para mostrar o mês da ``AgendaDiaria`` ou ``Compromisso`` visualizado.
  [rodfersou]

* Altera evento no Portlet Calendário para ficar mais visível a data do evento.
  [rodfersou, agnogueira, hvelarde]

* Corrige bug de navegação entre meses no portlet de calendário extendido.
  [dbarbato]


1.0rc1 (2014-09-22)
^^^^^^^^^^^^^^^^^^^

* Remove AgendaDiaria e Compromisso da navegação.
  [ericof]

* Provê um portlet de calendário que linka direto para a agendadiaria.
  [ericof]

* A data de efetivação de uma AgendaDiaria publicada para datas futuras será a data atual.
  Para AgendaDiaria com data no passado, a data de efetivação sera a própria data de início da AgendaDiaria.
  [ericof]

* Visão padrão de agenda agora exibe a AgendaDiaria para a data corrente.
  Se não houve AgendaDiaria, exibimos uma mensagem
  [ericof]

* Remove limite de altura para compromissos no tile de Agenda.
  [ericof]

* Agenda, AgendaDiaria e Compromisso agora suportam Tags.
  [ericof]

* Adiciona testes para upgrade steps.
  [ericof]

* Adiciona teste para behavior de NameFromDate
  [ericof]

1.0b3 (2014-02-28)
^^^^^^^^^^^^^^^^^^

* Aumenta cobertura de testes para os tiles.
  [dbarbato]

* Aumenta cobertura de testes.
  [ericof]

* Renomeia pacote (profile) para .gov.br.
  [ericof]

* Oculta upgrade steps.
  [dbarbato]


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
.. _`#32`: https://github.com/plonegovbr/brasil.gov.agenda/issues/32
.. _`#37`: https://github.com/plonegovbr/brasil.gov.agenda/issues/37

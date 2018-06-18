Changelog
---------

2.0a2 (unreleased)
^^^^^^^^^^^^^^^^^^

.. Warning::
    Esta versão remove todos os upgrade steps do branch 1.x.
    Atualizações só serão suportadas da versão mais recente desse branch.
    Esta versão também remove a dependência no collective.portlet.calendar.
    Remova manualmente todos os portlets de calendario estendido e desinstale o pacote antes de atualizar.

- Remove dependência no collective.portlet.calendar.
  [hvelarde]

- Remove upgrade steps do branch 1.x.
  [hvelarde]

- Esconde checkbox de seleção de tipo compromisso na busca da agenda diária.
  [rodfersou]

- Remove parametros GET sem utilidade na agenda diária.
  [rodfersou]

- Melhora a compatibilidade futura com o Python 3;
  adiciona dependência no `six <https://pypi.python.org/pypi/six>`_.
  [hvelarde]

- Remove dependência no five.grok.
  [hvelarde]

- Remove atalhos para adicionar agendas diárias e compromissos.
  [hvelarde]

- Corrige tratamento de fuso horário na view padrão do tipo de conteúdo ``AgendaDiaria``;
  isso evita mudanças na hora dos compromissos em browsers com um fuso horário diferente do vigente no Brasil.
  [rodfersou, hvelarde]


2.0a1 (2018-06-06)
^^^^^^^^^^^^^^^^^^

- Adiciona dependência no plone4.csrffixes e corrige testes.
  [rodfersou]

- Atualiza layout e funcionalidades da view de Agenda.
  [rodfersou]

- Remove registro de subscribers durante migração de conteúdo;
  isso evita erros na importação dos compromissos de uma agenda.
  [hvelarde]

- Remove dependência no five.grok da declaração de subscribers.
  [hvelarde]

- Atualiza layout e funcionalidades do tile de Agenda.
  [rodfersou]

- Adiciona suporte para processamento de recursos estáticos usando o `webpack`_.
  [rodfersou]

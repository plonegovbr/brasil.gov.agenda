Changelog
---------

2.0a2 (unreleased)
^^^^^^^^^^^^^^^^^^

- Corrige tratamento de fuso horário na view padrão do tipo de conteúdo ``AgendaDiaria``;
- Remove atalhos para adicionar agendas diárias e compromissos.
  [hvelarde]

- Corrije tratamento de fuso horário na view padrão do tipo de conteúdo ``AgendaDiaria``;
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

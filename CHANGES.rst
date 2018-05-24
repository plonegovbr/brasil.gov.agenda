Changelog
---------

2.0a1 (unreleased)
^^^^^^^^^^^^^^^^^^

- Corrige ``WrongType`` ao tentar editar agendas sem tags (fecha `#85 <https://github.com/plonegovbr/brasil.gov.agenda/issues/85>`_).
  [hvelarde]

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

- Adiciona suporte para processamento de recursos estáticos usando o `webpack <http://webpack.js.org/>`_.
  [rodfersou]

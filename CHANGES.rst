Changelog
---------

2.0b2 (2019-04-05)
^^^^^^^^^^^^^^^^^^

- Acrestenta o campo 'Solicitante' no tipo de conteúdo ``Compromisso``. 
  (closes `#plonegovbr/brasil.gov.agenda#153 <https://github.com/plonegovbr/brasil.gov.agenda/issues/153>`_).
  [idgserpro]

- Remove o campo ``subjects`` do tipos de conteúdo ``Compromisso`` por ser considerado `desnecessário <https://listas.interlegis.gov.br/pipermail/plonegov-br/2018-June/004767.html>`_.
  [hvelarde]


2.0b1 (2018-11-23)
^^^^^^^^^^^^^^^^^^

- Remove registro de recursos estaticos dos resource registries;
  agora utilizamos um viewlet para incluir eles simplificando a manutenção do complemento.
  [rodfersou]

- Atualiza configuração do webpack.
  [rodfersou]

- Corrige o tile de Agenda quando a lingua é diferente de Português Brasileiro (fecha `#149 <https://github.com/plonegovbr/brasil.gov.agenda/issues/149>`_).
  [rodfersou]


2.0a7 (2018-09-28)
^^^^^^^^^^^^^^^^^^

.. warning::
    Este release atualiza as dependências do processamento de recursos estáticos.
    Em ambiente de desenvolvimento pode ser necessário remover as pastas ``parts`` e ``webpack/node_modules`` para efetivar a atualização de ambiente.

- Atualiza traduções ao Português Brasileiro.
  [hvelarde]

- Simplifica visão de agenda.
  [rodfersou]

- Corrige título da agenda diária caso o nome da pessoa no cargo mudar (fecha `#142 <https://github.com/plonegovbr/brasil.gov.agenda/issues/142>`_).
  [hvelarde]

- Evita a emissão de source maps dos recursos estáticos.
  [hvelarde]

- Atualiza versões do `Node.js <https://nodejs.org/>`_ e sc.recipe.staticresources.
  [rodfersou]


2.0a6 (2018-08-31)
^^^^^^^^^^^^^^^^^^

- Evita ``UnicodeDecodeError`` no título da agenda diária.
  [hvelarde]

- Adiciona dependência soft no collective.portlet.calendar para remover browser layer obsoleto (fecha `#137 <https://github.com/plonegovbr/brasil.gov.agenda/issues/137>`_).
  [hvelarde]


2.0a5 (2018-07-20)
^^^^^^^^^^^^^^^^^^

- Corrige o campo atualização ao navegar pelos dias.
  [rodfersou]


2.0a4 (2018-07-06)
^^^^^^^^^^^^^^^^^^

.. Warning::
    Esta versão inabilita o uso do portlet de Busca de Agenda.
    Remova manualmente todos os portlets de Busca de Agenda antes de atualizar.

- Ajustes gerais de layout.
  [agnogueira, rodfersou]

- O portlet de Busca de Agenda foi inabilitado e será completamente removido na versão 3.0.
  [hvelarde]

- Corrige dependências do pacote.
  [hvelarde]

- Limpeza e reorganização do código.
  [hvelarde, rodfersou]


2.0a3 (2018-06-28)
^^^^^^^^^^^^^^^^^^

- Remove o registro condicional de subscribers incluído no release 2.0a1.
  [hvelarde]

- Marca dias com compromissos nos calendários (fecha `#118 <https://github.com/plonegovbr/brasil.gov.agenda/issues/118>`_).
  [rodfersou]

- Adiciona listagem de agendas diárias ao acessar agenda quando estiver autenticado.
  [rodfersou]

- Corrige ações para editar e apagar compromisso.
  [rodfersou]

- Corrige alinhamento do titulo do calendário.
  [rodfersou]


2.0a2 (2018-06-18)
^^^^^^^^^^^^^^^^^^

.. Warning::
    Esta versão remove todos os upgrade steps do branch 1.x.
    Atualizações só serão suportadas da versão mais recente desse branch.
    Esta versão também remove a dependência no collective.portlet.calendar.
    Remova manualmente todos os portlets de calendario estendido e desinstale o pacote antes de atualizar.

- Corrige mensagem de agenda vazia quando não existem compromissos.
  [rodfersou]

- Corrige a busca de compromissos na agenda.
  [hvelarde]

- Corrige funcionamento da view padrão do tipo de conteúdo ``AgendaDiaria`` para evitar `problemas com proxies intermediárias <https://community.plone.org/t/6658>`_.
  [rodfersou]

- Remove dependência no collective.portlet.calendar;
  o layout do IDG 2.x não faz uso de portlets.
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

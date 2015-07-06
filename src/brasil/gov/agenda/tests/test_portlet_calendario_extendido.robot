*** Settings ***

Resource  brasil/gov/agenda/tests/keywords.robot

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${id_agenda} =  agenda-do-presidente

*** Test cases ***

 Test Navegacao Portlet Calendario
    Enable Autologin as  Site Administrator
    Go to homepage

    Create Agenda  Agenda do Presidente  Esta é a agenda do presidente  Machado de Assis
    Workflow Publish
    # Deve ser criada a Agenda Diária para o dia de hoje para testar a
    # navegação do portlet após redirecionamento. Ver abaixo.
    Create AgendaDiaria  ${DIA_ATUAL}  ${MES_ATUAL}  ${ANO_ATUAL}
    Workflow Publish
    Add Portlet Calendario Extendido  Portlet Calendario Extendido  /${id_agenda}
    Go to   ${PLONE_URL}/${id_agenda}
    # Verifica se há um link para agenda do dia atual
    Page Should Contain Element  css=a[title="Agenda"]

    Test Navegacao Portlet Calendario Extendido  ${PLONE_URL}/${id_agenda}

    # Teste com usuário anônimo.
    Disable autologin

    # Quando acessamos uma Agenda com usuário anônimo e existe uma Agenda
    # Diária para o dia de hoje, ocorre um redirecionamento para a Agenda
    # Diária de hoje. Aqui testamos a navegação com esse redirecionamento.
    Go to   ${PLONE_URL}/${id_agenda}
    # Verifica se há um link para agenda do dia atual
    Page Should Contain Element  css=a[title="Agenda"]

    Test Navegacao Portlet Calendario Extendido  ${PLONE_URL}/${id_agenda}

    # Agora testamos a navegação sem o redirecionamento.
    Test Navegacao Portlet Calendario Extendido  ${PLONE_URL}

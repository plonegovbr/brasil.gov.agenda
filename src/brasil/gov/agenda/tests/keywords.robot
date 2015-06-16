*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote
Variables  brasil/gov/agenda/tests/variables.py

*** Variables ***

${title_selector} =  input#form-widgets-IBasic-title
${description_selector} =  textarea#form-widgets-IBasic-description
${autoridade_selector} =  input#form-widgets-autoridade
${orgao_selector} =  input#form-widgets-orgao
${date_day_selector} =  input#form-widgets-date-day
${date_month_selector} =  select#form-widgets-date-month
${date_year_selector} =  input#form-widgets-date-year
${title_extended_calendar_selector} =  input#form\\.name
${mes_anterior_selector} =  a#calendar-previous
${mes_posterior_selector} =  a#calendar-next

*** Keywords ***

Click Adicionar Agenda
    Open Add New Menu
    Click Link  css=a#agenda
    Page Should Contain  Adicionar Agenda

Click Adicionar AgendaDiaria
    Open Add New Menu
    Click Link  css=a#agendadiaria
    Page Should Contain  Adicionar Agenda Diária

Create Agenda
    [arguments]  ${title}  ${description}  ${autoridade}

    Click Adicionar Agenda
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Input Text  css=${autoridade_selector}  ${autoridade}
    Input Text  css=${orgao_selector}  Presidência da República
    Click Button  Salvar
    Page Should Contain  Item criado

Create AgendaDiaria
    [arguments]  ${dia}  ${mes}  ${ano}

    Click Adicionar AgendaDiaria
    Input Text  css=${date_day_selector}  ${dia}
    Input Text  css=${date_year_selector}  ${ano}
    Select From List  css=${date_month_selector}  ${mes}
    Click Button  Salvar
    Page Should Contain  ${dia}
    Page Should Contain  de
    Page Should Contain  ${ano}

Manage Portlets
    Go to   ${PLONE_URL}/@@manage-portlets

Add Right Portlet
    [arguments]  ${portlet}
    Manage Portlets
    Select from list  xpath=//div[@id="portletmanager-plone-rightcolumn"]//select  ${portlet}

Add Portlet Calendario Extendido
    [arguments]  ${title}  ${raiz}
    Add Right Portlet  Extended Calendar portlet
    Input Text  css=${title_extended_calendar_selector}  ${title}
    Select Checkbox  css=input[value="${raiz}"]
    Click Button  Atualizar
    Click Button  Salvar

Click Mes Anterior
    Click Link  css=${mes_anterior_selector}

Click Mes Posterior
    Click Link  css=${mes_posterior_selector}

Test Navegacao Portlet Calendario Extendido
   [arguments]  ${url}
    Go to  ${url}

    # Testa navegação para o mês anterior
    Click Mes Anterior
    Page Should Contain Element  css=#calendar-previous[data-month="${DOIS_MESES_ANTERIORES}"]
    Page Should Contain Element  css=#calendar-next[data-month="${MES_ATUAL}"]

    # Testa navegação para o mês posterior
    Click Mes Posterior
    Click Mes Posterior
    Page Should Contain Element  css=#calendar-previous[data-month="${MES_ATUAL}"]
    Page Should Contain Element  css=#calendar-next[data-month="${DOIS_MESES_POSTERIORES}"]

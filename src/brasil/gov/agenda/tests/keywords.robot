*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote
Variables  brasil/gov/agenda/tests/variables.py

*** Variables ***

${title_selector} =  input#form-widgets-IBasic-title
${description_selector} =  textarea#form-widgets-IBasic-description
${autoridade_selector} =  input#form-widgets-autoridade
${orgao_selector} =  input#form-widgets-orgao
${date_day_selector} =  select#form-widgets-date-day
${date_month_selector} =  select#form-widgets-date-month
${date_year_selector} =  select#form-widgets-date-year
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
    Select From List  css=${date_day_selector}  ${dia}
    Select From List  css=${date_year_selector}  ${ano}
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

Test Navegacao Portlet Calendario Extendido
    [arguments]  ${url}
    Go to  ${url}

    # need to slow down Selenium here to avoid errors on calendar portlet
    ${speed} =  Set Selenium Speed  2 seconds

    # Testa navegação para o mês anterior
    Click Link  css=${mes_anterior_selector}
    Wait Until Page Contains Element  css=#calendar-previous[data-month="${DOIS_MESES_ANTERIORES}"]
    Wait Until Page Contains Element  css=#calendar-next[data-month="${MES_ATUAL}"]

    # Testa navegação para o mês posterior
    Click Link  css=${mes_posterior_selector}
    Click Link  css=${mes_posterior_selector}
    Wait Until Page Contains Element  css=#calendar-previous[data-month="${MES_ATUAL}"]
    Wait Until Page Contains Element  css=#calendar-next[data-month="${DOIS_MESES_POSTERIORES}"]

    Set Selenium Speed  ${speed}

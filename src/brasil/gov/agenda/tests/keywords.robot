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

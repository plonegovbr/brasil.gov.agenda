*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote

*** Variables ***

${title_selector} =  input#form-widgets-IBasic-title
${title_compromisso_selector} =  input#form-widgets-title
${description_selector} =  textarea#form-widgets-IBasic-description
${description_compromisso_selector} =  textarea#form-widgets-description
${autoridade_selector} =  input#form-widgets-autoridade
${orgao_selector} =  input#form-widgets-orgao
${date_day_selector} =  select#form-widgets-date-day
${date_month_selector} =  select#form-widgets-date-month
${date_year_selector} =  select#form-widgets-date-year
${start_day_selector} =  select#form-widgets-start_date-day
${start_month_selector} =  select#form-widgets-start_date-month
${start_year_selector} =  select#form-widgets-start_date-year
${end_day_selector} =  select#form-widgets-end_date-day
${end_month_selector} =  select#form-widgets-end_date-month
${end_year_selector} =  select#form-widgets-end_date-year

*** Keywords ***

Click Adicionar Agenda
    Open Add New Menu
    Click Link  css=a#agenda
    Page Should Contain  Adicionar Agenda

Click Adicionar AgendaDiaria
    Wait Until Page Contains Element  css=a#agendadiaria
    Open Add New Menu
    Click Link  css=a#agendadiaria
    Page Should Contain  Adicionar Agenda Diária

Click Adicionar Compromisso
    Wait Until Page Contains Element  css=a#compromisso
    Open Add New Menu
    Click Link  css=a#compromisso
    Page Should Contain  Adicionar Compromisso

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

Create Compromisso
    [arguments]  ${title}  ${description}  ${start_day}  ${start_month}  ${start_year}  ${end_day}  ${end_month}  ${end_year}

    Click Adicionar Compromisso
    Input Text  css=${title_compromisso_selector}  ${title}
    Input Text  css=${description_compromisso_selector}  ${description}
    Select From List  css=${start_day_selector}  ${start_day}
    Select From List  css=${start_year_selector}  ${start_year}
    Select From List  css=${start_month_selector}  ${start_month}
    Select From List  css=${end_day_selector}  ${end_day}
    Select From List  css=${end_year_selector}  ${end_year}
    Select From List  css=${end_month_selector}  ${end_month}
    Click Button  Salvar
    Page Should Contain  Voce vê esta página

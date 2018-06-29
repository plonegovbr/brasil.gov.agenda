*** Settings ***

Resource  brasil/gov/agenda/tests/keywords.robot
Variables  plone/app/testing/interfaces.py

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${title_basic_selector} =  input#form-widgets-IBasic-title
${description_basic_selector} =  textarea#form-widgets-IBasic-description
${title_selector} =  input#form-widgets-title
${description_selector} =  textarea#form-widgets-description
${autoridade_selector} =  input#form-widgets-autoridade
${orgao_selector} =  input#form-widgets-orgao
${attendees_selector} =  textarea#form-widgets-attendees
${start_day_selector} =  select#form-widgets-start_date-day
${start_month_selector} =  select#form-widgets-start_date-month
${start_year_selector} =  select#form-widgets-start_date-year
${start_hour_selector} =  select#form-widgets-start_date-hour
${start_min_selector} =  select#form-widgets-start_date-minute
${end_day_selector} =  select#form-widgets-end_date-day
${end_month_selector} =  select#form-widgets-end_date-month
${end_year_selector} =  select#form-widgets-end_date-year
${end_hour_selector} =  select#form-widgets-end_date-hour
${end_min_selector} =  select#form-widgets-end_date-minute


*** Test cases ***

Test CRUD
    Enable Autologin as  Site Administrator
    Go to homepage

    Create Agenda

    Create  Compromisso  Compromisso do dia
    Update  Compromisso  Compromisso do dia de hoje
    Delete

Test Default Values
    Enable Autologin as  Site Administrator
    Go to homepage

    Create Agenda

    Click Adicionar Compromisso
    Textfield Value Should Be  css=${autoridade_selector}  Clarice Lispector

Test Edit Delete Compromisso AgendaDiaria
    Enable Autologin as  Site Administrator
    Go to homepage

    Create Agenda
    Create  Júlio Verne  Compromisso do dia
    Click Link  Agenda de Clarice Lispector para 28/10/2013
    Page Should Contain  Júlio Verne
    Click Link  css=.editar_compromisso
    Input Text  css=${title_selector}  Madre Teresa
    Click Button  css=#form-buttons-save
    Wait Until Page Contains  Madre Teresa
    Click Link  css=.remover_compromisso
    Click Button  css=.destructive
    Wait Until Page Contains  Atualmente não existem compromissos agendados.

Test Highlight Appointments
    Enable Autologin as  Site Administrator
    Go to homepage

    Create Agenda

    Create  Compromisso  Compromisso do dia
    Click Link  Agenda de Clarice Lispector para 28/10/2013
    Wait Until Page Contains Element  css=td.ui-has-appointments


*** Keywords ***

Click Adicionar Compromisso
    Open Add New Menu
    Click Link  css=a#compromisso
    Page Should Contain  Adicionar Compromisso

Create Agenda
    Click Adicionar Agenda
    Input Text  css=${title_basic_selector}  Agenda da Presidenta
    Input Text  css=${description_basic_selector}  Agenda da Presidenta da República
    Input Text  css=${autoridade_selector}  Clarice Lispector
    Input Text  css=${orgao_selector}  Presidência da República
    Click Button  Salvar
    Page Should Contain  Item criado

Create
    [arguments]  ${title}  ${description}

    Click Adicionar Compromisso
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Select From List  css=${start_day_selector}  28
    Select From List  css=${start_year_selector}  2013
    Select From List  css=${start_month_selector}  10
    Select From List  css=${start_hour_selector}  1
    Select From List  css=${start_min_selector}  30
    Select From List  css=${end_day_selector}  28
    Select From List  css=${end_year_selector}  2013
    Input Text  css=${attendees_selector}  Machado de Assis
    Select From List  css=${end_month_selector}  10
    Select From List  css=${end_hour_selector}  2
    Select From List  css=${end_min_selector}  00
    Click Button  Salvar
    Page Should Contain  28
    Page Should Contain  de
    Page Should Contain  2013

Update
    [arguments]  ${title}  ${description}

    Click Link  link=Edição
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Click Button  Salvar
    Page Should Contain  Alterações salvas

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Excluir
    Page Should Contain  Agenda

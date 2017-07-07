*** Settings ***

Resource  brasil/gov/agenda/tests/keywords.robot
Variables  plone/app/testing/interfaces.py

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${title_basic_selector} =  input#form-widgets-IBasic-title
${description_basic_selector} =  textarea#form-widgets-IBasic-description
${autoridade_selector} =  input#form-widgets-autoridade
${orgao_selector} =  input#form-widgets-orgao
${date_day_selector} =  select#form-widgets-date-day
${date_month_selector} =  select#form-widgets-date-month
${date_year_selector} =  select#form-widgets-date-year

*** Test cases ***

Test CRUD
    Enable Autologin as  Site Administrator
    Go to homepage

    Create Agenda

    Create AgendaDiaria  05  2  2013
    Update  17  10  2013
    Delete

Test Default Values
    Enable Autologin as  Site Administrator
    Go to homepage

    Create Agenda

    Click Adicionar AgendaDiaria
    Textfield Value Should Be  css=${autoridade_selector}  Clarice Lispector

Test Data Duplicada
    Enable Autologin as  Site Administrator
    Go to homepage

    Create Agenda

    Create AgendaDiaria  05  2  2013

    Click Link  Agenda da Presidenta

    Click Adicionar AgendaDiaria
    Select From List  css=${date_day_selector}  05
    Select From List  css=${date_year_selector}  2013
    Select From List  css=${date_month_selector}  2
    Click Button  Salvar
    Page Should Contain  Existem alguns erros

Test AgendaDiaria With Portlet
    Enable Autologin as  Site Administrator
    Go to homepage

    Add Right Portlet  Calendário
    Go to homepage

    Create Agenda

    Create AgendaDiaria  05  2  2013
    Page Should Contain    Fevereiro


*** Keywords ***
Create Agenda
    Click Adicionar Agenda
    Input Text  css=${title_basic_selector}  Agenda da Presidenta
    Input Text  css=${description_basic_selector}  Agenda da Presidenta da República
    Input Text  css=${autoridade_selector}  Clarice Lispector
    Input Text  css=${orgao_selector}  Presidência da República
    Click Button  Salvar
    Page Should Contain  Item criado

Update
    [arguments]  ${dia}  ${mes}  ${ano}

    Click Link  link=Edição
    Select From List  css=${date_day_selector}  ${dia}
    Select From List  css=${date_year_selector}  ${ano}
    Select From List  css=${date_month_selector}  ${mes}
    Click Button  Salvar
    Page Should Contain  Alterações salvas
    Page Should Contain  ${dia}
    Page Should Contain  de
    Page Should Contain  ${ano}

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Excluir
    Page Should Contain  Agenda

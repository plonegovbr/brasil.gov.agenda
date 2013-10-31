*** Settings ***

Library  Selenium2Library  timeout=10 seconds  implicit_wait=5 seconds
Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${title_basic_selector} =  input#form-widgets-IBasic-title
${description_basic_selector} =  textarea#form-widgets-IBasic-description
${autoridade_selector} =  input#form-widgets-autoridade
${orgao_selector} =  input#form-widgets-orgao
${date_day_selector} =  input#form-widgets-date-day
${date_month_selector} =  select#form-widgets-date-month
${date_year_selector} =  input#form-widgets-date-year


*** Test cases ***

Test CRUD
    Log in as site owner
    Go to homepage

    Create Agenda

    Create  05  2  2013
    Update  17  10  2013
    Delete

Test Default Values
    Log in as site owner
    Go to homepage

    Create Agenda

    Click Add AgendaDiaria
    Textfield Value Should Be  css=${autoridade_selector}  Clarice Lispector

Test Data Duplicada
    Log in as site owner
    Go to homepage

    Create Agenda

    Create  05  2  2013

    Click Link  Agenda da Presidenta

    Click Add AgendaDiaria
    Input Text  css=${date_day_selector}  05
    Input Text  css=${date_year_selector}  2013
    Select From List  css=${date_month_selector}  2
    Click Button  Save
    Page Should Contain  There were some errors


*** Keywords ***

Click Add Agenda
    Open Add New Menu
    Click Link  css=a#agenda
    Page Should Contain  Add Agenda

Click Add AgendaDiaria
    Open Add New Menu
    Click Link  css=a#agendadiaria
    Page Should Contain  Add Agenda Diaria

Create Agenda
    Click Add Agenda
    Input Text  css=${title_basic_selector}  Agenda da Presidenta
    Input Text  css=${description_basic_selector}  Agenda da Presidenta da República
    Input Text  css=${autoridade_selector}  Clarice Lispector
    Input Text  css=${orgao_selector}  Presidência da República
    Click Button  Save
    Page Should Contain  Item created

Create
    [arguments]  ${dia}  ${mes}  ${ano}

    Click Add AgendaDiaria
    Input Text  css=${date_day_selector}  ${dia}
    Input Text  css=${date_year_selector}  ${ano}
    Select From List  css=${date_month_selector}  ${mes}
    Click Button  Save
    Page Should Contain  ${dia}
    Page Should Contain  de
    Page Should Contain  ${ano}

Update
    [arguments]  ${dia}  ${mes}  ${ano}

    Click Link  link=Edit
    Input Text  css=${date_day_selector}  ${dia}
    Input Text  css=${date_year_selector}  ${ano}
    Select From List  css=${date_month_selector}  ${mes}
    Click Button  Save
    Page Should Contain  Changes saved
    Page Should Contain  ${dia}
    Page Should Contain  de
    Page Should Contain  ${ano}

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Agenda

*** Settings ***

Library  Selenium2Library  timeout=10 seconds  implicit_wait=5 seconds
Resource  plone/app/robotframework/keywords.robot
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
${start_day_selector} =  input#form-widgets-start_date-day
${start_month_selector} =  select#form-widgets-start_date-month
${start_year_selector} =  input#form-widgets-start_date-year
${start_hour_selector} =  input#form-widgets-start_date-hour
${start_min_selector} =  input#form-widgets-start_date-min
${end_day_selector} =  input#form-widgets-end_date-day
${end_month_selector} =  select#form-widgets-end_date-month
${end_year_selector} =  input#form-widgets-end_date-year
${end_hour_selector} =  input#form-widgets-end_date-hour
${end_min_selector} =  input#form-widgets-end_date-min


*** Test cases ***

Test CRUD
    Log in as site owner
    Go to homepage

    Create Agenda

    Create  Compromisso  Compromisso do dia
    Update  Compromisso  Compromisso do dia de hoje
    Delete

Test Default Values
    Log in as site owner
    Go to homepage

    Create Agenda

    Click Add Compromisso
    Textfield Value Should Be  css=${autoridade_selector}  Clarice Lispector

*** Keywords ***

Click Add Agenda
    Open Add New Menu
    Click Link  css=a#agenda
    Page Should Contain  Add Agenda

Click Add Compromisso
    Open Add New Menu
    Click Link  css=a#compromisso
    Page Should Contain  Add Compromisso

Create Agenda
    Click Add Agenda
    Input Text  css=${title_basic_selector}  Agenda da Presidenta
    Input Text  css=${description_basic_selector}  Agenda da Presidenta da República
    Input Text  css=${autoridade_selector}  Clarice Lispector
    Input Text  css=${orgao_selector}  Presidência da República
    Click Button  Save
    Page Should Contain  Item created

Create
    [arguments]  ${title}  ${description}

    Click Add Compromisso
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Input Text  css=${start_day_selector}  28
    Input Text  css=${start_year_selector}  2013
    Select From List  css=${start_month_selector}  10
    Input Text  css=${start_hour_selector}  13
    Input Text  css=${start_min_selector}  30
    Input Text  css=${end_day_selector}  28
    Input Text  css=${end_year_selector}  2013
    Select From List  css=${start_month_selector}  10
    Input Text  css=${end_hour_selector}  14
    Input Text  css=${end_min_selector}  00
    Click Button  Save
    Page Should Contain  28
    Page Should Contain  de
    Page Should Contain  2013

Update
    [arguments]  ${title}  ${description}

    Click Link  link=Edit
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Click Button  Save
    Page Should Contain  Changes saved

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Agenda

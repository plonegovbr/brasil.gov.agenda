*** Settings ***

Library  Selenium2Library  timeout=10 seconds  implicit_wait=5 seconds
Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${title_selector} =  input#form-widgets-IBasic-title
${description_selector} =  textarea#form-widgets-IBasic-description
${autoridade_selector} =  input#form-widgets-autoridade
${orgao_selector} =  input#form-widgets-orgao

*** Test cases ***

Test CRUD
    Log in as site owner
    Go to homepage

    Create  Agenda do Presidente  Esta é a agenda do presidente  Machado de Assis
    Update  Agenda da Presidenta  Esta é a agenda da presidenta  Clarice Lispector
    Delete

*** Keywords ***

Click Add Agenda
    Open Add New Menu
    Click Link  css=a#agenda
    Page Should Contain  Add Agenda

Create
    [arguments]  ${title}  ${description}  ${autoridade}

    Click Add Agenda
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Input Text  css=${autoridade_selector}  ${autoridade}
    Input Text  css=${orgao_selector}  Presidência da República
    Click Button  Save
    Page Should Contain  Item created

Update
    [arguments]  ${title}  ${description}  ${autoridade}

    Click Link  link=Edit
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Input Text  css=${autoridade_selector}  ${autoridade}
    Input Text  css=${orgao_selector}  Presidência da República
    Click Button  Save
    Page Should Contain  Changes saved

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Plone site
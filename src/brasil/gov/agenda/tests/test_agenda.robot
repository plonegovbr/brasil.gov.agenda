*** Settings ***

Resource  brasil/gov/agenda/tests/keywords.robot
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
    Enable Autologin as  Site Administrator
    Go to homepage

    Create Agenda  Agenda do Presidente  Esta é a agenda do presidente  Machado de Assis
    Update  Agenda da Presidenta  Esta é a agenda da presidenta  Clarice Lispector
    Delete

*** Keywords ***

Update
    [arguments]  ${title}  ${description}  ${autoridade}

    Click Link  link=Edição
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Input Text  css=${autoridade_selector}  ${autoridade}
    Input Text  css=${orgao_selector}  Presidência da República
    Click Button  Salvar
    Page Should Contain  Alterações salvas

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Excluir
    Page Should Contain  Plone site

*** Settings ***

Resource  brasil/gov/agenda/tests/keywords.robot

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${day_selector} =  //a[contains(@class, 'ui-state-default')][text()='10']

*** Test cases ***

Test Clica Dia
    Enable Autologin as  Site Administrator
    Go to homepage

    Create Agenda  Agenda do Presidente  Esta é a agenda do presidente  Machado de Assis
    Create Compromisso  Compromisso  Descrição  10  10  2019  10  10  2019
    Click Link  Agenda do Presidente
    Create Compromisso  Compromisso  Descrição  11  10  2019  11  10  2019
    Click Link  Agenda de Machado de Assis para 11/10/2019
    Element Should Become Visible  xpath=${day_selector}
    Click Element  xpath=${day_selector}
    # Ao clicar no dia, o dia corrente não pode ir para o treceiro calendário .ui-datepicker-group-last
    Page Should Not Contain Element  css=.ui-datepicker-group-last .ui-datepicker-current-day

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
${layout_selector} =  select#form-widgets-template_layout


${tile_agenda_selector} =  div.tile-container div.agenda-tile
${tile_selector} =  select#form-widgets-available_tiles-from
${agenda_selector}  .ui-draggable .contenttype-agenda
${agenda_tile_location}  'agenda'
${row_button_selector} =  a#btn-row
${column_button_selector} =  a#btn-column
${tile_button_selector} =  a#btn-tile
${row_drop_area_selector} =  div.layout
${column_drop_area_selector} =  div.cover-row
${tile_drop_area_selector} =  div.cover-column
${tile_cancel_area_selector} =  div.modal-backdrop
${delete_tile_selector} =  button.close
${CONTENT_CHOOSER_SELECTOR} =  div#contentchooser-content-search

*** Test cases ***

Test CRUD
    Log in as site owner
    Go to homepage

    # Create Agenda
    Create Agenda  Agenda do Presidente  Esta é a agenda do presidente  Machado de Assis

    # Allow Agenda Tile to be inserted
    Configure Cover

    # Create Cover
    Go to homepage
    Create Cover  Title  Description  Empty layout
    
    # Insert Agenda Tile into Cover
    Edit Cover Layout
    Page Should Contain  Export layout
    Add Tile  ${agenda_tile_location}
    Save Cover Layout

    # as tile is empty, we see default message
    Compose Cover
    Page Should Contain  Please drag&drop some content here to populate the tile

    # drag&drop an Agenda
    Open Content Chooser


    # quebrando aqui
    #
    #
    # acho que precisa clicar no ícone por árvore
    # para exibir a agenda

    Sleep  1s
    Click Link  link=Content tree
    Drag And Drop  css=${agenda_selector}  css=${tile_agenda_selector}
    Sleep  1s
    Page Should Contain  Agenda do Presidente

    # move to the default view and check tile persisted
    Click Link  link=View
    Page Should Contain  Agenda do Presidente

    # Deleta Cover
    Delete

*** Keywords ***

Configure Cover
    Goto  ${PLONE_URL}/@@cover-settings
    Select From List  css=${tile_selector}  Agenda
    Sleep  1s
    Click Button  from2toButton
    Sleep  1s
    Click Button  form-buttons-save

Click Add Agenda
    Open Add New Menu
    Click Link  css=a#agenda
    Page Should Contain  Add Agenda

Create Agenda
    [arguments]  ${title}  ${description}  ${autoridade}

    Click Add Agenda
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Input Text  css=${autoridade_selector}  ${autoridade}
    Input Text  css=${orgao_selector}  Presidência da República
    Click Button  Save
    Page Should Contain  Item created

Create Cover
    [arguments]  ${title}  ${description}  ${layout}

    Click Add Cover
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Select From List  css=${layout_selector}  ${layout}
    Click Button  Save
    Page Should Contain  Item created

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Plone site

Click Add Cover
    Open Add New Menu
    Click Link  css=a#collective-cover-content
    Page Should Contain  Add Cover

Edit Cover Layout
    [Documentation]  Click on Layout tab and wait until the layout has been
    ...              loaded. Buttons related with layout operations must be
    ...              also visible.
    Click Link  link=Layout
    Sleep  1s  Wait for cover layout to load
    Page Should Contain  Export layout
    Page Should Contain  Saved

Save Cover Layout
    [Documentation]  Click on Save button and wait until layout has been
    ...              saved.
    Page Should Contain  Save
    Click Element  css=a#btn-save.btn
    Wait Until Page Contains  Saved

Add Tile
    [arguments]  ${tile}

    Drag And Drop  xpath=//a[contains(@data-tile-type, ${tile})]  css=${tile_drop_area_selector}
    Wait Until Page Contains Element  css=.tile-name

Compose Cover
    [Documentation]  Click on Compose tab and wait until the layout has been
    ...              loaded.
    Click Link  link=Compose
    Sleep  1s  Wait for cover compose to load
    Wait Until Page Contains Element  css=div#contentchooser-content-show-button
    Page Should Contain  Add Content

Open Content Chooser
    Click Element  css=div#contentchooser-content-show-button
    Wait Until Page Contains Element  css=${CONTENT_CHOOSER_SELECTOR}
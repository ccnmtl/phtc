Feature: Hide Section

Tests to check that students/admins/etc see only the 
Secitons/Modules that they are supposed to see in 
the dashboard


    Scenario: Admin Can see the hidden module
        Using selenium
        When I access the url "/"
        Given I am logged out
        Then I re-login as an admin
        When I access the url "/edit/module-1/"
        And go to module one edit screen
        Then I click the edit button
        And submit hide in the section css
        Then module 1 has css class of hide

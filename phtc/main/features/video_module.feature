Feature: Video Module

Tests to check that the admin has the ability to place a link to the module
in the dashboard underneath the Video Module headign, thus seperating it 
from the sequential learning modules

    Scenario: Admin can move module to the Video Section
        Given I am logged out
        Then I re-login as an admin
        When I access the url "/edit/module-2/"
        And go to module two edit screen
        Then I click the edit button
        And submit video in the module type
        Then module 2 is now under video section

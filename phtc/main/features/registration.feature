Feature: Registration Form

    Scenario: Form Basics
        When I access the url "/registration/register/"
        Then I see the h3 "Create a new PHTC account"

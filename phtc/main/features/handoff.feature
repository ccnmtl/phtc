Feature: Handoff

Tests to check that users coming from NYLearns are being redirected
to the correct place

    Scenario: Student is logged into PHTC and clicks a NYLearns link
    	Using selenium
        Given I am logged as a student
        When I access the handoff url "/nynj/?course=0102&userID=123&usrnm=test"
        Then I see the handoff module "0102"
    
    Scenario: New NYNJ user clicks on link from the NYLearns Site going to PHTC
        Using selenium
        Given I am not logged in
        When I access the url "/nynj/?course=0102&userID=123&usrnm=test123"
        And I click on the link "Need a new account"
        And I fill out the form

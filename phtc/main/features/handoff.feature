Feature: Handoff

Tests to check that users coming from NYLearns are being redirected
to the correct place

    Scenario: Unregistered new NYNJ user clicks on link from the NYLearns Site going to PHTC
        Using selenium
        Given I am not logged in
        When I access the url "/nynj/?course=0102&userID=123&usrnm=test123"
        And it fails when I try to use my NYLearns login info
        And I click on the link "Need a new account"
        And I fill out the form
        Then I see the header "Dashboard" 
        Finished using selenium

    Scenario: Student is logged into PHTC and clicks a NYLearns link
    	Using selenium
        Given I am logged as a student
        When I access the handoff url "/nynj/?course=0102&userID=123&usrnm=test"
        Then I see the handoff module "0102"
        Finished using selenium
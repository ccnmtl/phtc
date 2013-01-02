Feature: Handoff

Tests to check that users coming from NYLearns are being redirected
to the correct place

    Scenario: Unregistered new NYLears user clicks on link from the NYLearns Site going to PHTC
        Using selenium
        Given I am not logged in
        When I access the url "/nylearns/?course=123&userID=123"
        And I click on the link "Need a new account?"
        And I fill out the form
        Then I see the handoff module "123" 
        Finished using selenium

    Scenario: Student is logged into PHTC and clicks a NYLearns link
    	Using selenium
        Given I am logged as a student
        When I access the handoff url "/nylearns/?course=123&userID=123"
        Then I see the handoff module "Introduction to Qualitative Research"
        Finished using selenium
Feature: Roles

Tests to check that students/admins/etc see only the things
that they are supposed to see

    Scenario: Student Does Not See Edit Link
        Given I am logged as a student
        When I access the url "/module-1/"
        Then I do not see an edit link

    Scenario: Admin Does See Edit Link
        Given I am logged in as an admin
        When I access the url "/module-1/"
#        Then I see an edit link
    
    Scenario: Logged out user does not see edit link
        Given I am not logged in
        When I access the url "/module-1/"
        Then I do not see an edit link

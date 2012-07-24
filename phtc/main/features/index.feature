Feature: Index Page

Just some simple sanity checks on the index page of the application
This also serves as a good test that the lettuce and selenium
stuff is all hooked up properly and running.

    Scenario: Index Page Load With Selenium
        Using selenium
        Given I am logged as a student
        When I access the url "/"
        Then I see the header "Dashboard"
        Finished using selenium

    Scenario: Index Page Load
        Given I am logged as a student
        When I access the url "/"
        Then I see the header "Dashboard"


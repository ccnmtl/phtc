Feature: Index Page

Just some simple sanity checks on the index page of the application
This also serves as a good test that the lettuce and selenium
stuff is all hooked up properly and running.

    Scenario: Index Page Load With Selenium
        Using selenium
        When I access the url "/"
        Then I see the header "module 1"
        Finished using selenium

    Scenario: Index Page Load
        When I access the url "/"
        Then I see the header "module 1"


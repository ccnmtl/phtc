Feature: Question Label can Contain HTML

    Scenario: Place an Image Tag in the Label Field
        Using selenium
        When I access the url "/"
        Given I am logged out
        Then I re-login as an admin
        When I access the url "/edit/module-1/three/evaluation/"
        And I insert an image in the label field of a question 
        



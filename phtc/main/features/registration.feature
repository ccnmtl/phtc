Feature: Registration Form

    Scenario: Form Basics
        When I access the url "/registration/register/"
        Then I see the h3 "Create a new PHTC account"
        Then there is an "id_username" field
        Then there is an "id_email" field
        Then there is an "id_password1" field
        Then there is an "id_password2" field
        Then there is an "id_sex" select
        Then there is an "id_age" select
        Then there is an "id_origin" select
        Then there is an "id_ethnicity" select
        Then there is an "id_disadvantaged" select
        Then there is an "id_employment_location" select
        Then there is an "id_position" select
        Then there is a "Send activation email" submit button

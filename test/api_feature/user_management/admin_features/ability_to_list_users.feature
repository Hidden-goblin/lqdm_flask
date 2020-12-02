Feature: Admin can list users (User Management)

    As an administrator
    I want to list users
    So that I could manage them

    Scenario:
        Given I am "JohnDoe"
        When I list users
        Then I get "401" http status code
        And The error message is "You don't have access to this resource."

    Scenario:
        Given I am "ElsaWriter"
        And I am authenticated
        When I list users
        Then I get "403" http status code
        And The error message is "You are not allowed to access this resource."

    Scenario:
        Given I am "BobAdmin"
        And I am authenticated
        When I list users
        Then I get "200" http status code
        And At least "1" users


Feature: Admin can list users (User Management)

    As an administrator
    I want to list users
    So that I could manage them

    @error
    Scenario: Anomymous users cannot list users
        Given I am "JohnDoe"
        When I list users
        Then I get "401" http status code
        And The error message is "You don't have access to this resource."

    @error
    Scenario: Non admin users cannot list users
        Given I am "ElsaWriter"
        And I am authenticated
        When I list users
        Then I get "403" http status code
        And The error message is "You are not allowed to access this resource."

    Scenario: Admin user can list users
        Given I am "BobAdmin"
        And I am authenticated
        When I list users
        Then I get "200" http status code
        And I retrieve at least "1" users


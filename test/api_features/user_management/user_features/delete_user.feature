Feature: User can delete account (User Management)

    As an user
    I want to delete my account
    So that I won't appear in this application anymore

  Scenario: User delete his account
    Given I am "AlbusUser"
    And I have subscribed
    And I am authenticated
    When I delete "AlbusUser" user
    Then I get "204" http status code

  @error
  Scenario: Cannot remove the last admin account
    Given There is "1" account with role "Admin"
    And I am "BobAdmin"
    And  I am authenticated
    When I delete "BobAdmin" user
    Then I get "403" http status code
    And The error message is "Cannot delete account"
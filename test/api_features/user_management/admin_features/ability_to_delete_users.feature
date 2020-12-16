Feature: Admin can delete user (User Management)

    As an administrator
    I want to delete accounts
    So that they won't appear in this application anymore

  Scenario: Deleting an existing account
    Given "AlbusUser" exists
    And I am "BobAdmin"
    And I am authenticated
    When I delete "AlbusUser" user
    Then I get "204" http status code
    And The "AlbusUser" account "does not" exist


  @error
  Scenario: Cannot delete when not authenticated
    Given "AlbusUser" exists
    And I am "BobAdmin"
    When I delete "AlbusUser" user
    Then I get "401" http status code
    And The "AlbusUser" account "does" exist
Feature: User subscription
  As an user
  I want to subscribe
  So that I could access advanced features

  Scenario Outline: Mandatory field
    Given I am "RobinUser"
    And I forgive "<field>" field
    When I subscribe
    Then I get "<status>" http status code
    And I receive "<message>" message

    Examples: Missing mandatory
      | field    | message                 | status |
      | email    | email is mandatory      | 400    |
      | password | password is mandatory   | 400    |

    Examples: All provided
      | field | message                 |  status |
      | none  | subscription successful | 200     |


  Scenario: Existing user
    Given I am "RobinUser"
    And "TwinRobinUser" exists
    When I subscribe
    Then I receive "You cannot subscribe with this email" message
    And I get "400" http status code
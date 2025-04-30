Feature: Generate Unique ID

Scenario: With existing tasks
    Given I have a list of tasks
    When I generate a new ID
    Then the new ID is unique


Scenario: No existing tasks
    Given there are no tasks
    When I generate a new ID
    Then the new ID is 1


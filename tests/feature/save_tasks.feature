Feature: Save tasks

Scenario: Save tasks
    Given I have a list of tasks
    When I save the tasks
    Then the saved file exists


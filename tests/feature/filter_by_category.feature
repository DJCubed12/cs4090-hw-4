Feature: Filter by Category

Scenario: Work
    Given I have a list of tasks
    When I filter by Work category
    Then only tasks with Work category are left

Scenario: School
    Given I have a list of tasks
    When I filter by School category
    Then only tasks with School category are left

Scenario: Personal
    Given I have a list of tasks
    When I filter by Personal category
    Then only tasks with Personal category are left


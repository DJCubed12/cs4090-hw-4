Feature: Filter by Priority

Scenario: High
    Given I have a list of tasks
    When I filter by High priority
    Then only tasks with High priority are left

Scenario: Medium
    Given I have a list of tasks
    When I filter by Medium priority
    Then only tasks with Medium priority are left

Scenario: Low
    Given I have a list of tasks
    When I filter by Low priority
    Then only tasks with Low priority are left


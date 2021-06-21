# Created by Elias Ladenburger at 07.06.2021
Feature: Play Group Game
  Group Games are instances of scenarios and are played by more than one, non-authenticated participant.

  Background:
    Given a group game in progress
    Given 3 participants

  Scenario: Not all participants have solved an inject
    Given all participants see the same inject
    When one participant solves an inject
    Then the participant cannot solve another inject

  Scenario: Personalize a Group Game
    Given a participant that belongs to a target group
    And an inject hint that is defined for this target group
    When the participant sees this inject
    Then the participant should see the hint


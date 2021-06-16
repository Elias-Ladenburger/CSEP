# Created by Elias Ladenburger at 07.06.2021
Feature: Join Group Game
  Group Games are instances of scenarios. Before they can be played, participants must connect to a lobby

  Scenario: Join Open Game
    Given an open group game
    When a participant wants to join
    Then they enter the game lobby

  Scenario: Join Closed Game
    Given a closed group game
    When a participants wants to join
    Then the participant receives an error message

  Scenario: Join Full Game in Progress
    Given a group game in progress
    When a participant wants to join
    And the maximum number of participants has already been reached
    Then the participant receives an error message

  Scenario: Rejoin Group Game
    Given a group game in progress
    When a participant wants to join
    And the game currently has fewer participants than have started the game
    Then the participant joins for the current inject

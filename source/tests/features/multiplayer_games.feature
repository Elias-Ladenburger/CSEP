# Created by Elias Ladenburger at 07.06.2021
Feature: Group Game
  Group Games are instances of scenarios and are played by more than one, non-authenticated participant.

  Background:
    Given one inject
    And a choice to go to one target inject
    And one other inject.


  Scenario: Solve Choice Inject
    When the player selects choice number 0
    Then this choice must refer to the target inject.

  Scenario: Solve Choice Inject
    When the player selects choice number 1
    Then this choice must refer to the other inject.
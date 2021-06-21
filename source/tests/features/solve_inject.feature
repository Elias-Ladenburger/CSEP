# language: en
# Created by Elias Ladenburger at 07.06.2021

Feature: Solve Inject
  As a participant I want to be able to go from one inject to another to advance the storyline of a game.
  This may require me to do certain tasks (i.e. "solve" an inject).


  Scenario Template: Solve a Choice Inject
    Given one <source> inject to start from
    And a choice to go to one <target> inject
    And a choice to go to one <other> inject
    When the player selects choice at index <choice id>
    Then this choice must refer to the <valid> inject.
    Scenarios:
      | source | target | other | choice id  | valid |
      | starting | target | other | 0        | target |
      | starting | target | other | 1        | other |

  Scenario: Solve an Informative Inject
    Given one informative inject to start from
    And a choice to go to one target inject
    When the player selects choice at index 0
    Then this choice must refer to the target inject.

  Scenario: Make an Illegal Choice
    Given one source inject to start from
    And a choice to go to one target inject
    When the player selects choice at index 1
    Then this must throw an value error.

  Scenario: Solve Last Inject
    Given a learning scenario
    And a game in progress
    When the player selects choice at index 0
    Then the game must end.

# Created by Elias Ladenburger at 07.06.2021
Feature: Open Group Game
  Group Games are instances of scenarios. Before they can be facilitated, they must be opened by a trainer.

Background:
  Given a trainer
  And a learning scenario

Scenario: Open a Group Game
  When the trainer selects a scenario
  And selects "open group game"
  Then the trainer should see the lobby of the new game.

Scenario: Start a Group Game
  Given an open group game
  When the trainer select "start game"
  Then all participants see the same inject
  And the trainer sees all details of the game
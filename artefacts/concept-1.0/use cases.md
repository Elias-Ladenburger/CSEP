# Use Cases

## UC1.1 Play Game Alone

### Overview
A scenario is be played by a single learner.

### Actors
A learner. A learner can be authenticated or unauthenticated.

### Preconditions
At least one Scenario for single-player use exists.

### Successful Outcome(s)
The learner has completed the scenario.

### Alternative Outcomes
The learner has abandoned the scenario.

### Non-Scope
Saving scenario-progress will not be supported.

### Description
1. The learner starts the scenario.
1. The learner reads the scenario briefing.
1. Repeat until there are no more injects:
    1. The learner views an inject.
    1. The learner solves the inject [^1].
1. The learner receives feedback on their performance for the scenario.

### Alternatives 

### Assumptions

### Grounding

## UC1.2 Play Game in Group

### Overview
A scenario is played by a group of learners.

### Actors
- A learner. A learner can be authenticated or unauthenticated.
- A trainer. A trainer needs to be authenticated.

### Preconditions
At least one group scenario exists.

### Successful Outcome(s)
All learners of the group have completed the scenario.

### Alternative Outcomes
- One or more learners have abandoned the scenario.
- The trainer has canceled the scenario.

### Non-Scope
Saving scenario-progress will not be supported.

### Description
1. The trainer starts the scenario.
1. The learners access the scenario.
1. The learner read the scenario briefing.
1. Repeat until there are no more injects:
    1. Each learner views the next inject.
    1. Each learner solves the inject [^1].
    1. Wait until all learners have completed previous step.
    1. The trainer provides feedback on how the group reacted to this inject.
1. The trainer provides feedback on the group performance performance for the scenario.

### Alternatives 

### Assumptions

### Grounding

## UC1.2 Facilitate Group Game

### Overview
A scenario is played by a group of learners.

### Actors
- A learner. A learner can be authenticated or unauthenticated.
- A trainer. A trainer needs to be authenticated.

### Preconditions
At least one group scenario exists.

### Successful Outcome(s)
All learners of the group have completed the scenario.

### Alternative Outcomes
- One or more learners have abandoned the scenario.
- The trainer has canceled the scenario.

### Non-Scope
Saving scenario-progress will not be supported.

### Description
1. The trainer starts the scenario.
1. The learners access the scenario.
1. The learner read the scenario briefing.
1. Repeat until there are no more injects:
    1. Each learner views the next inject.
    1. Each learner solves the inject [^1].
    1. Wait until all learners have completed previous step.
    1. The trainer provides feedback on how the group reacted to this inject.
1. The trainer provides feedback on the group performance performance for the scenario.

### Alternatives 

### Assumptions

### Grounding

## UC2.1 Create Scenario

### Overview

### Actors
A scenario designer.

### Preconditions
- The user is authenticated. 
- The user has the role "scenario designer".
- The user has opened the "edit scenarios" view.

### Successful Outcome(s)
A scenario has been created.

### Alternative Outcomes
Creation of the scenario has been canceled.

### Non-Scope

### Description
1. The user selects "create scenario".
1. The user inserts a name of the scenario.
1. The user inserts a short description of the scenario.
1. (Optional:) the user uploads a thumbnail-image for the scenario.[^2]
1. The user adds a description of the target group for the scenario:
    1. Role[^3],
    1. Industry[^4] and
    1. Experience / Prior Knowledge.[^5]
1. (Optional:) The user adds tags for categorizing the scenario.
1. The user adds any number of stories.

### Alternatives 

### Assumptions

### Grounding

## UC2.2 Edit Scenario

### Overview

### Actors
A scenario designer.

### Preconditions
- The user is authenticated. 
- The user has the role "scenario designer".
- A scenario exists.

### Successful Outcome(s)
The scenario has been modified.

### Alternative Outcomes
Modification of the scenario has been canceled.

### Non-Scope
Editing scenario-statistics will not be possible.

### Description
1. The user selects an existing scenario.
1. The user selects "edit scenario".
1. The user performs one or more changes:
    1. change a name of the scenario.
    1. change the description of the scenario.
    1. change, add or delete the thumbnail-image for the scenario. 
    1. change the definition of the target group.
    1. edit any number of stories:
        1. edit story title.
        1. edit inject transitions.
        1. edit injects.
1. (Optional:) The user adds or deletes tags for categorizing the scenario.

### Alternatives 

### Assumptions
It should be possible to match scenario statistics to the version of a scenario, so as to compare effectiveness of modifications.

### Grounding

## UC2.3 Delete Scenario

### Overview

### Actors
A scenario designer.

### Preconditions
- The user is authenticated. 
- The user has the role "scenario designer".
- A scenario exists.

### Successful Outcome(s)
The scenario has been deleted.

### Alternative Outcomes
Deleting the scenario has been aborted.

### Non-Scope
Deleting specific versions (history) of a scenario will not be supported.

### Description
1. The user selects an existing scenario.
1. The user selects "delete scenario".
1. The user confirms their choice.

### Alternatives 
Instead of confirmation, the user selects "cancel".

### Assumptions

### Grounding

## UC3.1 View Game Results (Self)
### Overview

### Actors
A scenario designer.

### Preconditions
- The user is authenticated. 
- The user has the role "scenario designer".
- A scenario exists.

### Successful Outcome(s)
The scenario has been modified.

### Alternative Outcomes
Modification of the scenario has been canceled.

### Non-Scope

### Description

### Alternatives 

### Assumptions

### Grounding

## UC3.2 View Game Results (Other)
### Overview

### Actors
A scenario designer.

### Preconditions
- The user is authenticated. 
- The user has the role "scenario designer".
- A scenario exists.

### Successful Outcome(s)
The scenario has been modified.

### Alternative Outcomes
Modification of the scenario has been canceled.

### Non-Scope

### Description

### Alternatives 

### Assumptions

### Grounding

## UC4 View Scenario Statistics
### Overview

### Actors
A scenario designer.

### Preconditions
- The user is authenticated. 
- The user has the role "scenario designer".
- A scenario exists.

### Successful Outcome(s)
The scenario has been modified.

### Alternative Outcomes
Modification of the scenario has been canceled.

### Non-Scope

### Description

### Alternatives 

### Assumptions

### Grounding

## Footnotes
[^1]: "solving" an inject can be one of the following:
    * continue to end of scenario if inject links to no transition. 
    * continue to next inject if inject only links to one transition.
    * choose transition and continue to inject referenced by said transition if inject links to multiple transitions.
[^2]: The benefit of this step may need to be reevaluated in the future. It is likely to introduce a high level of complexity.
[^3]:
[^4]:
[^5]:
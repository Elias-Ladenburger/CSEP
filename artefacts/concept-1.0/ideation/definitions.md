## Scenario
A scenario is a set of *stories*. 

A scenario is suitable for one or more specific *target groups*.

The meta-information of a scenario includes a *title*, *description* and possible *image*.

## Game
A game is an instance of a scenario. 

## Story

Let story *S* be a directed graph. Let *I* be a set of all nodes of *S* and let *T* be the set of all edges of S. 

Note that the nodes of a story are hereafter referred to as *injects* and the edges of a story are referred to as *transitions*. 

## Inject
An inject provides the user with information or a task, thus advancing the scenario. It can be understood as a possible state that a game may reach. 

An inject may reference and be referenced by any number of *transitions*. An inject that only refers to one transition is an *informational inject*, while an inject that refers to multiple transitions is an *input inject*. 
An inject that is not referenced by a transition is called an *entry point*, whereas an inject that references no further transitions is called an *exit point*. 

An inject that neither refers to nor is referred by transitions is considered illegal. For the sake of simplicity, this case will not be considered further.

An inject can be *solved* by a learner, if they select a transition. The *exit point* cannot be solved.

An inject may have an *inject reaction*, which provides immediate feedback to the learner, after they have solved the inject.

## Transition
A *transition* describes a labeled, directed path from one inject to another inject. If multiple transitions point connect one inject to another, they can be called *choices*.

## Target Group
A target group is a set of statements which describe the type of learner that is expected to profit most from this scenario.

These statements refer to the *industry* of the organization of the learner, the *prior knowledge*, the *position* of the learner within their organization.

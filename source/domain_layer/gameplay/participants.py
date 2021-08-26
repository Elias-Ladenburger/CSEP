from datetime import datetime
from typing import List

from pydantic import BaseModel


class InjectHistory(BaseModel):
    """Represents a solution to a particular inject that a participant has submitted."""
    inject_slug: str
    timestamp: datetime = datetime.now()
    solution: str

    class Config:
        allow_mutation = False


class GameParticipant(BaseModel):
    """A participant of a GroupGame."""
    participant_id: str
    history: List[InjectHistory] = []

    def solve_inject(self, inject_slug: str, solution):
        """Append the solution for this inject to the solution history of this participant."""
        self.history.append(InjectHistory(inject_slug=inject_slug, solution=solution))

    def has_solved(self, inject_slug: str):
        """
        :returns: True, if the solution history of this participant contains this inject, False otherwise.
        """
        for entry in reversed(self.history):
            if entry.inject_slug == inject_slug:
                return True

    def get_solution(self, inject_slug):
        """Check, how this participant has solved a given inject.
        :return: the solution provided by the participant, if they have solved this inject. None otherwise."""
        for entry in reversed(self.history):
            if entry.inject_slug == inject_slug:
                return entry.solution
        return None


class AuthenticatedParticipant(BaseModel):
    pass


class UnauthenticatedParticipant(BaseModel):
    pass

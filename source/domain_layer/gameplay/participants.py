from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, PrivateAttr


class InjectHistory(BaseModel):
    inject_slug: str
    timestamp: datetime = datetime.now()
    solution: str

    class Config:
        allow_mutation = False


class GameParticipant(BaseModel):
    game_id: str
    participant_id: str
    history: List[InjectHistory] = []

    def solve_inject(self, inject_slug: str, solution):
        self.history.append(InjectHistory(inject_slug=inject_slug, solution=solution))

    def has_solved(self, inject_slug: str):
        for entry in reversed(self.history):
            if entry.inject_slug == inject_slug:
                return True

    def get_solution(self, inject_slug):
        for entry in reversed(self.history):
            if entry.inject_slug == inject_slug:
                return entry.solution
        return None


class AuthenticatedParticipant(BaseModel):
    pass


class UnauthenticatedParticipant(BaseModel):
    pass

from pydantic import BaseModel


class GameParticipant(BaseModel):
    pass


class AuthenticatedParticipant(BaseModel):
    pass


class UnauthenticatedParticipant(BaseModel):
    pass
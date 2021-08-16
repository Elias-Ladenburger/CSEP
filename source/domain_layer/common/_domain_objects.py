from pydantic import BaseModel, PrivateAttr


class AggregateRoot(BaseModel):
    _entity_id: str = PrivateAttr("new")


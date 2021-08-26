from pydantic import BaseModel, PrivateAttr


class AggregateRoot(BaseModel):
    """A base class for all aggregate roots."""
    _entity_id: str = PrivateAttr("new")


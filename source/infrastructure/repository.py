from bson import ObjectId

from infrastructure.database import CustomDB


class Repository:
    my_db = CustomDB

    @classmethod
    def _get_entity_by_id(cls, collection_name: str, entity_id: int):
        entity_id = Repository._build_object_id(entity_id=entity_id)
        id_criteria = {"_id": ObjectId(entity_id)}
        entity_id, entity = cls.my_db.get_one_by_criteria(collection_name=collection_name, criteria=id_criteria)
        return entity

    @classmethod
    def _get_all(cls, collection_name: str):
        entity_cursor = cls.my_db.get_all(collection_name=collection_name)
        return entity_cursor

    @classmethod
    def _save_entity(cls, collection_name: str, entity: dict):
        inserted_id = cls.my_db.insert_one(collection_name=collection_name, entity=entity)
        return inserted_id

    @classmethod
    def _delete_one(cls, collection_name: str, entity_id: int):
        entity_id = Repository._build_object_id(entity_id=entity_id)
        delete_criteria = {"_id": ObjectId(entity_id)}
        cls.my_db.delete_one(collection_name=collection_name, criteria=delete_criteria)

    @staticmethod
    def _build_object_id(entity_id):
        if isinstance(entity_id, str):
            entity_id = ObjectId(entity_id)
        if isinstance(entity_id, ObjectId):
            return entity_id
        else:
            return TypeError("Entity ID must be a string or of type 'bson.ObjectId'!")
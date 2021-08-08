from infrastructure_layer.database import CustomDB


class Repository:
    my_db = CustomDB

    @classmethod
    def _get_entity_by_id(cls, collection_name: str, entity_id):
        """
        :param collection_name: the name of the database collection or table from which the entity should be queried
        :param entity_id: the database id of the entity
        :return: a tuple of (entity_id: str, entity_data: dict)
        """
        id_criteria = {"_id": entity_id}
        entity_id, entity = cls.get_many_by_criteria(collection_name=collection_name, criteria=id_criteria)
        return entity_id, entity

    @classmethod
    def get_many_by_criteria(cls, collection_name: str, criteria: dict, exact_match: bool = True):
        """
        Find all entities that have the exact key-value pairs provided in criteria.

        :param collection_name: the name of the database collection or table from which the entity should be queried
        :param criteria: a dictionary of key-value pairs that an entity must possess.
        :param exact_match: if set to false, will also find entities that have a superset of the values.
        (i.e. if criteria is {"key": ["value"]}, this would also find an entity with {"key": ["value", "other value"]}
        :return: a tuple of (entity_id: str, entity_data: dict)
        """
        entity_id, entity = cls.my_db.get_one_by_criteria(collection_name=collection_name, criteria=criteria)
        return entity_id, entity

    @classmethod
    def _get_all(cls, collection_name: str):
        entity_cursor = cls.my_db.get_all(collection_name=collection_name)
        return entity_cursor

    @classmethod
    def _insert_entity(cls, collection_name: str, entity: dict):
        inserted_id = cls.my_db.insert_one(collection_name=collection_name, entity=entity)
        return inserted_id

    @classmethod
    def _delete_one(cls, collection_name: str, entity_id: str):
        delete_criteria = {"_id": entity_id}
        return cls.my_db.delete_one(collection_name=collection_name, criteria=delete_criteria)

    @classmethod
    def _update_entity(cls, collection_name: str, entity: dict, entity_id):
        return cls.my_db.save_one(collection_name=collection_name, new_values=entity, entity_id=entity_id)

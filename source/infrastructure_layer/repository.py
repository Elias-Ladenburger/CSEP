from infrastructure_layer.database import CustomDB


class Repository:
    my_db = CustomDB
    collection_name = ""

    @classmethod
    def _get_entity_by_id(cls, entity_id):
        """
        :param entity_id: the database id of the entity
        :return: a tuple of (entity_id: str, entity_data: dict)
        """
        id_criteria = {"_id": entity_id}
        entity_id, entity = cls.get_one_by_criteria(criteria=id_criteria)
        return entity_id, entity

    @classmethod
    def get_one_by_criteria(cls, criteria: dict):
        """Finds an entity, given the specified criteria."""
        entity_id, entity = cls.my_db.get_one_by_criteria(cls.collection_name, criteria)
        return entity_id, entity

    @classmethod
    def get_many_by_criteria(cls, criteria: dict, exact_match: bool = True):
        """
        Find all entities that have the exact key-value pairs provided in criteria.

        :param criteria: a dictionary of key-value pairs that an entity must possess.
        :param exact_match: if set to false, will also find entities that have a superset of the values.
        (i.e. if criteria is {"key": ["value"]}, this would also find an entity with {"key": ["value", "other value"]}
        :return: a tuple of (entity_id: str, entity_data: dict)
        """
        resultset = cls.my_db.get_many(collection_name=cls.collection_name, criteria=criteria, exact_match=exact_match)
        return resultset

    @classmethod
    def _get_all(cls):
        entity_cursor = cls.my_db.get_all(collection_name=cls.collection_name)
        return entity_cursor

    @classmethod
    def _insert_entity(cls, entity: dict):
        """Insert a new entity to the database.
        :param collection_name: The name of the database collection to insert the entity into.
        :param entity: A dictionary object of the entity data.
        :returns: The ID with which this entity can be retrieved from the database."""
        inserted_id = cls.my_db.insert_one(collection_name=cls.collection_name, entity=entity)
        return inserted_id

    @classmethod
    def _delete_one(cls, entity_id: str):
        """Remove an existing entity from the database.
            :param collection_name: The name of the database collection to insert the entity into.
            :param entity: A dictionary object of the entity data.
            :returns: The ID with which this entity can be retrieved from the database."""
        delete_criteria = {"_id": entity_id}
        return cls.my_db.delete_one(collection_name=cls.collection_name, criteria=delete_criteria)

    @classmethod
    def _update_entity(cls, entity: dict, entity_id):
        return cls.my_db.save_one(collection_name=cls.collection_name, new_values=entity, entity_id=entity_id)

    @classmethod
    def partial_update(cls, partial_dict: dict, entity_id: str = ""):
        if entity_id == "":
            entity_id = partial_dict.pop("_entity_id", "")
        if entity_id == "":
            raise ValueError("No id found for this entity!")
        entity_id, entity_dict = cls._get_entity_by_id(entity_id)
        for key in partial_dict:
            if key in entity_dict:
                entity_dict[key] = partial_dict[key]
        return cls._update_entity(entity_dict, entity_id)


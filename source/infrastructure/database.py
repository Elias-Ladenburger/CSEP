import bson
import pymongo
from bson import ObjectId
from bson.errors import InvalidId


class CustomDB:
    """
    A custom class for accessing a database.
    Currently wraps around the pymongo.MongoClient to provide convenience accessors.
    Legal MongoDB-query expressions can be found in the documentation: https://docs.mongodb.com/manual/reference/operator/query/
   """
    collections = dict(
        scenarios="scenarios",
        games="games",
        game_histories="game_histories",
        histories="game_histories",
        test="test"
    )

    @classmethod
    def get_collection_by_name(cls, collection_name: str):
        """
        Get a database collection or table by name.
        :param collection_name: the name of the collection to access.
        :return: an object that can perform database operations.
        """
        from globalconfig import config
        client = pymongo.MongoClient(
            config.get_db_config().DB_HOST)
        db = client[config.get_db_config().DB_NAME]
        coll = db[collection_name]
        if coll is None:
            raise NotImplemented
        else:
            return coll

    @classmethod
    def get_one_by_criteria(cls, collection_name: str, criteria: dict):
        """
        Find a single entity from a collection, by the criteria provided.
        :param collection_name: The collection in which to look for the entity.
        :param criteria: The criteria to filter for the entity.
        :returns: A single entity (first found, if multiple match the criteria).
        """
        collection = cls.get_collection_by_name(collection_name)
        entity_filter = CustomDB._build_filter(criteria=criteria)
        result = collection.find_one(filter=entity_filter)
        if result:
            result_id = str(result.pop("_id"))
        else:
            result_id = None
        return result_id, result

    @classmethod
    def get_all(cls, collection_name: str):
        """
        Convenience function. Returns all entities within a collection.
        :param collection_name: The collection from which all entities are to be retrieved.
        """
        collection = cls.get_collection_by_name(collection_name)
        return collection.find({})

    @classmethod
    def save_one(cls, collection_name: str, new_values: dict, entity_id=None):
        """
        Update an existing entity or insert, if it does not yet exist.

        :param collection_name: the name of the collection into which this object will be inserted.
        :param new_values: a dict with the data of the entity to be saved.
                            If entity exists already, these values will be updated.
        :param entity_id: Optional. The id of the entity to be saved.
        :returns: the id of the saved entity.
        """

        if "_id" not in new_values:
            if not entity_id:
                return cls.insert_one(collection_name=collection_name, entity=new_values)
        else:
            entity_id = new_values.pop("_id")
        return cls.update_one(collection_name=collection_name, new_values=new_values, entity_id=entity_id)

    @classmethod
    def insert_one(cls, collection_name: str, entity: dict):
        """
        :param collection_name: the name of the collection into which this object will be inserted
        :param entity: a dict with the data of the entity
        :returns: the id of the newly inserted entity
        """
        collection = cls.get_collection_by_name(collection_name)
        return str(collection.insert_one(entity).inserted_id)

    @classmethod
    def update_one(cls, collection_name: str, new_values: dict, entity_id):
        """
        :param collection_name: the name of the collection which contains the entity to be changed
        :param new_values: a dict with the data of the entity
        :param entity_id: the id of the entity that is to be changed
        :returns: the id of the changed entity
        """
        collection = cls.get_collection_by_name(collection_name)
        query_filter = CustomDB._build_filter({"_id": entity_id})
        update_statement = {"$set": new_values}
        collection.update_one(filter=query_filter, update=update_statement, upsert=True)
        return entity_id

    @classmethod
    def delete_one(cls, collection_name: str, criteria: dict):
        """
        :param collection_name: the name of the collection into which this object will be inserted
        :param criteria: a dict with criteria of what to delete
        :returns: the deletion result
        """
        collection = cls.get_collection_by_name(collection_name)
        entity_filter = CustomDB._build_filter(criteria)
        return collection.delete_one(filter=entity_filter)

    @classmethod
    def _purge_database(cls, collection_name: str, criteria: dict = None):
        """Should NOT be used in production"""
        if "prod" not in collection_name:
            if not criteria:
                query_filter = {}
            else:
                query_filter = CustomDB._build_filter(criteria=criteria)
            collection = cls.get_collection_by_name(collection_name)
            collection.delete_many(filter=query_filter)
        else:
            raise NotImplementedError("Purging a production database has consciously not been implemented."
                                      "If this is truly a necessary step, please clear the database directly.")

    @staticmethod
    def _build_filter(criteria: dict):
        if not criteria:
            pass
        if "_id" in criteria:
            entity_id = criteria["_id"]
            criteria["_id"] = CustomDB._build_object_id(entity_id)
        tmp_filter = criteria
        return tmp_filter

    @staticmethod
    def _build_object_id(entity_id):
        if isinstance(entity_id, str):
            try:
                entity_id = ObjectId(entity_id)
            except bson.errors.InvalidId:
                return ObjectId()
        if isinstance(entity_id, ObjectId):
            return entity_id
        else:
            return TypeError("Entity ID must be a string or of type 'bson.ObjectId'!")

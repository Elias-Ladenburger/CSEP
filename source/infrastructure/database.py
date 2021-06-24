import pymongo
from bson import ObjectId
from bson.errors import InvalidId


class CustomDB:
    """
    A custom class for accessing a database.
    Currently wraps around the pymongo.MongoClient to provide convenience accessors.
    Legal MongoDB-query expressions can be found in the documentation: https://docs.mongodb.com/manual/reference/operator/query/
   """
    from globalconfig import config
    _client = pymongo.MongoClient(
        config.get_db_config().DB_HOST)
    collections = dict(
        scenarios="scenarios",
        games="games",
        game_histories="game_histories",
        histories="game_histories",
        test="test"
    )

    @classmethod
    def get_collection_by_name(cls, collection_name: str):
        from globalconfig import config
        db = cls._client[config.get_db_config().DB_NAME]
        coll = db[collection_name]
        if coll is None:
            raise NotImplemented
        else:
            return coll

    @classmethod
    def get_one_by_criteria(cls, collection_name: str, criteria: dict):
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
        collection = cls.get_collection_by_name(collection_name)
        return collection.find({})

    @classmethod
    def save_one(cls, collection_name: str, new_values: dict, entity_id=None):
        if "_id" not in new_values:
            if not entity_id:
                cls.insert_one(collection_name=collection_name, entity=new_values)
        else:
            entity_id = new_values.pop("_id")
        cls.update_one(collection_name=collection_name, new_values=new_values, entity_id=entity_id)

    @classmethod
    def insert_one(cls, collection_name: str, entity: dict):
        collection = cls.get_collection_by_name(collection_name)
        return str(collection.insert_one(entity).inserted_id)

    @classmethod
    def update_one(cls, collection_name: str, new_values: dict, entity_id):
        collection = cls.get_collection_by_name(collection_name)
        query_filter = CustomDB._build_filter({"_id": entity_id})
        update_statement = {"$set": new_values}
        collection.update_one(filter=query_filter, update=update_statement, upsert=True)

    @classmethod
    def delete_one(cls, collection_name: str, criteria: dict):
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
            except InvalidId:
                return ObjectId("000000000000")
        if isinstance(entity_id, ObjectId):
            return entity_id
        else:
            return TypeError("Entity ID must be a string or of type 'bson.ObjectId'!")

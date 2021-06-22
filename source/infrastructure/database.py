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
        result = collection.find_one(filter=criteria)
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
    def insert_one(cls, collection_name: str, entity: dict):
        collection = cls.get_collection_by_name(collection_name)
        return collection.insert_one(entity)

    @classmethod
    def delete_one(cls, collection_name: str, criteria: dict):
        collection = cls.get_collection_by_name(collection_name)
        entity_filter = cls._build_filter(criteria)
        return collection.delete_one(filter=entity_filter)

    @classmethod
    def _purge_database(cls, collection_name: str, criteria: dict = None):
        """Should NOT be used in production"""
        if "prod" not in collection_name:
            if not criteria:
                criteria = {}
            collection = cls.get_collection_by_name(collection_name)
            collection.delete_many(filter=criteria)
        else:
            raise NotImplementedError("Purging a production database has consciously not been implemented."
                                      "If this is truly a necessary step, please clear the database directly.")

    @staticmethod
    def _build_filter(filter_id):
        try:
            tmp_filter = {"_id": ObjectId(filter_id)}
        except InvalidId:
            return {"_id": ObjectId("000000000000")}
        return tmp_filter

import pymongo
from bson import ObjectId


class CustomDatabase:
    """
    A custom class for accessing a database.
    Currently wraps around the pymongo.MongoClient to provide convenience accessors.
    Legal MongoDB-query expressions can be found in the documentation: https://docs.mongodb.com/manual/reference/operator/query/
   """
    def __init__(self, mode: str = "dev"):
        self._client = pymongo.MongoClient(
            "mongodb+srv://db_readwrite:8LMHkYjhNsXqa78f@univie-ladenburger-fygpi.mongodb.net/semtech?retryWrites=true&w=majority")
        if mode == "prod":
            client_name = "csep-prod"
        elif mode == "test":
            client_name = "csep-test"
        else:
            client_name = "csep-dev"
        self.db = self._client[client_name]
        self.collections = dict(
            scenarios=self.db["scenarios"],
            games=self.db["games"],
            game_histories=self.db["game_histories"],
            histories=self.db["game_histories"]
        )

    def get_coll_by_name(self, collection_name):
        coll = self.collections[collection_name]
        if coll is None:
            raise NotImplemented
        else:
            return self.collections[collection_name]

    def get_one_by_criteria(self, collection_name, criteria):
        db = self.get_coll_by_name(collection_name)
        result = db.find_one(filter=criteria)
        if result:
            result_id = str(result.pop("_id"))
        else:
            result_id = None
        return result_id, result

    def get_all(self, collection_name):
        db = self.get_coll_by_name(collection_name)
        return db.find({})

    def insert_one(self, collection_name, entity):
        db = self.get_coll_by_name(collection_name)
        return db.insert_one(entity)

    def delete_one(self, collection_name, criteria):
        db = self.get_coll_by_name(collection_name)
        entity_filter = self._build_filter(criteria)
        return db.delete_one(filter=entity_filter)

    def _purge_database(self, collection_name, criteria={}):
        """Should NOT be used in production"""
        db = self.get_coll_by_name(collection_name)
        db.delete_many(filter=criteria)

    @staticmethod
    def _build_filter(filter_id):
        try:
            tmp_filter = {"_id": ObjectId(filter_id)}
        except InvalidId:
            return {"_id": ObjectId("000000000000")}
        return tmp_filter

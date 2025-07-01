from pymongo import MongoClient
from pymongo.database import Database


class MongoDbConnection:
    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, mongo_uri: str, db: str = None):
        if hasattr(self, "_initialized") and self._initialized:
            return  # Evita reejecutar __init__ en el Singleton
        self.mongo_uri = mongo_uri
        self._database = db
        self._initialized = True

    def connect(self) -> Database:
        if self._client is None:
            try:
                self._client = MongoClient(
                    self.mongo_uri,
                    serverSelectionTimeoutMS=5000
                )
                self._client.admin.command('ismaster')  # Verifica la conexión
                self._database = self._client[self._database] 
                print(f"✅ Connection to Mongo client established successfully")
            except Exception as e:
                print(f"❌ Error connecting to MongoDB: {e}")
                raise
        return self._database

    def get_collection(self, collection_name):
        if self._database is None:
            self.connect()
        return self._database[collection_name]

    def create_collection(self, collection_name):
        if self._database is None:
            self.connect()
        if collection_name not in self._database.list_collection_names():
            self._database.create_collection(collection_name)
            print(f"✅ Collection '{collection_name}' created successfully")
        else:
            print(f"ℹ️ Collection '{collection_name}' already exists")

    def save_message_to_mongo(self, message_data, collection_name=None):
        if isinstance(collection_name, str):
            collection = self.get_collection(collection_name)
            collection.insert_one(message_data)
        else:
            raise ValueError("collection_name debe ser un string con el nombre de la colección")

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._database = None
            print("🔒 MongoDB connection closed")



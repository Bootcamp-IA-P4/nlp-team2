
from database import db_config as mdb
from dotenv import load_dotenv
import os
load_dotenv()


if __name__ == "__main__":
    try:
        # Initialize MongoDB connection
        print("🔗 Initializing MongoDB connection...")
        if not os.getenv('MONGO_URI') or not os.getenv('MONGO_DBNAME'):
            raise ValueError("Environment variables MONGO_URI and MONGO_DBNAME must be set")        
        # Create a MongoDbConnection instance
        try:
            mongo_db = mdb.MongoDbConnection(mongo_uri=os.getenv('MONGO_URI'),db=os.getenv('MONGO_DBNAME'))
            print("✅ MongoDB connection initialized with provided URI")
        except Exception as e:
            raise e
        # Connect to the MongoDB database                               
        try:             
            print("🔗 Connecting to MongoDB database...")
            mongo_db.connect()       
        except Exception as e:
            raise e
        # Create or access the collection
        try:
            source_collection_name = os.getenv("MONGO_SOURCE_COLLECTION")
            target_collection_name = os.getenv("MONGO_TARGET_COLLECTION")
            if not source_collection_name and not target_collection_name:
                raise ValueError("Environment variables MONGO_SOURCE_COLLECTION nnd MONGO_TARGET_COLLECTION must be set")
            source_collection = mongo_db.create_collection(source_collection_name)
            target_collection = mongo_db.create_collection(target_collection_name)
            
        except Exception as e:
            raise e

        mongo_db.close()


    except Exception as e:
        print(f"❌ Error creating MongoDB: {e}")
        raise e


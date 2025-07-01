
from database import db_config as mdb
from database import models
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
            for collection in models.get_collections():
                schema = models.get_schema_for_collection(collection)
                print(f"🔄 Creating collection '{collection}' with schema...")
                mongo_db.create_collection_with_schema(collection, schema)
                
                

            
        except Exception as e:
            raise e

        mongo_db.close()


    except Exception as e:
        print(f"❌ Error creating MongoDB: {e}")
        raise e


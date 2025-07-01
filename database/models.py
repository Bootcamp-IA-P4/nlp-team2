schema_video_urls= {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "description", "url"],
        "properties": {
            "video_id": {
                "bsonType": "string",
                "description": "Must be a string and is required"
            },
            "title": {
                "bsonType": "string",
                "description": "Must be a string and is required"
            },
            "description": {
                "bsonType": "string",
                "description": "Must be a string and is required"
            },
            "url": {
                "bsonType": "string",
                "pattern": "^https?://.+",
                "description": "Must be a valid URL starting with http:// or https://"
            }
        }
    }
}
schema_threads = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["thread_id", "title", "content", "parent_id", "created_at"],
        "properties": {
            "thread_id": {
                "bsonType": "string",
                "description": "Must be a string and is required"
            },
            "title": {
                "bsonType": "string",
                "description": "Must be a string and is required"
            },
            "content": {
                "bsonType": "string",
                "description": "Must be a string and is required"
            },
            "parent_id": {
                "bsonType": "string",
                "description": "Must be a string and is required"
            },
            "created_at": {
                "bsonType": "date",
                "description": "Must be a date and is required"
            }
        }
    }
}

collections = ["video_urls","threads"]
schemas = {"video_urls": schema_video_urls,
            "threads": schema_threads}

def get_collections():
    return collections

def get_schema_for_collection(collection_name):
    if collection_name in schemas:
        return schemas[collection_name]
    else:
        raise ValueError(f"Couldn't find schema. Collection '{collection_name}' does not exist.")






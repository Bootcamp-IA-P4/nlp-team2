schema_youtube_comments = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["nombre", "email"],
                "properties": {
                    "nombre": {
                        "bsonType": "string",
                        "description": "Debe ser un string y es obligatorio"
                    },
                    "email": {
                        "bsonType": "string",
                        "pattern": "^.+@.+\\..+$",
                        "description": "Debe ser un email válido"
                    },
                    "edad": {
                        "bsonType": "int",
                        "minimum": 0,
                        "maximum": 120,
                        "description": "Edad entre 0 y 120"
                    }
                }
            }
        }

schema_classified_comments = {}

collections = ["youtube_comments", 
               "classified_comments"]
schemas = {"youtube_comments": schema_youtube_comments,
            "classified_comments": schema_classified_comments}


def get_collections():
    return collections

def get_schema_for_collection(collection_name):
    if collection_name in schemas:
        return schemas[collection_name]
    else:
        raise ValueError(f"Collection '{collection_name}' does not exist.")






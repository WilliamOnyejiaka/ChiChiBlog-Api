from bson.objectid import ObjectId


def valid_object_id(identity: str) -> bool:
    try:
        ObjectId(identity)
        return True
    except Exception:
        return False

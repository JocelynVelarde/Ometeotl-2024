import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for encoding ObjectId as string.

    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

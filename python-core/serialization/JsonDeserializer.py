import json

from serialization.JsonObjectDecoder import JsonObjectDecoder

class JsonDeserializer:
    def deserialize(self, json_string):
        json_dictionary = json.loads(json_string)
        
        return json.loads(json.dumps(json_dictionary), object_hook=JsonObjectDecoder)